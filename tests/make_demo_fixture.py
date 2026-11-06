"""Builds tests/fixtures/charts/DEMO.json: SYNTHETIC 5-minute bars for a made-up
NSE symbol DEMO (Yahoo ticker DEMO.NS), 61 NSE sessions ending Fri 2026-11-06.
Not market data. The last session has an opening-range breakout at 9:45 IST
so the whole pipeline can be shown and tested offline.

    python3 tests/make_demo_fixture.py
"""
import datetime as dt, json, os, random

NSE_HOLIDAYS = {"2026-09-14", "2026-10-02", "2026-10-20"}  # the 2026 ones inside the window
IST = dt.timedelta(hours=5, minutes=30)


def sessions(last, n):
    d, out = last, []
    while len(out) < n:
        if d.weekday() < 5 and d.isoformat() not in NSE_HOLIDAYS:
            out.append(d)
        d -= dt.timedelta(days=1)
    return out[::-1]


def build(seed=7):
    rnd = random.Random(seed)
    days = sessions(dt.date(2026, 11, 6), 61)
    ts, o, h, l, c, v = [], [], [], [], [], []
    px = 1480.0
    for k, day in enumerate(days):
        last = k == len(days) - 1
        px *= 1 + rnd.gauss(0, 0.004)  # overnight gap
        for b in range(75):  # 9:15 .. 15:25 bar starts
            start = dt.datetime.combine(day, dt.time(9, 15)) + dt.timedelta(minutes=5 * b)
            op = px
            if last and b < 3:      # opening range: 1500 to 1510
                cl = [1504.0, 1508.5, 1503.0][b]; op = [1501.0, 1504.0, 1508.5][b]
                hi, lo = max(op, cl) + 1.5, min(op, cl) - 1.0
            elif last and b == 3:   # 9:30 bar stays inside
                op, cl, hi, lo = 1503.0, 1507.0, 1509.0, 1502.5
            elif last and b == 4:   # 9:35 bar closes above the range high (1510)
                op, cl, hi, lo = 1507.0, 1513.5, 1514.0, 1506.5
            else:
                cl = op * (1 + rnd.gauss(0.0001, 0.0018))
                hi = max(op, cl) * (1 + abs(rnd.gauss(0, 0.0008)))
                lo = min(op, cl) * (1 - abs(rnd.gauss(0, 0.0008)))
            px = cl
            ts.append(int((start - IST - dt.datetime(1970, 1, 1)).total_seconds()))
            o.append(round(op, 2)); h.append(round(hi, 2)); l.append(round(lo, 2)); c.append(round(cl, 2))
            v.append(int(rnd.uniform(40000, 120000) * (2.5 if b < 3 else 1)))
    meta = {"currency": "INR", "symbol": "DEMO.NS", "exchangeName": "NSI", "instrumentType": "EQUITY",
            "gmtoffset": 19800, "timezone": "IST", "exchangeTimezoneName": "Asia/Kolkata",
            "regularMarketPrice": c[-1], "chartPreviousClose": c[-76], "previousClose": c[-76],
            "dataGranularity": "5m", "range": "60d", "longName": "Demo Synthetic Ltd (not a real stock)"}
    return {"chart": {"result": [{"meta": meta, "timestamp": ts, "indicators": {"quote": [
        {"open": o, "high": h, "low": l, "close": c, "volume": v}]}}], "error": None}}


if __name__ == "__main__":
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "charts")
    os.makedirs(here, exist_ok=True)
    with open(os.path.join(here, "DEMO.json"), "w") as fh:
        json.dump(build(), fh)
    print("wrote tests/fixtures/charts/DEMO.json (synthetic)")
