# Real-data check

Run 2026-11-06T13:10:07Z. Yahoo 60-day 5-minute charts (unofficial, free), NSE files. Derived numbers only. Backtest: opening-range breakout, entry on the first 5-min close above the range, flat by 15:10, ₹500 risk a trade, charges at the pack's defaults. 60 in-sample days: a description of those days, not a forecast. Not financial advice.

## Live NSE checks

- **nse_universe**: exit 0 — NSE equity list: 2,630 rows. / Kept 2,390 NSE stocks in the EQ series (intraday-eligible by series). / Dropped: 207 series BE, 33 series BZ.
- **news**: exit 0 — items by source (7 days): {'NSE': 2} / notes: none

## Data sanity

| symbol | bars | sessions (full) | empty bars filled | first-last bar IST | short sessions | error |
| --- | --- | --- | --- | --- | --- | --- |
| RELIANCE | 4390 | 60 (60) | 110 | 09:15-15:25 | - |  |
| HDFCBANK | 4389 | 60 (60) | 111 | 09:15-15:25 | - |  |
| ICICIBANK | 4376 | 60 (60) | 124 | 09:15-15:25 | - |  |
| INFY | 4383 | 60 (60) | 117 | 09:15-15:25 | - |  |
| TCS | 4379 | 60 (59) | 117 | 09:15-15:25 | 2026-10-15:71 |  |
| SBIN | 4389 | 60 (60) | 111 | 09:15-15:25 | - |  |
| ITC | 4391 | 60 (60) | 109 | 09:15-15:25 | - |  |
| LT | 4377 | 60 (60) | 123 | 09:15-15:25 | - |  |
| AXISBANK | 4385 | 60 (59) | 111 | 09:15-15:25 | 2026-10-15:71 |  |
| KOTAKBANK | 4387 | 60 (60) | 113 | 09:15-15:25 | - |  |
| BHARTIARTL | 4379 | 60 (60) | 121 | 09:15-15:25 | - |  |
| HINDUNILVR | 4384 | 60 (60) | 116 | 09:15-15:25 | - |  |
| BAJFINANCE | 4388 | 60 (60) | 112 | 09:15-15:25 | - |  |
| MARUTI | 4379 | 60 (59) | 117 | 09:15-15:25 | 2026-10-15:71 |  |
| M&M | 4383 | 60 (60) | 117 | 09:15-15:25 | - |  |
| SUNPHARMA | 4379 | 60 (60) | 121 | 09:15-15:25 | - |  |
| TITAN | 4377 | 60 (60) | 123 | 09:15-15:25 | - |  |
| NTPC | 4384 | 60 (59) | 112 | 09:15-15:25 | 2026-10-15:71 |  |
| BAJAJ-AUTO | 4374 | 60 (60) | 126 | 09:15-15:25 | - |  |
| ULTRACEMCO | 4364 | 60 (59) | 132 | 09:15-15:25 | 2026-10-15:71 |  |

## Backtest, all symbols together

| OR | stop | target | trades | gross ₹ | charges ₹ | net ₹ (discount) | net ₹ (HDFC InvestRight) | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 681 | -7,253 | 57,966 | -65,220 | -125,359 | 0.467 |
| 15m | or_mid | 2.0R | 681 | -1,863 | 57,968 | -59,831 | -119,973 | 0.385 |
| 15m | or_low | 1.0R | 681 | -5,180 | 40,576 | -45,756 | -74,075 | 0.46 |
| 15m | or_low | 2.0R | 681 | -330 | 40,579 | -40,909 | -69,229 | 0.429 |
| 30m | or_mid | 1.0R | 628 | -7,312 | 50,378 | -57,690 | -105,652 | 0.455 |
| 30m | or_mid | 2.0R | 628 | -405 | 50,381 | -50,786 | -98,750 | 0.393 |
| 30m | or_low | 1.5R | 628 | -4,025 | 34,261 | -38,287 | -62,460 | 0.428 |

## Newest session through the pipeline (replayed at 10:15 IST)

### RELIANCE
- entry (exit 0): RELIANCE  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹1306.00, low ₹1295.60 (3 of 3 bars). / TRIGGERED 9:50 AM at ₹1311.90: the 9:45 bar (bar 6) closed above the range high ₹1306.00 (+0.45%).
- exit (exit 0): Exit plan: RELIANCE long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹1,311.90 at 9:50 AM (bar 6) /   Stop          ₹1,300.80  opening-range midpoint: (₹1,306.00 + ₹1,295.60) / 2 = ₹1300.8 /   Target        ₹1,334.10  2R (two times the risk) /   Risk a share  ₹11.10 (0.85% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): RELIANCE buy, Friday 2026-11-06: entry 1311.90 at 9:50 AM (bar 6), stop 1300.80, target 1334.10 (2R, risk 11.10 a share). / 10,000 replays of the rest of the session, 9:50 AM to 3:10 PM (64 five-minute bars), seed 19. / Each bar is drawn whole from RELIANCE's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   4.8 % /   stop first     37.0 %
- budget (exit 0): RELIANCE buy, opening-range breakout, entry 1311.90 at 9:50 AM / Stop 1300.80: opening-range midpoint. Target 1334.10: 2R (two times the risk). / Sized at 1311.90 (the plan's entry). Risk 11.10 a share (entry 1311.90 minus stop 1300.80). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 11.10 risk a share                          45 shares
- risk (exit 0): PASS  #1 buy RELIANCE 30 shares, entry /           entry 1311.90 (the plan's entry), stop 1300.80, target 1334.10: risk 11.10 a share /           max loss ₹374.62 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹60,643 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 30 RELIANCE, market, good for today /   stop-loss 1300.80 /   take-profit 1334.10 /   max loss about ₹374.62 if the stop fills at 1300.80 (it can fill worse in a fast market) /   why: opening-range breakout on RELIANCE: 30 shares, bound by your max order (30 x 11.10 + charges = ₹374.62 at the stop)

### HDFCBANK
- entry (exit 0): HDFCBANK  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹767.40, low ₹754.65 (3 of 3 bars). / TRIGGERED 9:35 AM at ₹767.65: the 9:30 bar (bar 3) closed above the range high ₹767.40 (+0.03%).
- exit (exit 0): Exit plan: HDFCBANK long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹767.65 at 9:35 AM (bar 3) /   Stop          ₹761.02  opening-range midpoint: (₹767.40 + ₹754.65) / 2 = ₹761.025, rounded down /   Target        ₹780.91  2R (two times the risk) /   Risk a share  ₹6.63 (0.86% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): HDFCBANK buy, Friday 2026-11-06: entry 767.65 at 9:35 AM (bar 3), stop 761.02, target 780.91 (2R, risk 6.63 a share). / 10,000 replays of the rest of the session, 9:35 AM to 3:10 PM (67 five-minute bars), seed 19. / Each bar is drawn whole from HDFCBANK's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   5.3 % /   stop first     35.1 %
- budget (exit 0): HDFCBANK buy, opening-range breakout, entry 767.65 at 9:35 AM / Stop 761.02: opening-range midpoint. Target 780.91: 2R (two times the risk). / Sized at 767.65 (the plan's entry). Risk 6.63 a share (entry 767.65 minus stop 761.02). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 6.63 risk a share                           75 shares
- risk (exit 0): PASS  #1 buy HDFCBANK 52 shares, entry /           entry 767.65 (the plan's entry), stop 761.02, target 780.91: risk 6.63 a share /           max loss ₹386.96 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹60,082.20 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 52 HDFCBANK, market, good for today /   stop-loss 761.02 /   take-profit 780.91 /   max loss about ₹386.96 if the stop fills at 761.02 (it can fill worse in a fast market) /   why: opening-range breakout on HDFCBANK: 52 shares, bound by your max order (52 x 6.63 + charges = ₹386.96 at the stop)

### ICICIBANK
- entry (exit 0): ICICIBANK  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹1518.10, low ₹1505.00 (3 of 3 bars). / TRIGGERED 9:50 AM at ₹1518.80: the 9:45 bar (bar 6) closed above the range high ₹1518.10 (+0.05%).
- exit (exit 0): Exit plan: ICICIBANK long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹1,518.80 at 9:50 AM (bar 6) /   Stop          ₹1,511.55  opening-range midpoint: (₹1,518.10 + ₹1,505.00) / 2 = ₹1511.55 /   Target        ₹1,533.30  2R (two times the risk) /   Risk a share  ₹7.25 (0.48% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): ICICIBANK buy, Friday 2026-11-06: entry 1518.80 at 9:50 AM (bar 6), stop 1511.55, target 1533.30 (2R, risk 7.25 a share). / 10,000 replays of the rest of the session, 9:50 AM to 3:10 PM (64 five-minute bars), seed 19. / Each bar is drawn whole from ICICIBANK's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   20.1 % /   stop first     56.0 %
- budget (exit 0): ICICIBANK buy, opening-range breakout, entry 1518.80 at 9:50 AM / Stop 1511.55: opening-range midpoint. Target 1533.30: 2R (two times the risk). / Sized at 1518.80 (the plan's entry). Risk 7.25 a share (entry 1518.80 minus stop 1511.55). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 7.25 risk a share                           68 shares
- risk (exit 0): PASS  #1 buy ICICIBANK 26 shares, entry /           entry 1518.80 (the plan's entry), stop 1511.55, target 1533.30: risk 7.25 a share /           max loss ₹230.35 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹60,511.20 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 26 ICICIBANK, market, good for today /   stop-loss 1511.55 /   take-profit 1533.30 /   max loss about ₹230.35 if the stop fills at 1511.55 (it can fill worse in a fast market) /   why: opening-range breakout on ICICIBANK: 26 shares, bound by your max order (26 x 7.25 + charges = ₹230.35 at the stop)

### INFY
- entry (exit 1): INFY  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹1198.80, low ₹1179.00 (3 of 3 bars). / WAITING  last close ₹1185.00 (10:10 bar), ₹13.80 under the range high ₹1198.80 (-1.15%).

### TCS
- entry (exit 1): TCS  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹2564.60, low ₹2519.80 (3 of 3 bars). / WAITING  last close ₹2537.40 (10:10 bar), ₹27.20 under the range high ₹2564.60 (-1.06%).

### SBIN
- entry (exit 0): SBIN  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹999.30, low ₹991.55 (3 of 3 bars). / TRIGGERED 9:50 AM at ₹1000.50: the 9:45 bar (bar 6) closed above the range high ₹999.30 (+0.12%).
- exit (exit 0): Exit plan: SBIN long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹1,000.50 at 9:50 AM (bar 6) /   Stop          ₹995.42  opening-range midpoint: (₹999.30 + ₹991.55) / 2 = ₹995.425, rounded down /   Target        ₹1,010.66  2R (two times the risk) /   Risk a share  ₹5.08 (0.51% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): SBIN buy, Friday 2026-11-06: entry 1000.50 at 9:50 AM (bar 6), stop 995.42, target 1010.66 (2R, risk 5.08 a share). / 10,000 replays of the rest of the session, 9:50 AM to 3:10 PM (64 five-minute bars), seed 19. / Each bar is drawn whole from SBIN's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   15.2 % /   stop first     65.0 %
- budget (exit 0): SBIN buy, opening-range breakout, entry 1000.50 at 9:50 AM / Stop 995.42: opening-range midpoint. Target 1010.66: 2R (two times the risk). / Sized at 1000.50 (the plan's entry). Risk 5.08 a share (entry 1000.50 minus stop 995.42). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 5.08 risk a share                           98 shares
- risk (exit 0): PASS  #1 buy SBIN 39 shares, entry /           entry 1000.50 (the plan's entry), stop 995.42, target 1010.66: risk 5.08 a share /           max loss ₹239.46 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹60,980.50 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 39 SBIN, market, good for today /   stop-loss 995.42 /   take-profit 1010.66 /   max loss about ₹239.46 if the stop fills at 995.42 (it can fill worse in a fast market) /   why: opening-range breakout on SBIN: 39 shares, bound by your max order (39 x 5.08 + charges = ₹239.46 at the stop)

### ITC
- entry (exit 0): ITC  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹278.60, low ₹275.95 (3 of 3 bars). / TRIGGERED 9:45 AM at ₹279.35: the 9:40 bar (bar 5) closed above the range high ₹278.60 (+0.27%).
- exit (exit 0): Exit plan: ITC long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹279.35 at 9:45 AM (bar 5) /   Stop          ₹277.27  opening-range midpoint: (₹278.60 + ₹275.95) / 2 = ₹277.275, rounded down /   Target        ₹283.51  2R (two times the risk) /   Risk a share  ₹2.08 (0.74% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): ITC buy, Friday 2026-11-06: entry 279.35 at 9:45 AM (bar 5), stop 277.27, target 283.51 (2R, risk 2.08 a share). / 10,000 replays of the rest of the session, 9:45 AM to 3:10 PM (65 five-minute bars), seed 19. / Each bar is drawn whole from ITC's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   10.2 % /   stop first     45.4 %
- budget (exit 0): ITC buy, opening-range breakout, entry 279.35 at 9:45 AM / Stop 277.27: opening-range midpoint. Target 283.51: 2R (two times the risk). / Sized at 279.35 (the plan's entry). Risk 2.08 a share (entry 279.35 minus stop 277.27). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 2.08 risk a share                          240 shares
- risk (exit 0): PASS  #1 buy ITC 143 shares, entry /           entry 279.35 (the plan's entry), stop 277.27, target 283.51: risk 2.08 a share /           max loss ₹339.71 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹60,052.95 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 143 ITC, market, good for today /   stop-loss 277.27 /   take-profit 283.51 /   max loss about ₹339.71 if the stop fills at 277.27 (it can fill worse in a fast market) /   why: opening-range breakout on ITC: 143 shares, bound by your max order (143 x 2.08 + charges = ₹339.71 at the stop)

### LT
- entry (exit 1): LT  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹4049.00, low ₹3997.10 (3 of 3 bars). / WAITING  last close ₹4032.60 (10:10 bar), ₹16.40 under the range high ₹4049.00 (-0.41%).

### AXISBANK
- entry (exit 0): AXISBANK  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹1285.20, low ₹1276.20 (3 of 3 bars). / TRIGGERED 9:50 AM at ₹1285.80: the 9:45 bar (bar 6) closed above the range high ₹1285.20 (+0.05%).
- exit (exit 0): Exit plan: AXISBANK long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹1,285.80 at 9:50 AM (bar 6) /   Stop          ₹1,280.70  opening-range midpoint: (₹1,285.20 + ₹1,276.20) / 2 = ₹1280.7 /   Target        ₹1,296.00  2R (two times the risk) /   Risk a share  ₹5.10 (0.40% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): AXISBANK buy, Friday 2026-11-06: entry 1285.80 at 9:50 AM (bar 6), stop 1280.70, target 1296.00 (2R, risk 5.10 a share). / 10,000 replays of the rest of the session, 9:50 AM to 3:10 PM (64 five-minute bars), seed 19. / Each bar is drawn whole from AXISBANK's own 5-min bars at the same time of day (+-2 bars) over its last 58 full sessions (2026-08-12 to 2026-11-05). /  /   target first   33.3 % /   stop first     60.1 %
- budget (exit 0): AXISBANK buy, opening-range breakout, entry 1285.80 at 9:50 AM / Stop 1280.70: opening-range midpoint. Target 1296.00: 2R (two times the risk). / Sized at 1285.80 (the plan's entry). Risk 5.10 a share (entry 1285.80 minus stop 1280.70). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 5.10 risk a share                           98 shares
- risk (exit 0): PASS  #1 buy AXISBANK 31 shares, entry /           entry 1285.80 (the plan's entry), stop 1280.70, target 1296.00: risk 5.10 a share /           max loss ₹200.36 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹60,140.20 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 31 AXISBANK, market, good for today /   stop-loss 1280.70 /   take-profit 1296.00 /   max loss about ₹200.36 if the stop fills at 1280.70 (it can fill worse in a fast market) /   why: opening-range breakout on AXISBANK: 31 shares, bound by your max order (31 x 5.10 + charges = ₹200.36 at the stop)

### KOTAKBANK
- entry (exit 0): KOTAKBANK  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹469.65, low ₹463.00 (3 of 3 bars). / TRIGGERED 9:55 AM at ₹470.60: the 9:50 bar (bar 7) closed above the range high ₹469.65 (+0.20%).
- exit (exit 0): Exit plan: KOTAKBANK long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹470.60 at 9:55 AM (bar 7) /   Stop          ₹466.32  opening-range midpoint: (₹469.65 + ₹463.00) / 2 = ₹466.325, rounded down /   Target        ₹479.16  2R (two times the risk) /   Risk a share  ₹4.28 (0.91% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): KOTAKBANK buy, Friday 2026-11-06: entry 470.60 at 9:55 AM (bar 7), stop 466.32, target 479.16 (2R, risk 4.28 a share). / 10,000 replays of the rest of the session, 9:55 AM to 3:10 PM (63 five-minute bars), seed 19. / Each bar is drawn whole from KOTAKBANK's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   7.1 % /   stop first     28.8 %
- budget (exit 0): KOTAKBANK buy, opening-range breakout, entry 470.60 at 9:55 AM / Stop 466.32: opening-range midpoint. Target 479.16: 2R (two times the risk). / Sized at 470.60 (the plan's entry). Risk 4.28 a share (entry 470.60 minus stop 466.32). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 4.28 risk a share                          116 shares
- risk (exit 0): PASS  #1 buy KOTAKBANK 84 shares, entry /           entry 470.60 (the plan's entry), stop 466.32, target 479.16: risk 4.28 a share /           max loss ₹401.30 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹60,469.60 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 84 KOTAKBANK, market, good for today /   stop-loss 466.32 /   take-profit 479.16 /   max loss about ₹401.30 if the stop fills at 466.32 (it can fill worse in a fast market) /   why: opening-range breakout on KOTAKBANK: 84 shares, bound by your max order (84 x 4.28 + charges = ₹401.30 at the stop)

### BHARTIARTL
- entry (exit 1): BHARTIARTL  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹2101.60, low ₹2078.40 (3 of 3 bars). / WAITING  last close ₹2076.40 (10:10 bar), ₹25.20 under the range high ₹2101.60 (-1.20%).

### HINDUNILVR
- entry (exit 0): HINDUNILVR  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹1973.90, low ₹1954.40 (3 of 3 bars). / TRIGGERED 9:50 AM at ₹1976.20: the 9:45 bar (bar 6) closed above the range high ₹1973.90 (+0.12%).
- exit (exit 0): Exit plan: HINDUNILVR long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹1,976.20 at 9:50 AM (bar 6) /   Stop          ₹1,964.15  opening-range midpoint: (₹1,973.90 + ₹1,954.40) / 2 = ₹1964.15 /   Target        ₹2,000.30  2R (two times the risk) /   Risk a share  ₹12.05 (0.61% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): HINDUNILVR buy, Friday 2026-11-06: entry 1976.20 at 9:50 AM (bar 6), stop 1964.15, target 2000.30 (2R, risk 12.05 a share). / 10,000 replays of the rest of the session, 9:50 AM to 3:10 PM (64 five-minute bars), seed 19. / Each bar is drawn whole from HINDUNILVR's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   15.1 % /   stop first     51.3 %
- budget (exit 0): HINDUNILVR buy, opening-range breakout, entry 1976.20 at 9:50 AM / Stop 1964.15: opening-range midpoint. Target 2000.30: 2R (two times the risk). / Sized at 1976.20 (the plan's entry). Risk 12.05 a share (entry 1976.20 minus stop 1964.15). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 12.05 risk a share                          41 shares
- risk (exit 0): PASS  #1 buy HINDUNILVR 20 shares, entry /           entry 1976.20 (the plan's entry), stop 1964.15, target 2000.30: risk 12.05 a share /           max loss ₹282.85 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹60,476 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 20 HINDUNILVR, market, good for today /   stop-loss 1964.15 /   take-profit 2000.30 /   max loss about ₹282.85 if the stop fills at 1964.15 (it can fill worse in a fast market) /   why: opening-range breakout on HINDUNILVR: 20 shares, bound by your max order (20 x 12.05 + charges = ₹282.85 at the stop)

### BAJFINANCE
- entry (exit 0): BAJFINANCE  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹1051.85, low ₹1045.00 (3 of 3 bars). / TRIGGERED 9:50 AM at ₹1053.35: the 9:45 bar (bar 6) closed above the range high ₹1051.85 (+0.14%).
- exit (exit 0): Exit plan: BAJFINANCE long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹1,053.35 at 9:50 AM (bar 6) /   Stop          ₹1,048.42  opening-range midpoint: (₹1,051.85 + ₹1,045.00) / 2 = ₹1048.425, rounded down /   Target        ₹1,063.21  2R (two times the risk) /   Risk a share  ₹4.93 (0.47% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): BAJFINANCE buy, Friday 2026-11-06: entry 1053.35 at 9:50 AM (bar 6), stop 1048.42, target 1063.21 (2R, risk 4.93 a share). / 10,000 replays of the rest of the session, 9:50 AM to 3:10 PM (64 five-minute bars), seed 19. / Each bar is drawn whole from BAJFINANCE's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   28.7 % /   stop first     63.8 %
- budget (exit 0): BAJFINANCE buy, opening-range breakout, entry 1053.35 at 9:50 AM / Stop 1048.42: opening-range midpoint. Target 1063.21: 2R (two times the risk). / Sized at 1053.35 (the plan's entry). Risk 4.93 a share (entry 1053.35 minus stop 1048.42). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 4.93 risk a share                          101 shares
- risk (exit 0): PASS  #1 buy BAJFINANCE 37 shares, entry /           entry 1053.35 (the plan's entry), stop 1048.42, target 1063.21: risk 4.93 a share /           max loss ₹223.71 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹61,026.05 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 37 BAJFINANCE, market, good for today /   stop-loss 1048.42 /   take-profit 1063.21 /   max loss about ₹223.71 if the stop fills at 1048.42 (it can fill worse in a fast market) /   why: opening-range breakout on BAJFINANCE: 37 shares, bound by your max order (37 x 4.93 + charges = ₹223.71 at the stop)

### MARUTI
- entry (exit 0): MARUTI  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹12637.00, low ₹12453.00 (3 of 3 bars). / TRIGGERED 9:50 AM at ₹12670.00: the 9:45 bar (bar 6) closed above the range high ₹12637.00 (+0.26%).
- exit (exit 0): Exit plan: MARUTI long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹12,670.00 at 9:50 AM (bar 6) /   Stop          ₹12,545.00  opening-range midpoint: (₹12,637.00 + ₹12,453.00) / 2 = ₹12545 /   Target        ₹12,920.00  2R (two times the risk) /   Risk a share  ₹125.00 (0.99% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): MARUTI buy, Friday 2026-11-06: entry 12670.00 at 9:50 AM (bar 6), stop 12545.00, target 12920.00 (2R, risk 125.00 a share). / 10,000 replays of the rest of the session, 9:50 AM to 3:10 PM (64 five-minute bars), seed 19. / Each bar is drawn whole from MARUTI's own 5-min bars at the same time of day (+-2 bars) over its last 58 full sessions (2026-08-12 to 2026-11-05). /  /   target first   2.4 % /   stop first     39.7 %
- budget (exit 0): MARUTI buy, opening-range breakout, entry 12670.00 at 9:50 AM / Stop 12545.00: opening-range midpoint. Target 12920.00: 2R (two times the risk). / Sized at 12670.00 (the plan's entry). Risk 125.00 a share (entry 12670.00 minus stop 12545.00). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 125.00 risk a share                          4 shares
- risk (exit 0): PASS  #1 buy MARUTI 3 shares, entry /           entry 12670.00 (the plan's entry), stop 12545.00, target 12920.00: risk 125.00 a share /           max loss ₹415.16 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹61,990 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 3 MARUTI, market, good for today /   stop-loss 12545.00 /   take-profit 12920.00 /   max loss about ₹415.16 if the stop fills at 12545.00 (it can fill worse in a fast market) /   why: opening-range breakout on MARUTI: 3 shares, bound by your max order (3 x 125.00 + charges = ₹415.16 at the stop)

### M&M
- entry (exit 0): M&M  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹3226.50, low ₹3133.90 (3 of 3 bars). / TRIGGERED 9:35 AM at ₹3241.90: the 9:30 bar (bar 3) closed above the range high ₹3226.50 (+0.48%).
- exit (exit 0): Exit plan: M&M long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹3,241.90 at 9:35 AM (bar 3) /   Stop          ₹3,180.20  opening-range midpoint: (₹3,226.50 + ₹3,133.90) / 2 = ₹3180.2 /   Target        ₹3,365.30  2R (two times the risk) /   Risk a share  ₹61.70 (1.90% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): M&M buy, Friday 2026-11-06: entry 3241.90 at 9:35 AM (bar 3), stop 3180.20, target 3365.30 (2R, risk 61.70 a share). / 10,000 replays of the rest of the session, 9:35 AM to 3:10 PM (67 five-minute bars), seed 19. / Each bar is drawn whole from M&M's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   0.2 % /   stop first     6.8 %
- budget (exit 0): M&M buy, opening-range breakout, entry 3241.90 at 9:35 AM / Stop 3180.20: opening-range midpoint. Target 3365.30: 2R (two times the risk). / Sized at 3241.90 (the plan's entry). Risk 61.70 a share (entry 3241.90 minus stop 3180.20). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 61.70 risk a share                           8 shares  <- binds
- risk (exit 0): PASS  #1 buy M&M 7 shares, entry /           entry 3241.90 (the plan's entry), stop 3180.20, target 3365.30: risk 61.70 a share /           max loss ₹455.74 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹77,306.70 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 7 M&M, market, good for today /   stop-loss 3180.20 /   take-profit 3365.30 /   max loss about ₹455.74 if the stop fills at 3180.20 (it can fill worse in a fast market) /   why: opening-range breakout on M&M: 7 shares, bound by your ₹500 max loss per trade (7 x 61.70 + charges = ₹455.74 at the stop)

### SUNPHARMA
- entry (exit 0): SUNPHARMA  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹1839.90, low ₹1815.00 (3 of 3 bars). / TRIGGERED 9:40 AM at ₹1845.60: the 9:35 bar (bar 4) closed above the range high ₹1839.90 (+0.31%).
- exit (exit 0): Exit plan: SUNPHARMA long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹1,845.60 at 9:40 AM (bar 4) /   Stop          ₹1,827.45  opening-range midpoint: (₹1,839.90 + ₹1,815.00) / 2 = ₹1827.45 /   Target        ₹1,881.90  2R (two times the risk) /   Risk a share  ₹18.15 (0.98% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): SUNPHARMA buy, Friday 2026-11-06: entry 1845.60 at 9:40 AM (bar 4), stop 1827.45, target 1881.90 (2R, risk 18.15 a share). / 10,000 replays of the rest of the session, 9:40 AM to 3:10 PM (66 five-minute bars), seed 19. / Each bar is drawn whole from SUNPHARMA's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   4.2 % /   stop first     33.8 %
- budget (exit 0): SUNPHARMA buy, opening-range breakout, entry 1845.60 at 9:40 AM / Stop 1827.45: opening-range midpoint. Target 1881.90: 2R (two times the risk). / Sized at 1845.60 (the plan's entry). Risk 18.15 a share (entry 1845.60 minus stop 1827.45). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 18.15 risk a share                          27 shares
- risk (exit 0): PASS  #1 buy SUNPHARMA 21 shares, entry /           entry 1845.60 (the plan's entry), stop 1827.45, target 1881.90: risk 18.15 a share /           max loss ₹422.10 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹61,242.40 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 21 SUNPHARMA, market, good for today /   stop-loss 1827.45 /   take-profit 1881.90 /   max loss about ₹422.10 if the stop fills at 1827.45 (it can fill worse in a fast market) /   why: opening-range breakout on SUNPHARMA: 21 shares, bound by your max order (21 x 18.15 + charges = ₹422.10 at the stop)

### TITAN
- entry (exit 0): TITAN  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹4930.00, low ₹4696.70 (3 of 3 bars). / TRIGGERED 9:35 AM at ₹4945.10: the 9:30 bar (bar 3) closed above the range high ₹4930.00 (+0.31%).
- exit (exit 0): Exit plan: TITAN long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹4,945.10 at 9:35 AM (bar 3) /   Stop          ₹4,813.35  opening-range midpoint: (₹4,930.00 + ₹4,696.70) / 2 = ₹4813.35 /   Target        ₹5,208.60  2R (two times the risk) /   Risk a share  ₹131.75 (2.66% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): TITAN buy, Friday 2026-11-06: entry 4945.10 at 9:35 AM (bar 3), stop 4813.35, target 5208.60 (2R, risk 131.75 a share). / 10,000 replays of the rest of the session, 9:35 AM to 3:10 PM (67 five-minute bars), seed 19. / Each bar is drawn whole from TITAN's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   0.0 % /   stop first     0.3 %
- budget (exit 0): TITAN buy, opening-range breakout, entry 4945.10 at 9:35 AM / Stop 4813.35: opening-range midpoint. Target 5208.60: 2R (two times the risk). / Sized at 4945.10 (the plan's entry). Risk 131.75 a share (entry 4945.10 minus stop 4813.35). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 131.75 risk a share                          3 shares  <- binds
- risk (exit 0): PASS  #1 buy TITAN 3 shares, entry /           entry 4945.10 (the plan's entry), stop 4813.35, target 5208.60: risk 131.75 a share /           max loss ₹410.76 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹85,164.70 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 3 TITAN, market, good for today /   stop-loss 4813.35 /   take-profit 5208.60 /   max loss about ₹410.76 if the stop fills at 4813.35 (it can fill worse in a fast market) /   why: opening-range breakout on TITAN: 3 shares, bound by your ₹500 max loss per trade (3 x 131.75 + charges = ₹410.76 at the stop)

### NTPC
- entry (exit 0): NTPC  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹312.75, low ₹309.25 (3 of 3 bars). / TRIGGERED 9:50 AM at ₹314.55: the 9:45 bar (bar 6) closed above the range high ₹312.75 (+0.58%).
- exit (exit 0): Exit plan: NTPC long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹314.55 at 9:50 AM (bar 6) /   Stop          ₹311.00  opening-range midpoint: (₹312.75 + ₹309.25) / 2 = ₹311 /   Target        ₹321.65  2R (two times the risk) /   Risk a share  ₹3.55 (1.13% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): NTPC buy, Friday 2026-11-06: entry 314.55 at 9:50 AM (bar 6), stop 311.00, target 321.65 (2R, risk 3.55 a share). / 10,000 replays of the rest of the session, 9:50 AM to 3:10 PM (64 five-minute bars), seed 19. / Each bar is drawn whole from NTPC's own 5-min bars at the same time of day (+-2 bars) over its last 58 full sessions (2026-08-12 to 2026-11-05). /  /   target first   1.9 % /   stop first     27.2 %
- budget (exit 0): NTPC buy, opening-range breakout, entry 314.55 at 9:50 AM / Stop 311.00: opening-range midpoint. Target 321.65: 2R (two times the risk). / Sized at 314.55 (the plan's entry). Risk 3.55 a share (entry 314.55 minus stop 311.00). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 3.55 risk a share                          140 shares
- risk (exit 0): PASS  #1 buy NTPC 127 shares, entry /           entry 314.55 (the plan's entry), stop 311.00, target 321.65: risk 3.55 a share /           max loss ₹493.02 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹60,052.15 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 127 NTPC, market, good for today /   stop-loss 311.00 /   take-profit 321.65 /   max loss about ₹493.02 if the stop fills at 311.00 (it can fill worse in a fast market) /   why: opening-range breakout on NTPC: 127 shares, bound by your max order (127 x 3.55 + charges = ₹493.02 at the stop)

### BAJAJ-AUTO
- entry (exit 0): BAJAJ-AUTO  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹10740.00, low ₹10618.00 (3 of 3 bars). / TRIGGERED 9:45 AM at ₹10768.00: the 9:40 bar (bar 5) closed above the range high ₹10740.00 (+0.26%).
- exit (exit 0): Exit plan: BAJAJ-AUTO long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹10,768.00 at 9:45 AM (bar 5) /   Stop          ₹10,679.00  opening-range midpoint: (₹10,740.00 + ₹10,618.00) / 2 = ₹10679 /   Target        ₹10,946.00  2R (two times the risk) /   Risk a share  ₹89.00 (0.83% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): BAJAJ-AUTO buy, Friday 2026-11-06: entry 10768.00 at 9:45 AM (bar 5), stop 10679.00, target 10946.00 (2R, risk 89.00 a share). / 10,000 replays of the rest of the session, 9:45 AM to 3:10 PM (65 five-minute bars), seed 19. / Each bar is drawn whole from BAJAJ-AUTO's own 5-min bars at the same time of day (+-2 bars) over its last 59 full sessions (2026-08-12 to 2026-11-05). /  /   target first   9.9 % /   stop first     44.2 %
- budget (exit 0): BAJAJ-AUTO buy, opening-range breakout, entry 10768.00 at 9:45 AM / Stop 10679.00: opening-range midpoint. Target 10946.00: 2R (two times the risk). / Sized at 10768.00 (the plan's entry). Risk 89.00 a share (entry 10768.00 minus stop 10679.00). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 89.00 risk a share                           5 shares
- risk (exit 0): PASS  #1 buy BAJAJ-AUTO 3 shares, entry /           entry 10768.00 (the plan's entry), stop 10679.00, target 10946.00: risk 89.00 a share /           max loss ₹301.16 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹67,696 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 3 BAJAJ-AUTO, market, good for today /   stop-loss 10679.00 /   take-profit 10946.00 /   max loss about ₹301.16 if the stop fills at 10679.00 (it can fill worse in a fast market) /   why: opening-range breakout on BAJAJ-AUTO: 3 shares, bound by your max order (3 x 89.00 + charges = ₹301.16 at the stop)

### ULTRACEMCO
- entry (exit 0): ULTRACEMCO  Fri 2026-11-06 10:15 IST  opening-range breakout (15-minute range) on 5-minute bars (Yahoo, free, can lag) / Opening range 9:15-9:30: high ₹12250.00, low ₹12103.00 (3 of 3 bars). / TRIGGERED 9:50 AM at ₹12253.00: the 9:45 bar (bar 6) closed above the range high ₹12250.00 (+0.02%).
- exit (exit 0): Exit plan: ULTRACEMCO long, Fri 2026-11-06, opening-range breakout on 5-minute bars /   Entry         ₹12,253.00 at 9:50 AM (bar 6) /   Stop          ₹12,176.50  opening-range midpoint: (₹12,250.00 + ₹12,103.00) / 2 = ₹12176.5 /   Target        ₹12,406.00  2R (two times the risk) /   Risk a share  ₹76.50 (0.62% of the entry) /   Reward:risk   2.0
- timemachine (exit 0): ULTRACEMCO buy, Friday 2026-11-06: entry 12253.00 at 9:50 AM (bar 6), stop 12176.50, target 12406.00 (2R, risk 76.50 a share). / 10,000 replays of the rest of the session, 9:50 AM to 3:10 PM (64 five-minute bars), seed 19. / Each bar is drawn whole from ULTRACEMCO's own 5-min bars at the same time of day (+-2 bars) over its last 58 full sessions (2026-08-12 to 2026-11-05). /  /   target first   18.9 % /   stop first     48.0 %
- budget (exit 0): ULTRACEMCO buy, opening-range breakout, entry 12253.00 at 9:50 AM / Stop 12176.50: opening-range midpoint. Target 12406.00: 2R (two times the risk). / Sized at 12253.00 (the plan's entry). Risk 76.50 a share (entry 12253.00 minus stop 12176.50). Reward:risk 2.00. /  / Limits (whole shares; the smallest one wins): /   max loss      ₹500 max loss / 76.50 risk a share                           6 shares
- risk (exit 0): PASS  #1 buy ULTRACEMCO 3 shares, entry /           entry 12253.00 (the plan's entry), stop 12176.50, target 12406.00: risk 76.50 a share /           max loss ₹268.42 (limit ₹500), reward:risk 2.00 (min 1) /           today before this: 0 of 3 trades, ₹0 of ₹1,500 daily loss /  / 1 passed, 0 blocked at 2026-11-06 10:15 India (IST). Cash after the passed orders: ₹63,241 (dry run account).
- ticket (exit 0): ORDER 1 of 1, DRY RUN (you place it yourself), Upstox (upstox-skill from the upstox/upstox-plugin-marketplace) /   BUY 3 ULTRACEMCO, market, good for today /   stop-loss 12176.50 /   take-profit 12406.00 /   max loss about ₹268.42 if the stop fills at 12176.50 (it can fill worse in a fast market) /   why: opening-range breakout on ULTRACEMCO: 3 shares, bound by your max order (3 x 76.50 + charges = ₹268.42 at the stop)

## Backtest per symbol

### RELIANCE

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 30 | 14/10/6 | 0.083 | 1,245 | 2,701 | -1,456 | 0.5 |
| 15m | or_mid | 2.0R | 30 | 8/12/10 | 0.172 | 2,584 | 2,701 | -118 | 0.433 |
| 15m | or_low | 1.0R | 30 | 9/9/12 | 0.002 | 39 | 1,884 | -1,845 | 0.467 |
| 15m | or_low | 2.0R | 30 | 5/9/16 | 0.123 | 1,841 | 1,884 | -44 | 0.4 |
| 30m | or_mid | 1.0R | 28 | 12/8/8 | 0.086 | 1,204 | 2,360 | -1,156 | 0.464 |
| 30m | or_mid | 2.0R | 28 | 5/10/13 | 0.122 | 1,716 | 2,360 | -644 | 0.393 |
| 30m | or_low | 1.5R | 28 | 3/7/18 | -0.021 | -294 | 1,584 | -1,878 | 0.393 |

### HDFCBANK

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 39 | 19/15/5 | 0.107 | 2,075 | 3,553 | -1,478 | 0.538 |
| 15m | or_mid | 2.0R | 39 | 8/17/14 | 0.1 | 1,930 | 3,553 | -1,624 | 0.41 |
| 15m | or_low | 1.0R | 39 | 12/9/18 | 0.056 | 1,083 | 2,556 | -1,473 | 0.487 |
| 15m | or_low | 2.0R | 39 | 2/9/28 | 0.024 | 452 | 2,555 | -2,103 | 0.462 |
| 30m | or_mid | 1.0R | 35 | 15/14/6 | 0.013 | 220 | 2,947 | -2,727 | 0.486 |
| 30m | or_mid | 2.0R | 35 | 4/15/16 | -0.045 | -792 | 2,947 | -3,739 | 0.4 |
| 30m | or_low | 1.5R | 35 | 4/5/26 | 0.071 | 1,230 | 2,075 | -845 | 0.514 |

### ICICIBANK

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 40 | 17/19/4 | -0.047 | -936 | 3,690 | -4,626 | 0.45 |
| 15m | or_mid | 2.0R | 40 | 11/20/9 | 0.088 | 1,739 | 3,690 | -1,951 | 0.375 |
| 15m | or_low | 1.0R | 40 | 13/13/14 | -0.012 | -221 | 2,640 | -2,861 | 0.45 |
| 15m | or_low | 2.0R | 40 | 3/13/24 | 0.088 | 1,768 | 2,641 | -873 | 0.45 |
| 30m | or_mid | 1.0R | 33 | 15/11/7 | 0.139 | 2,285 | 3,018 | -733 | 0.515 |
| 30m | or_mid | 2.0R | 33 | 9/11/13 | 0.359 | 5,887 | 3,019 | 2,868 | 0.485 |
| 30m | or_low | 1.5R | 33 | 5/5/23 | 0.208 | 3,392 | 2,065 | 1,327 | 0.485 |

### INFY

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 22 | 6/9/7 | -0.175 | -1,925 | 1,463 | -3,388 | 0.364 |
| 15m | or_mid | 2.0R | 22 | 1/10/11 | -0.334 | -3,666 | 1,462 | -5,128 | 0.273 |
| 15m | or_low | 1.0R | 22 | 1/3/18 | -0.136 | -1,493 | 888 | -2,381 | 0.364 |
| 15m | or_low | 2.0R | 22 | 0/3/19 | -0.121 | -1,331 | 888 | -2,219 | 0.364 |
| 30m | or_mid | 1.0R | 20 | 3/7/10 | -0.276 | -2,723 | 1,155 | -3,878 | 0.3 |
| 30m | or_mid | 2.0R | 20 | 1/7/12 | -0.233 | -2,293 | 1,155 | -3,448 | 0.3 |
| 30m | or_low | 1.5R | 20 | 0/2/18 | -0.129 | -1,285 | 680 | -1,965 | 0.35 |

### TCS

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 26 | 6/11/9 | -0.179 | -2,280 | 1,658 | -3,938 | 0.385 |
| 15m | or_mid | 2.0R | 26 | 2/12/12 | -0.24 | -3,063 | 1,657 | -4,720 | 0.346 |
| 15m | or_low | 1.0R | 26 | 2/8/16 | -0.269 | -3,440 | 981 | -4,421 | 0.346 |
| 15m | or_low | 2.0R | 26 | 1/8/17 | -0.231 | -2,961 | 982 | -3,943 | 0.346 |
| 30m | or_mid | 1.0R | 21 | 4/7/10 | -0.166 | -1,700 | 1,215 | -2,915 | 0.381 |
| 30m | or_mid | 2.0R | 21 | 1/8/12 | -0.196 | -2,023 | 1,215 | -3,239 | 0.333 |
| 30m | or_low | 1.5R | 21 | 1/3/17 | -0.127 | -1,305 | 698 | -2,003 | 0.333 |

### SBIN

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 35 | 10/17/8 | -0.18 | -3,118 | 2,980 | -6,098 | 0.371 |
| 15m | or_mid | 2.0R | 35 | 2/20/13 | -0.364 | -6,338 | 2,979 | -9,317 | 0.257 |
| 15m | or_low | 1.0R | 35 | 6/10/19 | -0.045 | -769 | 2,139 | -2,908 | 0.457 |
| 15m | or_low | 2.0R | 35 | 1/10/24 | -0.085 | -1,472 | 2,139 | -3,611 | 0.429 |
| 30m | or_mid | 1.0R | 32 | 8/12/12 | -0.076 | -1,199 | 2,720 | -3,920 | 0.438 |
| 30m | or_mid | 2.0R | 32 | 3/14/15 | -0.145 | -2,299 | 2,720 | -5,019 | 0.344 |
| 30m | or_low | 1.5R | 32 | 1/9/22 | -0.114 | -1,819 | 1,908 | -3,728 | 0.406 |

### ITC

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 33 | 13/14/6 | 0.0 | 2 | 2,874 | -2,871 | 0.515 |
| 15m | or_mid | 2.0R | 33 | 6/16/11 | 0.042 | 682 | 2,874 | -2,192 | 0.424 |
| 15m | or_low | 1.0R | 33 | 10/10/13 | 0.013 | 205 | 2,057 | -1,852 | 0.515 |
| 15m | or_low | 2.0R | 33 | 2/10/21 | 0.08 | 1,308 | 2,057 | -749 | 0.515 |
| 30m | or_mid | 1.0R | 31 | 11/11/9 | 0.07 | 1,076 | 2,586 | -1,510 | 0.548 |
| 30m | or_mid | 2.0R | 31 | 6/12/13 | 0.132 | 2,046 | 2,587 | -541 | 0.452 |
| 30m | or_low | 1.5R | 31 | 4/7/20 | 0.135 | 2,089 | 1,805 | 284 | 0.548 |

### LT

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 34 | 14/13/7 | 0.038 | 564 | 3,055 | -2,491 | 0.5 |
| 15m | or_mid | 2.0R | 34 | 6/16/12 | 0.044 | 654 | 3,055 | -2,401 | 0.412 |
| 15m | or_low | 1.0R | 34 | 8/9/17 | 0.016 | 174 | 2,200 | -2,027 | 0.5 |
| 15m | or_low | 2.0R | 34 | 0/9/25 | -0.061 | -1,093 | 2,200 | -3,293 | 0.441 |
| 30m | or_mid | 1.0R | 33 | 12/13/8 | -0.025 | -410 | 2,788 | -3,198 | 0.455 |
| 30m | or_mid | 2.0R | 33 | 4/14/15 | 0.031 | 492 | 2,788 | -2,296 | 0.424 |
| 30m | or_low | 1.5R | 33 | 1/8/24 | -0.058 | -1,001 | 1,935 | -2,936 | 0.424 |

### AXISBANK

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 40 | 15/18/7 | -0.04 | -818 | 3,548 | -4,366 | 0.475 |
| 15m | or_mid | 2.0R | 40 | 7/21/12 | 0.001 | -5 | 3,548 | -3,553 | 0.4 |
| 15m | or_low | 1.0R | 40 | 12/13/15 | -0.05 | -1,004 | 2,568 | -3,572 | 0.475 |
| 15m | or_low | 2.0R | 40 | 4/13/23 | -0.025 | -526 | 2,568 | -3,094 | 0.45 |
| 30m | or_mid | 1.0R | 37 | 15/13/9 | 0.067 | 1,226 | 3,102 | -1,877 | 0.514 |
| 30m | or_mid | 2.0R | 37 | 5/16/16 | 0.057 | 1,027 | 3,102 | -2,076 | 0.405 |
| 30m | or_low | 1.5R | 37 | 4/10/23 | -0.042 | -790 | 2,151 | -2,941 | 0.432 |

### KOTAKBANK

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 43 | 19/18/6 | -0.013 | -277 | 3,692 | -3,969 | 0.442 |
| 15m | or_mid | 2.0R | 43 | 8/21/14 | -0.023 | -516 | 3,692 | -4,208 | 0.326 |
| 15m | or_low | 1.0R | 43 | 11/11/21 | -0.014 | -302 | 2,654 | -2,955 | 0.395 |
| 15m | or_low | 2.0R | 43 | 3/11/29 | 0.025 | 536 | 2,654 | -2,118 | 0.349 |
| 30m | or_mid | 1.0R | 40 | 16/16/8 | -0.049 | -981 | 3,233 | -4,214 | 0.425 |
| 30m | or_mid | 2.0R | 40 | 6/18/16 | -0.02 | -427 | 3,234 | -3,661 | 0.325 |
| 30m | or_low | 1.5R | 40 | 4/9/27 | -0.011 | -218 | 2,256 | -2,474 | 0.35 |

### BHARTIARTL

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 32 | 13/14/5 | -0.044 | -711 | 3,053 | -3,764 | 0.469 |
| 15m | or_mid | 2.0R | 32 | 9/15/8 | 0.18 | 2,854 | 3,054 | -200 | 0.438 |
| 15m | or_low | 1.0R | 32 | 11/11/10 | 0.015 | 203 | 2,192 | -1,989 | 0.438 |
| 15m | or_low | 2.0R | 32 | 5/12/15 | 0.055 | 845 | 2,193 | -1,348 | 0.375 |
| 30m | or_mid | 1.0R | 28 | 12/10/6 | 0.05 | 674 | 2,478 | -1,804 | 0.464 |
| 30m | or_mid | 2.0R | 28 | 9/10/9 | 0.377 | 5,207 | 2,479 | 2,727 | 0.464 |
| 30m | or_low | 1.5R | 28 | 6/8/14 | 0.096 | 1,308 | 1,750 | -442 | 0.393 |

### HINDUNILVR

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 30 | 9/10/11 | -0.109 | -1,634 | 2,548 | -4,182 | 0.333 |
| 15m | or_mid | 2.0R | 30 | 5/10/15 | 0.051 | 750 | 2,549 | -1,799 | 0.333 |
| 15m | or_low | 1.0R | 30 | 5/6/19 | -0.04 | -588 | 1,718 | -2,305 | 0.333 |
| 15m | or_low | 2.0R | 30 | 2/7/21 | -0.045 | -655 | 1,718 | -2,373 | 0.3 |
| 30m | or_mid | 1.0R | 27 | 7/8/12 | -0.099 | -1,325 | 2,204 | -3,529 | 0.333 |
| 30m | or_mid | 2.0R | 27 | 3/8/16 | -0.001 | -5 | 2,205 | -2,210 | 0.333 |
| 30m | or_low | 1.5R | 27 | 2/5/20 | -0.062 | -856 | 1,477 | -2,332 | 0.333 |

### BAJFINANCE

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 34 | 15/14/5 | 0.025 | 441 | 2,510 | -2,069 | 0.471 |
| 15m | or_mid | 2.0R | 34 | 8/16/10 | 0.175 | 2,965 | 2,511 | 454 | 0.412 |
| 15m | or_low | 1.0R | 34 | 9/7/18 | 0.035 | 583 | 1,686 | -1,102 | 0.471 |
| 15m | or_low | 2.0R | 34 | 4/7/23 | 0.153 | 2,573 | 1,687 | 886 | 0.441 |
| 30m | or_mid | 1.0R | 30 | 12/13/5 | -0.008 | -93 | 2,048 | -2,141 | 0.467 |
| 30m | or_mid | 2.0R | 30 | 4/13/13 | 0.117 | 1,774 | 2,049 | -275 | 0.433 |
| 30m | or_low | 1.5R | 30 | 4/5/21 | 0.114 | 1,685 | 1,324 | 360 | 0.5 |

### MARUTI

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 37 | 14/16/7 | -0.027 | -359 | 3,321 | -3,680 | 0.486 |
| 15m | or_mid | 2.0R | 37 | 5/19/13 | -0.098 | -1,613 | 3,321 | -4,933 | 0.405 |
| 15m | or_low | 1.0R | 37 | 6/13/18 | -0.182 | -3,308 | 2,307 | -5,615 | 0.405 |
| 15m | or_low | 2.0R | 37 | 1/14/22 | -0.235 | -4,311 | 2,307 | -6,617 | 0.378 |
| 30m | or_mid | 1.0R | 36 | 10/17/9 | -0.2 | -3,293 | 2,935 | -6,228 | 0.389 |
| 30m | or_mid | 2.0R | 36 | 3/18/15 | -0.263 | -4,393 | 2,934 | -7,328 | 0.306 |
| 30m | or_low | 1.5R | 36 | 1/11/24 | -0.25 | -4,346 | 2,036 | -6,382 | 0.306 |

### M&M

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 34 | 12/10/12 | 0.056 | 931 | 2,535 | -1,604 | 0.471 |
| 15m | or_mid | 2.0R | 34 | 4/11/19 | 0.044 | 738 | 2,535 | -1,797 | 0.412 |
| 15m | or_low | 1.0R | 34 | 4/7/23 | -0.048 | -840 | 1,715 | -2,555 | 0.441 |
| 15m | or_low | 2.0R | 34 | 1/7/26 | -0.01 | -204 | 1,716 | -1,919 | 0.441 |
| 30m | or_mid | 1.0R | 33 | 11/10/12 | -0.002 | -51 | 2,410 | -2,461 | 0.424 |
| 30m | or_mid | 2.0R | 33 | 4/10/19 | 0.049 | 774 | 2,411 | -1,637 | 0.394 |
| 30m | or_low | 1.5R | 33 | 3/7/23 | 0.007 | 86 | 1,607 | -1,521 | 0.424 |

### SUNPHARMA

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 31 | 12/13/6 | 0.029 | 440 | 2,554 | -2,115 | 0.548 |
| 15m | or_mid | 2.0R | 31 | 3/16/12 | -0.12 | -1,870 | 2,553 | -4,423 | 0.419 |
| 15m | or_low | 1.0R | 31 | 7/6/18 | 0.067 | 1,007 | 1,789 | -782 | 0.516 |
| 15m | or_low | 2.0R | 31 | 0/6/25 | -0.045 | -680 | 1,788 | -2,468 | 0.484 |
| 30m | or_mid | 1.0R | 29 | 9/13/7 | -0.106 | -1,529 | 2,258 | -3,787 | 0.448 |
| 30m | or_mid | 2.0R | 29 | 2/14/13 | -0.168 | -2,419 | 2,258 | -4,677 | 0.414 |
| 30m | or_low | 1.5R | 29 | 1/6/22 | -0.099 | -1,431 | 1,524 | -2,956 | 0.414 |

### TITAN

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 37 | 19/12/6 | 0.178 | 3,144 | 3,264 | -120 | 0.568 |
| 15m | or_mid | 2.0R | 37 | 9/15/13 | 0.241 | 4,241 | 3,265 | 976 | 0.459 |
| 15m | or_low | 1.0R | 37 | 14/7/16 | 0.208 | 3,724 | 2,320 | 1,404 | 0.595 |
| 15m | or_low | 2.0R | 37 | 2/8/27 | 0.169 | 2,953 | 2,319 | 633 | 0.514 |
| 30m | or_mid | 1.0R | 35 | 15/10/10 | 0.105 | 1,793 | 2,760 | -967 | 0.514 |
| 30m | or_mid | 2.0R | 35 | 4/12/19 | 0.123 | 2,107 | 2,760 | -653 | 0.457 |
| 30m | or_low | 1.5R | 35 | 3/6/26 | 0.025 | 313 | 1,871 | -1,558 | 0.486 |

### NTPC

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 37 | 13/22/2 | -0.239 | -4,416 | 3,238 | -7,654 | 0.378 |
| 15m | or_mid | 2.0R | 37 | 4/25/8 | -0.385 | -7,130 | 3,237 | -10,367 | 0.27 |
| 15m | or_low | 1.0R | 37 | 5/10/22 | -0.201 | -3,716 | 2,312 | -6,028 | 0.378 |
| 15m | or_low | 2.0R | 37 | 1/10/26 | -0.198 | -3,656 | 2,312 | -5,968 | 0.351 |
| 30m | or_mid | 1.0R | 34 | 11/15/8 | -0.093 | -1,588 | 2,913 | -4,501 | 0.441 |
| 30m | or_mid | 2.0R | 34 | 3/18/13 | -0.241 | -4,113 | 2,912 | -7,025 | 0.353 |
| 30m | or_low | 1.5R | 34 | 1/6/27 | -0.123 | -2,090 | 1,998 | -4,087 | 0.412 |

### BAJAJ-AUTO

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 29 | 12/9/8 | 0.146 | 1,981 | 2,395 | -413 | 0.586 |
| 15m | or_mid | 2.0R | 29 | 6/11/12 | 0.226 | 3,131 | 2,395 | 736 | 0.483 |
| 15m | or_low | 1.0R | 29 | 7/6/16 | 0.053 | 771 | 1,655 | -884 | 0.517 |
| 15m | or_low | 2.0R | 29 | 2/6/21 | 0.065 | 987 | 1,655 | -669 | 0.483 |
| 30m | or_mid | 1.0R | 28 | 9/8/11 | 0.126 | 1,611 | 2,129 | -519 | 0.607 |
| 30m | or_mid | 2.0R | 28 | 2/10/16 | 0.005 | -43 | 2,129 | -2,172 | 0.464 |
| 30m | or_low | 1.5R | 28 | 2/5/21 | -0.0 | -111 | 1,408 | -1,519 | 0.464 |

### ULTRACEMCO

| OR | stop | target | trades | target/stop/close | avg R (before charges) | gross ₹ | charges ₹ | net ₹ | net win rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15m | or_mid | 1.0R | 38 | 14/17/7 | -0.091 | -1,602 | 3,335 | -4,937 | 0.447 |
| 15m | or_mid | 2.0R | 38 | 8/19/11 | 0.005 | 70 | 3,335 | -3,265 | 0.395 |
| 15m | or_low | 1.0R | 38 | 13/7/18 | 0.159 | 2,712 | 2,317 | 396 | 0.579 |
| 15m | or_low | 2.0R | 38 | 2/8/28 | 0.191 | 3,299 | 2,317 | 982 | 0.553 |
| 30m | or_mid | 1.0R | 38 | 13/18/7 | -0.143 | -2,509 | 3,117 | -5,625 | 0.421 |
| 30m | or_mid | 2.0R | 38 | 5/20/13 | -0.147 | -2,627 | 3,117 | -5,744 | 0.368 |
| 30m | or_low | 1.5R | 38 | 2/7/29 | 0.069 | 1,420 | 2,110 | -690 | 0.526 |

