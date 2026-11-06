# The Day Trader skill: India edition

Nine Claude skills for intraday trading on the NSE: scan charts, track
news and NSE filings, time the entry and the exit, replay the trade 10,000
times before you risk a rupee, size it with Indian charges included, check
it against your limits, and hand it to your broker only after you say yes.

A fork of [Jakeschincariol/day-trader-skill](https://github.com/Jakeschincariol/day-trader-skill)
(MIT), ported from US markets to India. Plain Python, standard library only,
no API keys for the data tools.

> **Dry run is the default.** Nothing in this pack places an order on its own.
> With `"dry_run": true` Claude never calls your broker: it gives you the
> checked order and you place it in your broker's app.

## What changed from the US version

| | US original | India edition |
| --- | --- | --- |
| Market hours | 9:30–16:00 ET, DST | 9:15–15:30 IST, no DST |
| Holidays | NYSE 2026–27 | NSE 2026 (circulars NSE/CMTR/71775, 72260) |
| Universe | Nasdaq Trader lists | NSE `EQUITY_L.csv`, EQ series only (BE / T2T can't be day-traded) |
| Charts | Yahoo `TSLA` | Yahoo `RELIANCE.NS` (type plain NSE symbols) |
| Filings | SEC EDGAR 8-K | NSE RSS: announcements, board meetings, financial results |
| Money | $ | ₹, with brokerage, STT, exchange, SEBI, stamp duty and GST counted in every max loss |
| Flat by | 15:55 | 15:10, before the broker's intraday auto square-off |
| Broker | Alpaca paper / IBKR | Upstox, Dhan, Groww connectors; Zerodha (GTT only); dry run by default |
| Rules | PDT guard | removed (no PDT rule in India); SEBI algo note; EQ-series block |
| Dropped | | `trader-analyst` (SEC XBRL) and `trader-pelosi` (US Congress filings): no free Indian equivalent that works reliably |

## Install

In Claude Code:

```
/plugin marketplace add Akhilpanvi/day-trader-skill-india
/plugin install day-trader-skill-india@day-trader-skill-india
```

Or copy the folders: `cp -r trader-* ~/.claude/skills/`. Python 3.8+.

## The nine

| command | job |
| --- | --- |
| `/trader-scanner` | NSE universe, pre-market daily setups, opening-range breakouts |
| `/trader-news` | Yahoo headlines + NSE announcements, board meetings, results |
| `/trader-entry` | watches the setup bar by bar, says when it triggers |
| `/trader-exit` | stop and target before the entry, flat by 15:10 |
| `/trader-timemachine` | 10,000 replays of the rest of the session + every past time the rule fired |
| `/trader-budget` | shares that fit your max loss, charges included |
| `/trader-risk` | PASS / BLOCK against your limits, holidays, EQ series |
| `/trader-broker` | the ticket, your yes, then you (dry run) or your broker connector places it |
| `/trader-alerts` | stop, target and flat-by alerts, NSE clock |

## One trade, end to end (synthetic demo data)

`tests/fixtures/charts/DEMO.json` is **made-up data** for a fake symbol
`DEMO` (built by `tests/make_demo_fixture.py`), so this runs offline:

```
entry.py check DEMO --setup orb --now "2026-11-06 09:40" --offline tests/fixtures/charts/DEMO.json --write
  Opening range 9:15-9:30: high ₹1510.00, low ₹1500.00 (3 of 3 bars).
  TRIGGERED 9:40 AM at ₹1513.50: the 9:35 bar closed above the range high.
exit.py plan --write
  Entry ₹1,513.50, stop ₹1,505.00 (range midpoint), target ₹1,530.50 (2R), flat by 15:10 IST
timemachine.py run --offline ... --write
  target first 41.7 %, stop first 55.9 %, neither 2.4 % (seed 19)
size.py --write                      (₹1,00,000 budget, ₹500 max loss, ₹40,000 max order)
  26 shares = ₹39,351. Max loss at the stop: 26 x 8.50 = ₹221 + ₹41.68 charges = ₹262.68.
  At the target: ₹399.89 after ₹42.11 charges.
check.py
  PASS #1 buy DEMO 26 shares: max loss ₹262.68 (limit ₹500), reward:risk 2.00
ticket.py approve --index 1 --reply "yes to all"   -> Not recorded (one order per yes)
ticket.py approve --index 1 --reply "yes"          -> Dry run: place it yourself in your broker's app
```

## Fine print

**Not financial advice.** Software that reads public data and does arithmetic.
Most people who day trade lose money: SEBI's study (PR 13/2024) found 71% of
individual intraday traders in the equity cash segment made a net loss in
FY 2022-23.

**Charges** default to a discount broker's intraday rates (zerodha.com/charges,
read 2026-11-06): brokerage the lower of ₹20 or 0.03% an order, STT 0.025% on
the sell, NSE transaction 0.00307%, SEBI ₹10/crore, stamp 0.003% on the buy,
GST 18%. Set `"charges"` in `trader/config.json` if yours differ.

**Not checked:** ASM/GSM surveillance lists and 2%/5% price bands. Brokers
often block intraday on those stocks; your broker's app is the final word.

**SEBI algo rules** (fully in force 1 April 2026): API orders above 10 a
second count as algo orders needing registration. One order at a time with a
human yes is far below that.

**Taxes.** Intraday equity profit is speculative business income in India.
Nothing here is tax advice.

**Data is free and unofficial.** Yahoo's chart endpoint can lag or rate-limit;
NSE often blocks scripts (save `EQUITY_L.csv` from a browser if so).

```bash
python3 -m unittest discover -s tests -v      # offline, synthetic data
python3 tests/real_data_check.py              # real NSE data (needs internet)
```

**Real data in GitHub's cloud:** Actions tab > "real-data check" > Run workflow.
It runs the offline tests, then the real-data check, and publishes `REPORT.md`
(derived numbers only, no raw Yahoo data) to the `real-data-results` branch.

MIT. Original by [Jake Schincariol](https://opusjake.ai); India port by
[Akhil Panvi](https://akhilpanvi.com).
