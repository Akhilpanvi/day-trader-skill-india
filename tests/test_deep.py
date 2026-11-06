"""Deeper offline checks for the India port: clocks in every tool, charges against an
independent calculation, sizing and risk agreeing on random trades, Indian symbols
(M&M, BAJAJ-AUTO) through the whole pipeline, and the edges of the trading window.
All chart data is SYNTHETIC (tests/make_demo_fixture.py)."""
import datetime as dt, importlib.util, json, os, random, shutil, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tests"))
import make_demo_fixture  # noqa: E402


def load(path):
    name = path.replace("/", "_").replace(".py", "")
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


TOOLS = {k: load(v) for k, v in {
    "scan": "trader-scanner/scan.py", "entry": "trader-entry/entry.py", "exit": "trader-exit/exit.py",
    "tm": "trader-timemachine/timemachine.py", "size": "trader-budget/size.py", "risk": "trader-risk/check.py",
    "ticket": "trader-broker/ticket.py", "alerts": "trader-alerts/alerts.py", "news": "trader-news/news.py"}.items()}
HOLIDAYS_2026 = ["2026-01-15", "2026-01-26", "2026-03-03", "2026-03-26", "2026-03-31", "2026-04-03",
                 "2026-04-14", "2026-05-01", "2026-05-28", "2026-06-26", "2026-09-14", "2026-10-02",
                 "2026-10-20", "2026-11-10", "2026-11-24", "2026-12-25"]


def ref_charges(qty, buy, sell):
    """Independent re-implementation of zerodha.com/charges intraday (read 2026-11-06)."""
    bv, sv = qty * buy, qty * sell
    brok = min(20.0, bv * 0.0003) + min(20.0, sv * 0.0003)
    stt = sv * 0.00025
    txn = (bv + sv) * 0.0000307
    sebi = (bv + sv) * 10 / 1e7
    stamp = bv * 0.00003
    gst = 0.18 * (brok + txn + sebi)
    return brok + stt + txn + sebi + stamp + gst


class Clocks(unittest.TestCase):
    def test_every_tool_is_ist(self):
        for name, m in TOOLS.items():
            if not hasattr(m, "to_eastern"):
                continue
            for _ in range(200):
                u = dt.datetime(2026, 1, 1) + dt.timedelta(minutes=random.randint(0, 525600))
                self.assertEqual(m.to_eastern(u) - u, dt.timedelta(hours=5, minutes=30), name)
                if hasattr(m, "eastern_to_utc"):
                    self.assertEqual(m.eastern_to_utc(m.to_eastern(u)), u, name)

    def test_parse_now_is_ist(self):
        for name in ("scan", "entry", "exit", "tm", "size", "risk", "ticket", "alerts"):
            got = TOOLS[name].parse_now("2026-11-06 09:15")
            got = got.replace(tzinfo=None) if hasattr(got, "replace") else got
            self.assertEqual(got, dt.datetime(2026, 11, 6, 3, 45), name)

    def test_same_holidays_everywhere(self):
        for name, m in TOOLS.items():
            if hasattr(m, "NSE_HOLIDAYS"):
                self.assertEqual(sorted(m.NSE_HOLIDAYS), HOLIDAYS_2026, name)
                self.assertEqual(m.NSE_EARLY_CLOSE, {}, name)

    def test_trading_days(self):
        for name in ("scan", "entry", "risk", "alerts"):
            td = TOOLS[name].trading_day
            for h in HOLIDAYS_2026:
                self.assertFalse(td(dt.date.fromisoformat(h))[0], (name, h))
            self.assertFalse(td(dt.date(2026, 11, 7))[0], name)       # Saturday
            self.assertFalse(td(dt.date(2026, 11, 8))[0], name)       # Sunday (Muhurat not modelled)
            self.assertTrue(td(dt.date(2026, 11, 6))[0], name)        # Friday
            self.assertTrue(td(dt.date(2026, 11, 11))[0], name)       # day after Diwali holiday

    def test_sessions(self):
        for name in ("scan", "entry", "exit", "alerts"):
            self.assertEqual(TOOLS[name].session(dt.date(2026, 11, 6)), (dt.time(9, 15), dt.time(15, 30)), name)
        tm = TOOLS["tm"]
        self.assertEqual((tm.SESSION_BARS, tm.OPEN_MIN, tm.CLOSE_MIN), (75, 555, 930))


class Charges(unittest.TestCase):
    def test_matches_independent_calc(self):
        rnd = random.Random(1)
        for _ in range(2000):
            q = rnd.randint(1, 5000)
            b = round(rnd.uniform(10, 5000), 2)
            s = round(b * rnd.uniform(0.9, 1.1), 2)
            self.assertAlmostEqual(TOOLS["size"].charges(q, b, s), ref_charges(q, b, s), delta=0.011)
            self.assertEqual(TOOLS["size"].charges(q, b, s), TOOLS["risk"].charges(q, b, s))

    def test_overrides(self):
        self.assertLess(TOOLS["size"].charges(10, 1000, 1000, {"brokerage_max": 0}),
                        TOOLS["size"].charges(10, 1000, 1000))


class Sizing(unittest.TestCase):
    def test_random_trades_fit_and_agree_with_risk(self):
        size, risk = TOOLS["size"], TOOLS["risk"]
        rnd = random.Random(2)
        n_orders = 0
        for _ in range(1500):
            entry = round(rnd.uniform(20, 4000), 2)
            stop = round(entry * (1 - rnd.uniform(0.002, 0.03)), 2)
            target = round(entry + (entry - stop) * rnd.choice([1, 1.5, 2, 3]), 2)
            cfg = {"budget": rnd.choice([20000, 100000, 500000]), "max_loss_per_trade_inr": rnd.choice([100, 500, 2000]),
                   "max_order_inr": rnd.choice([10000, 40000, 200000]), "min_order_inr": 0, "max_daily_loss_inr": 10 ** 6}
            if stop <= 0 or stop >= entry:
                continue
            s = size.size_trade({"symbol": "DEMO", "entry": entry, "stop": stop, "target": target}, cfg)
            if s["refusal"]:
                continue
            q = s["qty"]
            self.assertLessEqual(s["max_loss"], cfg["max_loss_per_trade_inr"] + 0.005)
            self.assertAlmostEqual(s["max_loss"], q * (s["entry"] - s["stop"]) + size.charges(q, s["entry"], s["stop"]), delta=0.02)
            o = size.bracket_order(s)
            res = risk.check([o], cfg, now=dt.datetime(2026, 11, 6, 4, 30))   # 10:00 IST
            r = res["results"][0]
            self.assertEqual(r["verdict"], "PASS", (cfg, o, r["reasons"]))
            self.assertAlmostEqual(r["max_loss"], s["max_loss"], delta=0.011)
            n_orders += 1
        self.assertGreater(n_orders, 500)

    def test_one_more_share_breaks_max_loss(self):
        size = TOOLS["size"]
        s = size.size_trade({"symbol": "DEMO", "entry": 1513.5, "stop": 1505, "target": 1530.5},
                            {"budget": 10 ** 7, "max_loss_per_trade_inr": 500, "max_order_inr": 10 ** 7})
        q = s["qty"]
        self.assertEqual(s["bound_by"], "max loss")
        self.assertLessEqual(q * 8.5 + size.charges(q, 1513.5, 1505), 500)
        self.assertGreater((q + 1) * 8.5 + size.charges(q + 1, 1513.5, 1505), 500)


class RiskWindow(unittest.TestCase):
    ORDER = {"symbol": "DEMO", "exchange": "NSE", "product": "intraday", "side": "buy", "qty": "10",
             "type": "market", "time_in_force": "day", "order_class": "bracket",
             "take_profit_limit_price": "110.00", "stop_loss_stop_price": "95.00",
             "plan": {"entry": 100, "stop": 95, "target": 110}}

    def verdict(self, ist, cfg=None, universe=None):
        risk = TOOLS["risk"]
        now = risk.parse_now(ist)
        return risk.check([dict(self.ORDER)], dict({"budget": 100000}, **(cfg or {})), now=now, universe=universe)

    def test_edges(self):
        cases = {"2026-11-06 09:14": "BLOCK", "2026-11-06 09:29": "BLOCK", "2026-11-06 09:30": "PASS",
                 "2026-11-06 14:59": "PASS", "2026-11-06 15:01": "BLOCK", "2026-11-06 15:31": "BLOCK",
                 "2026-11-07 10:00": "BLOCK", "2026-11-10 10:00": "BLOCK", "2026-11-11 10:00": "PASS"}
        for ist, want in cases.items():
            self.assertEqual(self.verdict(ist)["results"][0]["verdict"], want, ist)

    def test_square_off_warning(self):
        res = self.verdict("2026-11-06 10:00", {"flat_by": "15:20"})
        self.assertTrue(any("auto square-off" in w for w in res["warnings"]))
        res = self.verdict("2026-11-06 10:00")
        self.assertFalse(any("auto square-off" in w for w in res["warnings"]))

    def test_live_warning(self):
        self.assertTrue(any("LIVE" in w for w in self.verdict("2026-11-06 10:00", {"dry_run": False})["warnings"]))
        self.assertFalse(any("LIVE" in w for w in self.verdict("2026-11-06 10:00")["warnings"]))

    def test_series(self):
        self.assertEqual(self.verdict("2026-11-06 10:00", universe={"DEMO"})["results"][0]["verdict"], "PASS")
        self.assertEqual(self.verdict("2026-11-06 10:00", universe={"OTHER"})["results"][0]["verdict"], "BLOCK")

    def test_loss_includes_charges(self):
        # 100 shares, 5 risk = 500, plus charges > 500 limit -> BLOCK
        o = dict(self.ORDER, qty="100")
        risk = TOOLS["risk"]
        res = risk.check([o], {"budget": 100000, "max_loss_per_trade_inr": 500}, now=risk.parse_now("2026-11-06 10:00"))
        self.assertEqual(res["results"][0]["verdict"], "BLOCK")
        self.assertIn("charges", " ".join(res["results"][0]["reasons"]))


class Yes(unittest.TestCase):
    def test_indian_symbols(self):
        py = TOOLS["ticket"].parse_yes
        o = {"symbol": "M&M", "side": "buy", "qty": "10", "type": "market", "time_in_force": "day"}
        self.assertTrue(py("yes", o)[0])
        self.assertTrue(py("yes M&M 10", o)[0])
        self.assertFalse(py("yes BAJAJ-AUTO", o, batch_symbols=["M&M", "BAJAJ-AUTO"])[0])
        self.assertFalse(py("yes 11", o)[0])
        self.assertFalse(py("ok", o)[0])
        self.assertFalse(py("yes?", o)[0])
        self.assertFalse(py("yes to all", o)[0])


class News(unittest.TestCase):
    def test_name_variants(self):
        n = TOOLS["news"]
        for feed_name, ours in [("Mahindra & Mahindra Limited", "Mahindra & Mahindra Ltd"),
                                ("Bajaj Auto Limited", "Bajaj Auto Ltd."), ("ITC Limited", "ITC Ltd")]:
            xml = ("<rss><channel><item><title>%s</title><link>https://x/a.pdf</link><description>Updates"
                   "</description><pubDate>06-Nov-2026 10:00:00</pubDate></item></channel></rss>" % feed_name.replace("&", "&amp;"))
            self.assertEqual(len(n.parse_nse(xml.encode(), "announcement", {"SYM": ours})), 1, feed_name)

    def test_no_false_match(self):
        n = TOOLS["news"]
        xml = (b"<rss><channel><item><title>Reliance Power Limited</title><link>https://x/RPOWER_1.pdf</link>"
               b"<description>x</description><pubDate>06-Nov-2026 10:00:00</pubDate></item></channel></rss>")
        self.assertEqual(n.parse_nse(xml, "announcement", {"RELIANCE": "Reliance Industries Limited"}), [])

    def test_important_flag(self):
        n = TOOLS["news"]
        def one(desc):
            xml = ("<rss><channel><item><title>A Ltd</title><link>https://x/AAA_1.pdf</link><description>%s"
                   "</description><pubDate>06-Nov-2026 10:00:00</pubDate></item></channel></rss>" % desc).encode()
            return n.parse_nse(xml, "announcement", {"AAA": None})[0]["important"]
        self.assertTrue(one("Outcome of Board Meeting"))
        self.assertTrue(one("Credit Rating"))
        self.assertFalse(one("Copy of Newspaper Publication"))


class Pipelines(unittest.TestCase):
    """The whole flow for awkward NSE symbols, from the command line, offline."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, "trader"))
        os.makedirs(os.path.join(self.dir, "charts"))
        shutil.copy(os.path.join(ROOT, "trader-budget", "config.example.json"), os.path.join(self.dir, "trader", "config.json"))

    def tearDown(self):
        shutil.rmtree(self.dir)

    def run_tool(self, path, *args):
        p = subprocess.run([sys.executable, "-I", os.path.join(ROOT, path)] + list(args),
                           cwd=self.dir, capture_output=True, text=True, timeout=120)
        return p.returncode, p.stdout + p.stderr

    def flow(self, sym):
        chart = os.path.join(self.dir, "charts", sym + ".json")
        with open(chart, "w") as fh:
            json.dump(make_demo_fixture.build(symbol=sym), fh)
        now = "2026-11-06 09:40"
        code, out = self.run_tool("trader-scanner/scan.py", "orb", "--offline", os.path.join(self.dir, "charts"),
                                  "--now", now, "--symbols", sym, "--min-price", "0")
        self.assertIn("1 of 1 charts closed above", out, out)
        with open(os.path.join(self.dir, "trader", "watchlist.json")) as fh:
            wl = json.load(fh)
        self.assertEqual(wl["hits"][0]["symbol"], sym)
        code, out = self.run_tool("trader-entry/entry.py", "check", sym, "--setup", "orb", "--now", now, "--offline", chart, "--write")
        self.assertIn("TRIGGERED", out, out)
        code, out = self.run_tool("trader-exit/exit.py", "plan", "--now", now, "--write")
        self.assertEqual(code, 0, out)
        code, out = self.run_tool("trader-timemachine/timemachine.py", "run", "--offline", chart, "--now", now, "--write")
        self.assertEqual(code, 0, out)
        self.assertIn("10,000 replays", out)
        code, out = self.run_tool("trader-budget/size.py", "--now", now, "--write")
        self.assertEqual(code, 0, out)
        with open(os.path.join(self.dir, "trader", "universe.txt"), "w") as fh:
            fh.write("%s|Synthetic\n" % sym)
        code, out = self.run_tool("trader-risk/check.py", "--now", now)
        self.assertEqual(code, 0, out)
        code, out = self.run_tool("trader-broker/ticket.py", "show", "--now", now)
        self.assertIn("READY", out)
        self.assertIn('"symbol": "%s"' % sym, out)
        code, out = self.run_tool("trader-broker/ticket.py", "approve", "--index", "1", "--reply", "yes " + sym, "--now", now)
        self.assertIn("Recorded your yes", out, out)
        code, out = self.run_tool("trader-broker/ticket.py", "result", "--index", "1", "--status", "placed",
                                  "--broker-id", "X1", "--filled-qty", "26", "--filled-price", "1513.6", "--now", now)
        self.assertEqual(code, 0, out)
        code, out = self.run_tool("trader-broker/ticket.py", "flatten", "--symbol", sym, "--qty", "26", "--now", "2026-11-06 15:10")
        self.assertEqual(code, 0, out)
        code, out = self.run_tool("trader-risk/check.py", "--now", "2026-11-06 15:10")
        self.assertEqual(code, 0, out)          # an exit is never blocked by the window
        code, out = self.run_tool("trader-alerts/alerts.py", "add", "--from-plan")
        self.assertIn("flat-by", out)

    def test_demo(self):
        self.flow("DEMO")

    def test_ampersand(self):
        self.flow("M&M")

    def test_hyphen(self):
        self.flow("BAJAJ-AUTO")

    def test_scan_before_range_and_holiday(self):
        chart_dir = os.path.join(self.dir, "charts")
        with open(os.path.join(chart_dir, "DEMO.json"), "w") as fh:
            json.dump(make_demo_fixture.build(), fh)
        code, out = self.run_tool("trader-scanner/scan.py", "orb", "--offline", chart_dir, "--now", "2026-11-06 09:25", "--symbols", "DEMO")
        self.assertEqual(code, 1, out)
        code, out = self.run_tool("trader-scanner/scan.py", "orb", "--offline", chart_dir, "--now", "2026-11-10 10:00", "--symbols", "DEMO")
        self.assertEqual(code, 1)
        self.assertIn("holiday", out.lower())

    def test_daily_scan_runs(self):
        chart_dir = os.path.join(self.dir, "charts")
        with open(os.path.join(chart_dir, "DEMO.json"), "w") as fh:
            json.dump(make_demo_fixture.build(), fh)
        code, out = self.run_tool("trader-scanner/scan.py", "daily", "--offline", chart_dir, "--now", "2026-11-06 08:30",
                                  "--symbols", "DEMO", "--min-price", "0", "--min-volume", "0")
        self.assertIn(code, (0, 1), out)
        self.assertNotIn("Traceback", out)

    def test_alert_clock(self):
        code, out = self.run_tool("trader-alerts/alerts.py", "clock", "--now", "2026-11-10 10:00")
        self.assertIn("Diwali-Balipratipada", out)
        self.assertIn("2026-11-11 09:15", out)
        code, out = self.run_tool("trader-alerts/alerts.py", "clock", "--now", "2027-01-05 10:00")
        self.assertNotIn("Traceback", out)


if __name__ == "__main__":
    unittest.main()


class Scenarios(Pipelines):
    """More command-line paths: alerts ringing, live wording, limit orders, news CLI, NSE CSV quirks."""

    def chart(self, sym="DEMO"):
        path = os.path.join(self.dir, "charts", sym + ".json")
        with open(path, "w") as fh:
            json.dump(make_demo_fixture.build(symbol=sym), fh)
        return path

    def test_alert_rings_once(self):
        doc = make_demo_fixture.build()
        last = doc["chart"]["result"][0]["meta"]["regularMarketPrice"]
        doc["chart"]["result"][0]["meta"]["regularMarketTime"] = doc["chart"]["result"][0]["timestamp"][-1]
        off = os.path.join(self.dir, "quotes")
        os.makedirs(off)
        with open(os.path.join(off, "yahoo-DEMO.json"), "w") as fh:
            json.dump(doc, fh)
        self.run_tool("trader-alerts/alerts.py", "add", "--symbol", "DEMO", "--above", str(round(last - 1, 2)))
        code, out = self.run_tool("trader-alerts/alerts.py", "check", "--offline", off, "--now", "2026-11-06 15:29")
        self.assertIn("₹", out, out)
        self.assertIn("DEMO", out)
        code2, out2 = self.run_tool("trader-alerts/alerts.py", "check", "--offline", off, "--now", "2026-11-06 15:29")
        self.assertNotEqual(out.count("above"), 0)
        self.assertNotIn("Traceback", out + out2)

    def test_live_ticket_wording(self):
        self.flow("DEMO")
        cfg_path = os.path.join(self.dir, "trader", "config.json")
        with open(cfg_path) as fh:
            cfg = json.load(fh)
        cfg.update(dry_run=False, broker="dhan")
        with open(cfg_path, "w") as fh:
            json.dump(cfg, fh)
        code, out = self.run_tool("trader-broker/ticket.py", "show", "--now", "2026-11-06 15:10")
        self.assertIn("LIVE ACCOUNT, REAL MONEY", out)
        self.assertIn("Dhan", out)
        code, out = self.run_tool("trader-risk/check.py", "--now", "2026-11-06 15:10")
        self.assertIn("LIVE", out)

    def test_zerodha_note(self):
        self.flow("DEMO")
        cfg_path = os.path.join(self.dir, "trader", "config.json")
        with open(cfg_path) as fh:
            cfg = json.load(fh)
        cfg["broker"] = "zerodha"
        with open(cfg_path, "w") as fh:
            json.dump(cfg, fh)
        code, out = self.run_tool("trader-broker/ticket.py", "show", "--now", "2026-11-06 15:10")
        self.assertIn("GTT orders only", out)

    def test_limit_order_and_stale_plan(self):
        chart = self.chart()
        now = "2026-11-06 09:40"
        self.run_tool("trader-entry/entry.py", "check", "DEMO", "--setup", "orb", "--now", now, "--offline", chart, "--write")
        self.run_tool("trader-exit/exit.py", "plan", "--now", now, "--write", "--stop", "pct:0.5", "--target", "1.5R")
        code, out = self.run_tool("trader-budget/size.py", "--now", now, "--limit", "1512.00", "--write")
        self.assertEqual(code, 0, out)
        with open(os.path.join(self.dir, "trader", "orders.json")) as fh:
            o = json.load(fh)["orders"][0]
        self.assertEqual((o["type"], o["limit_price"]), ("limit", "1512.00"))
        code, out = self.run_tool("trader-budget/size.py", "--now", "2026-11-07 09:40")
        self.assertNotEqual(code, 0)                       # plan is for another day
        self.assertIn("another day", out.replace("is for 2026-11-06 and today is 2026-11-07", "another day"))

    def test_tm_chart_and_until(self):
        chart = self.chart()
        now = "2026-11-06 09:40"
        self.run_tool("trader-entry/entry.py", "check", "DEMO", "--setup", "orb", "--now", now, "--offline", chart, "--write")
        self.run_tool("trader-exit/exit.py", "plan", "--now", now, "--write")
        code, out = self.run_tool("trader-timemachine/timemachine.py", "run", "--offline", chart, "--now", now, "--until", "15:10")
        self.assertEqual(code, 0, out)
        self.assertIn("3:10 PM", out)
        code, out = self.run_tool("trader-timemachine/timemachine.py", "chart", "--offline", chart, "--now", now)
        self.assertEqual(code, 0, out)

    def test_news_cli_with_universe(self):
        off = os.path.join(self.dir, "news")
        os.makedirs(off)
        with open(os.path.join(off, "yahoo-RELIANCE.xml"), "w") as fh:
            fh.write("<rss><channel></channel></rss>")
        with open(os.path.join(off, "nse-Board_Meetings.xml"), "w") as fh:
            fh.write("<rss><channel><item><title>Reliance Industries Limited</title><link>https://x/bm.pdf</link>"
                     "<description>Reliance Industries Limited has informed the Exchange about Board Meeting to "
                     "consider Financial Results |SUBJECT: Board Meeting Intimation</description>"
                     "<pubDate>06-Nov-2026 08:00:00</pubDate></item></channel></rss>")
        for f in ("nse-Online_announcements.xml", "nse-Financial_Results.xml"):
            with open(os.path.join(off, f), "w") as fh:
                fh.write("<rss><channel></channel></rss>")
        with open(os.path.join(self.dir, "trader", "universe.txt"), "w") as fh:
            fh.write("RELIANCE|Reliance Industries Ltd\n")
        code, out = self.run_tool("trader-news/news.py", "--tickers", "RELIANCE.NS", "--offline", off, "--no-moves",
                                  "--now", "2026-11-06T04:00:00Z")
        self.assertIn("! 2026-11-06 08:00 IST  RELIANCE", out, out)
        self.assertNotIn("no company names", out)
        code, out = self.run_tool("trader-news/news.py", "--tickers", "RELIANCE", "--offline", off, "--no-moves",
                                  "--now", "2026-11-06T04:00:00Z")
        self.assertIn("Nothing new.", out)               # seen once, shown once

    def test_real_nse_csv_shape(self):
        # NSE's header has leading spaces and the file may start with a BOM
        csv = ("﻿SYMBOL,NAME OF COMPANY, SERIES, DATE OF LISTING, PAID UP VALUE, MARKET LOT, ISIN NUMBER, FACE VALUE\n"
               "20MICRONS,20 Microns Limited,EQ,06-OCT-2008,5,1,INE144J01027,5\n"
               "M&M,Mahindra & Mahindra Limited,EQ,29-NOV-1995,5,1,INE101A01026,5\n"
               "BAJAJ-AUTO,Bajaj Auto Limited,EQ,26-MAY-2008,10,1,INE917I01010,10\n"
               "ZZZ,Zzz Limited,BE,01-JAN-2020,10,1,INE000000000,10\n"
               "YYY,Yyy Limited,BZ,01-JAN-2020,10,1,INE000000001,10\n")
        path = os.path.join(self.dir, "EQUITY_L.csv")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(csv)
        code, out = self.run_tool("trader-scanner/scan.py", "universe", "--offline", path)
        self.assertEqual(code, 0, out)
        with open(os.path.join(self.dir, "trader", "universe.txt")) as fh:
            syms = [l.split("|")[0] for l in fh.read().splitlines()]
        self.assertEqual(syms, ["20MICRONS", "BAJAJ-AUTO", "M&M"])
        self.assertIn("1 series BE", out)
        self.assertIn("1 series BZ", out)
