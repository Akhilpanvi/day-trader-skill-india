"""Offline checks for the India port. Run: python3 -m unittest discover -s tests -v

The chart data is SYNTHETIC (tests/fixtures/charts/DEMO.json, made by
make_demo_fixture.py): a made-up symbol, not market data.
"""
import json, os, shutil, subprocess, sys, tempfile, unittest, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARTS = os.path.join(ROOT, "tests", "fixtures", "charts")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


size = load("trader-budget/size.py", "size")
news = load("trader-news/news.py", "news")
scan = load("trader-scanner/scan.py", "scan")
entry = load("trader-entry/entry.py", "entry")


class Units(unittest.TestCase):
    def test_nse_clock(self):
        import datetime as dt
        self.assertEqual(entry.session(dt.date(2026, 11, 6)), (dt.time(9, 15), dt.time(15, 30)))
        self.assertFalse(entry.trading_day(dt.date(2026, 11, 10))[0])        # Diwali-Balipratipada
        self.assertEqual(entry.parse_now("2026-11-06 09:15"), dt.datetime(2026, 11, 6, 3, 45))  # IST = UTC+5:30

    def test_symbols(self):
        self.assertEqual(scan.nse("reliance"), "RELIANCE.NS")
        self.assertEqual(scan.nse("M&M"), "M%26M.NS")
        self.assertEqual(scan.nse("^NSEI"), "^NSEI")

    def test_charges(self):
        # buy 10 @ 1000, sell 10 @ 990: brokerage 3 + 2.97, STT 2.475, txn 0.611, SEBI 0.02, stamp 0.30, GST 1.19
        self.assertEqual(size.charges(10, 1000, 990), 10.56)
        self.assertEqual(size.charges(1000, 1000, 1000) > 40, True)  # Rs 20 cap per order kicks in

    def test_universe_keeps_eq_only(self):
        kept, counts, _ = scan.build_universe("SYMBOL,NAME OF COMPANY, SERIES\nAAA,A Ltd,EQ\nBBB,B Ltd,BE\n")
        self.assertEqual(kept, [("AAA", "A Ltd")])
        self.assertEqual(counts["series BE"], 1)

    def test_nse_feed_match(self):
        xml = (b"<rss><channel><item><title>Demo Synthetic Ltd</title><link>https://x/DEMO_1.pdf</link>"
               b"<description>Board Meeting to consider Financial Results |SUBJECT: Board Meeting Intimation"
               b"</description><pubDate>06-Nov-2026 08:33:11</pubDate></item></channel></rss>")
        items = news.parse_nse(xml, "board meeting", {"DEMO": "Demo Synthetic Limited"})
        self.assertEqual(len(items), 1)
        self.assertTrue(items[0]["important"])
        self.assertEqual(items[0]["time"].isoformat(), "2026-11-06T03:03:11+00:00")


class Pipeline(unittest.TestCase):
    """entry -> exit -> budget -> risk -> broker, offline, on the synthetic DEMO chart."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, "trader"))
        shutil.copy(os.path.join(ROOT, "trader-budget", "config.example.json"),
                    os.path.join(self.dir, "trader", "config.json"))

    def tearDown(self):
        shutil.rmtree(self.dir)

    def run_tool(self, path, *args):
        p = subprocess.run([sys.executable, "-I", os.path.join(ROOT, path)] + list(args),
                           cwd=self.dir, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr

    def read(self, name):
        with open(os.path.join(self.dir, "trader", name)) as fh:
            return json.load(fh)

    def test_one_trade(self):
        now = "2026-11-06 09:40"
        chart = os.path.join(CHARTS, "DEMO.json")
        code, out = self.run_tool("trader-entry/entry.py", "check", "DEMO", "--setup", "orb",
                                  "--now", now, "--offline", chart, "--write")
        self.assertIn("TRIGGERED 9:40 AM at ₹1513.50", out)
        self.run_tool("trader-exit/exit.py", "plan", "--now", now, "--write")
        plan = self.read("plan.json")
        self.assertEqual((plan["stop"], plan["target"], plan["flat_by"]), (1505.0, 1530.5, "15:10"))
        self.run_tool("trader-budget/size.py", "--now", now, "--write")
        order = self.read("orders.json")["orders"][0]
        self.assertEqual((order["qty"], order["exchange"], order["product"]), ("26", "NSE", "intraday"))
        self.assertEqual(order["plan"]["max_loss"], 262.68)  # 26 x 8.50 + 41.68 charges
        code, out = self.run_tool("trader-risk/check.py", "--now", now)
        self.assertEqual(code, 0, out)
        for reply in ("yes to all", "yes buy 30", "sure"):
            code, out = self.run_tool("trader-broker/ticket.py", "approve", "--index", "1", "--reply", reply, "--now", now)
            self.assertIn("Not recorded", out)
        code, out = self.run_tool("trader-broker/ticket.py", "approve", "--index", "1", "--reply", "yes", "--now", now)
        self.assertIn("Dry run: place it yourself", out)

    def test_risk_blocks_non_eq_series(self):
        with open(os.path.join(self.dir, "trader", "orders.json"), "w") as fh:
            json.dump({"orders": [{"symbol": "XYZ", "exchange": "NSE", "product": "intraday", "side": "buy",
                                   "qty": "1", "type": "market", "time_in_force": "day", "order_class": "bracket",
                                   "take_profit_limit_price": "110.00", "stop_loss_stop_price": "95.00",
                                   "plan": {"entry": 100, "stop": 95, "target": 110}}]}, fh)
        with open(os.path.join(self.dir, "trader", "universe.txt"), "w") as fh:
            fh.write("DEMO|Demo Synthetic Ltd\n")
        code, out = self.run_tool("trader-risk/check.py", "--now", "2026-11-06 10:00", "--no-write")
        self.assertEqual(code, 1)
        self.assertIn("not in the EQ series", out)

    def test_holiday_window_blocks(self):
        with open(os.path.join(self.dir, "trader", "orders.json"), "w") as fh:
            json.dump({"orders": [{"symbol": "DEMO", "side": "buy", "qty": "1", "type": "market",
                                   "time_in_force": "day", "order_class": "bracket",
                                   "take_profit_limit_price": "110.00", "stop_loss_stop_price": "95.00",
                                   "plan": {"entry": 100, "stop": 95, "target": 110}}]}, fh)
        code, out = self.run_tool("trader-risk/check.py", "--now", "2026-11-10 10:00", "--no-write")
        self.assertEqual(code, 1)
        self.assertIn("Diwali", out)


if __name__ == "__main__":
    unittest.main()
