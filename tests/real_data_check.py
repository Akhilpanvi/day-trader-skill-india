#!/usr/bin/env python3
"""Real-data check: runs the pack on REAL NSE data (Yahoo .NS charts, NSE's own
files) and writes a report. Meant for GitHub Actions (.github/workflows/real-data.yml)
or your own computer; it needs internet. Standard library only.

    python3 tests/real_data_check.py                 # default symbol list
    python3 tests/real_data_check.py RELIANCE INFY   # your own list

What it does, per symbol:
  1. one request: 60 days of 5-minute bars (Yahoo, unofficial, can lag or 429)
  2. data sanity: sessions, bars per session, gaps, the IST 9:15-15:30 grid
  3. replays the newest session through the pipeline at 10:15 IST, offline on
     that real chart: entry -> exit -> time machine -> budget -> risk -> ticket
  4. backtest: the opening-range rule on every full session, for a few stop and
     target choices, with Indian charges, at a fixed Rs 500 risk a trade
Plus live checks of NSE's EQUITY_L.csv and the NSE news feeds.

Writes out/REPORT.md and out/summary.json: derived numbers only, never the raw
Yahoo data. A backtest on 60 days is a small, in-sample sample: it describes
those days, it does not predict the next ones. Not financial advice.
"""
import importlib.util, json, math, os, statistics, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")
SYMBOLS = ["RELIANCE", "HDFCBANK", "ICICIBANK", "INFY", "TCS", "SBIN", "ITC", "LT", "AXISBANK",
           "KOTAKBANK", "BHARTIARTL", "HINDUNILVR", "BAJFINANCE", "MARUTI", "M&M", "SUNPHARMA",
           "TITAN", "NTPC", "BAJAJ-AUTO", "ULTRACEMCO"]
RISK_INR = 500
GRID = [(15, "or_mid", 1.0), (15, "or_mid", 2.0), (15, "or_low", 1.0), (15, "or_low", 2.0),
        (30, "or_mid", 1.0), (30, "or_mid", 2.0), (30, "or_low", 1.5)]


def load(path):
    spec = importlib.util.spec_from_file_location(path.replace("/", "_")[:-3], os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


tm = load("trader-timemachine/timemachine.py")
size = load("trader-budget/size.py")


def run(work, path, *args, timeout=180):
    p = subprocess.run([sys.executable, "-I", os.path.join(ROOT, path)] + list(args), cwd=work,
                       capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def sanity(sym, text):
    res = tm.chart_result(text, sym)
    now = tm.parse_now(None)
    meta, bars, dropped = tm.parse_bars(res, now)
    days = tm.split_sessions(bars)
    full, short = tm.full_sessions(days, "9999-12-31")
    filled = sum(1 for _, D in full for b in D if b.get("filled"))
    starts = sorted({b["start"] for b in bars})
    return {"meta_symbol": meta.get("symbol"), "currency": meta.get("currency"), "tz": meta.get("exchangeTimezoneName"),
            "bars": len(bars), "sessions": len(days), "full_sessions": len(full), "filled_bars": filled,
            "short_sessions": [s["date"] + ":" + str(s["bars"]) for s in short][-5:],
            "first_bar": starts[0] if starts else None, "last_bar": starts[-1] if starts else None,
            "dropped": dropped, "last_day": max(days) if days else None}, full


def backtest(full):
    """The history rule on every full session for each grid point, with charges at fixed rupee risk."""
    out = []
    last = (15 * 60 + 5 - tm.OPEN_MIN) // 5          # the 15:05 bar: flat by 15:10
    for orm, stop_rule, tr in GRID:
        h = tm.history_replay(full, {"setup": "orb", "or_minutes": orm, "stop_rule": stop_rule, "target_r": tr}, last)
        net, gross, fees = [], 0.0, 0.0
        for t in h["trades"]:
            risk = t["entry"] - t["stop"]
            q = int(RISK_INR // risk) if risk > 0 else 0
            if q <= 0:
                continue
            exit_px = t["entry"] + t["R"] * risk
            g = q * (exit_px - t["entry"])
            f = size.charges(q, t["entry"], exit_px)
            gross += g
            fees += f
            net.append(g - f)
        out.append({"or_minutes": orm, "stop": stop_rule, "target_R": tr, "sessions": h["sessions"],
                    "trades": len(net), "target": h["target"], "stop_hits": h["stop"], "at_close": h["close"],
                    "avg_R_before_charges": h["avg_R"], "gross_inr": round(gross, 2), "charges_inr": round(fees, 2),
                    "net_inr": round(sum(net), 2), "net_per_trade": round(statistics.mean(net), 2) if net else None,
                    "win_rate_net": round(sum(1 for x in net if x > 0) / len(net), 3) if net else None})
    return out


def pipeline(sym, text, day):
    work = tempfile.mkdtemp()
    os.makedirs(os.path.join(work, "trader"))
    with open(os.path.join(ROOT, "trader-budget", "config.example.json")) as fh:
        cfg = json.load(fh)
    with open(os.path.join(work, "trader", "config.json"), "w") as fh:
        json.dump(cfg, fh)
    chart = os.path.join(work, "chart.json")
    with open(chart, "w") as fh:
        fh.write(text)
    now = "%s 10:15" % day
    steps = []
    code, out = run(work, "trader-entry/entry.py", "check", sym, "--setup", "orb", "--now", now, "--offline", chart, "--write")
    steps.append(("entry", code, out.splitlines()[:3]))
    if "TRIGGERED" not in out:
        return {"triggered_by_10_15": False, "steps": steps}
    for name, args in [("exit", ["trader-exit/exit.py", "plan", "--now", now, "--write"]),
                       ("timemachine", ["trader-timemachine/timemachine.py", "run", "--offline", chart, "--now", now,
                                        "--until", "15:10", "--write"]),
                       ("budget", ["trader-budget/size.py", "--now", now, "--write"]),
                       ("risk", ["trader-risk/check.py", "--now", now]),
                       ("ticket", ["trader-broker/ticket.py", "show", "--now", now])]:
        code, out = run(work, *args)
        steps.append((name, code, out.splitlines()[:6]))
        if code not in (0,) and name != "risk":
            break
    return {"triggered_by_10_15": True, "steps": steps}


def live_checks():
    work = tempfile.mkdtemp()
    os.makedirs(os.path.join(work, "trader"))
    res = {}
    code, out = run(work, "trader-scanner/scan.py", "universe", timeout=120)
    res["nse_universe"] = {"exit": code, "out": out.splitlines()[:4]}
    code, out = run(work, "trader-news/news.py", "--tickers", "RELIANCE", "INFY", "HDFCBANK", "TCS", "--no-moves",
                    "--dry-run", "--all", "--hours", "168", "--universe", os.path.join(work, "trader", "universe.txt"),
                    "--json", timeout=180)
    try:
        doc = json.loads(out)
        by = {}
        for it in doc["items"]:
            by[it["source"]] = by.get(it["source"], 0) + 1
        res["news"] = {"exit": code, "out": ["items by source (7 days): %s" % (by or "none"),
                                             "notes: %s" % ("; ".join(doc["notes"]) or "none")]}
    except ValueError:
        res["news"] = {"exit": code, "out": out.splitlines()[:6]}
    return res


def fmt_bt(rows):
    lines = ["| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        lines.append("| %dm | %s | %sR | %d | %d/%d/%d | %s | %s | %s | %s | %s |" % (
            r["or_minutes"], r["stop"], r["target_R"], r["trades"], r["target"], r["stop_hits"], r["at_close"],
            r["avg_R_before_charges"], "{:,.0f}".format(r["gross_inr"]), "{:,.0f}".format(r["charges_inr"]),
            "{:,.0f}".format(r["net_inr"]), r["win_rate_net"]))
    return "\n".join(lines)


def main(argv):
    syms = [s.upper() for s in argv] or SYMBOLS
    os.makedirs(OUT, exist_ok=True)
    summary = {"run_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "risk_per_trade_inr": RISK_INR,
               "symbols": {}, "live": live_checks()}
    total = {}
    for i, sym in enumerate(syms):
        if i:
            time.sleep(1.5)                            # be polite to a free endpoint
        entry = {}
        try:
            text = tm.fetch_chart(sym)
            entry["sanity"], full = sanity(sym, text)
            entry["backtest"] = backtest(full)
            entry["pipeline"] = pipeline(sym, text, entry["sanity"]["last_day"]) if entry["sanity"]["last_day"] else None
            for r in entry["backtest"]:
                k = (r["or_minutes"], r["stop"], r["target_R"])
                t = total.setdefault(k, {"trades": 0, "net": 0.0, "charges": 0.0, "gross": 0.0, "wins": 0})
                t["trades"] += r["trades"]; t["net"] += r["net_inr"]; t["charges"] += r["charges_inr"]
                t["gross"] += r["gross_inr"]; t["wins"] += round((r["win_rate_net"] or 0) * r["trades"])
        except Exception as e:                           # report it, keep going
            entry["error"] = "%s: %s" % (type(e).__name__, e)
        summary["symbols"][sym] = entry
        print(sym, "error" if "error" in entry else "ok", entry.get("error", ""), flush=True)
    summary["backtest_total"] = [dict(or_minutes=k[0], stop=k[1], target_R=k[2], **{x: round(y, 2) for x, y in v.items()})
                                 for k, v in total.items()]
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2, default=str)

    md = ["# Real-data check", "", "Run %s. Yahoo 60-day 5-minute charts (unofficial, free), NSE files. "
          "Derived numbers only. Backtest: opening-range breakout, entry on the first 5-min close above the range, "
          "flat by 15:10, ₹%d risk a trade, charges at the pack's defaults. 60 in-sample days: a description of "
          "those days, not a forecast. Not financial advice." % (summary["run_at_utc"], RISK_INR), "",
          "## Live NSE checks", ""]
    for k, v in summary["live"].items():
        md.append("- **%s**: exit %s — %s" % (k, v["exit"], " / ".join(v["out"][:3])))
    md += ["", "## Data sanity", "", "| symbol | bars | sessions (full) | empty bars filled | first-last bar IST | short sessions | error |",
           "| --- | --- | --- | --- | --- | --- | --- |"]
    for s, e in summary["symbols"].items():
        z = e.get("sanity") or {}
        md.append("| %s | %s | %s (%s) | %s | %s-%s | %s | %s |" % (s, z.get("bars"), z.get("sessions"), z.get("full_sessions"), z.get("filled_bars"),
                  z.get("first_bar"), z.get("last_bar"), ", ".join(z.get("short_sessions") or []) or "-", e.get("error", "")))
    md += ["", "## Backtest, all symbols together", "",
           "| OR | stop | target | trades | gross ₹ | charges ₹ | net ₹ | net win rate |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in summary["backtest_total"]:
        md.append("| %dm | %s | %sR | %d | %s | %s | %s | %s |" % (r["or_minutes"], r["stop"], r["target_R"], r["trades"],
                  "{:,.0f}".format(r["gross"]), "{:,.0f}".format(r["charges"]), "{:,.0f}".format(r["net"]),
                  round(r["wins"] / r["trades"], 3) if r["trades"] else "-"))
    md += ["", "## Newest session through the pipeline (replayed at 10:15 IST)", ""]
    for s, e in summary["symbols"].items():
        p = e.get("pipeline")
        if not p:
            continue
        md.append("### %s" % s)
        for name, code, lines in p["steps"]:
            md.append("- %s (exit %s): %s" % (name, code, " / ".join(lines)))
        md.append("")
    md += ["## Backtest per symbol", ""]
    for s, e in summary["symbols"].items():
        if e.get("backtest"):
            md += ["### %s" % s, "", fmt_bt(e["backtest"]), ""]
    with open(os.path.join(OUT, "REPORT.md"), "w") as fh:
        fh.write("\n".join(md) + "\n")
    ok = sum(1 for e in summary["symbols"].values() if "error" not in e)
    print("done: %d of %d symbols; out/REPORT.md" % (ok, len(syms)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
