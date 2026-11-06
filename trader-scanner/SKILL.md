---
name: trader-scanner
description: >-
  Chart Scanner. Scans thousands of charts for setups: opening-range
  breakouts, flags, oversold bounces on NSE stocks. Builds the list of NSE
  EQ-series stocks from NSE's EQUITY_L.csv, runs a pre-market scan of daily closes (20-day closing-high breakout, bull
  flag, reclaimed the 20-day average, oversold, oversold bounce) and an
  intraday opening-range breakout scan on 5-minute bars, then writes
  trader/watchlist.json for trader-news and trader-entry. Free Yahoo data,
  bar by bar. Use when the user says "scan the market", "find me setups",
  "what is breaking out", "opening range breakouts", "scan for bull flags",
  "oversold stocks", "pre-market scan", "build my watchlist", "what should I
  look at today", or at the start of a trading day before /trader-news.
argument-hint: "[universe | daily | orb] [--at HH:MM]"
---

# trader-scanner

The Chart Scanner is the first step of a day trade. It reads thousands of
free charts and lists the ones that match a rule. That is all it does. A scan
is a list of charts that match a rule, not a list of stocks to buy, and a
setup on a chart is not a prediction. Most people who day trade lose money;
the scanner does not change that. It only saves you from flipping through
2,000 charts by hand.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/scan.py" universe                       # -> trader/universe.txt
python3 "${CLAUDE_SKILL_DIR}/scan.py" daily                          # before the open -> trader/watchlist.json
python3 "${CLAUDE_SKILL_DIR}/scan.py" daily --symbols RELIANCE,INFY,TCS  # or --watchlist FILE, --limit 200
python3 "${CLAUDE_SKILL_DIR}/scan.py" orb                            # after 9:35 AM IST -> trader/watchlist.json
python3 "${CLAUDE_SKILL_DIR}/scan.py" orb --at 10:15                 # cut the clock at 10:15 AM IST
python3 "${CLAUDE_SKILL_DIR}/scan.py" orb --watchlist trader/watchlist.json --json
```

Flags: `--min-price 50` (rupees) and `--min-volume` (daily 500,000 shares, orb 0),
`--or-minutes 15`, `--max-confirm 200` (orb stage 2),
`--now "2026-11-06 10:15"` (IST) to pin the clock, `--offline PATH`
to read saved Yahoo files, `--no-write`, `--show N`, `--json`. Exit code 0
when the scan found something, 1 when it found nothing or could not run (the
reason is one plain line).

## What it reads and writes

| file | what |
| --- | --- |
| `trader/universe.txt` | written by `universe`: one `SYMBOL\|Name` a line, read by `daily` and `orb` |
| `trader/watchlist.json` | written by `daily` and `orb`: `mode`, `as_of`, `universe`, `scanned`, `failed`, `hits[]`. trader-news and trader-entry read `hits[].symbol` |
| `trader/config.json` | read by `orb`: `no_entries_after` (default 15:30) |

## The universe

`universe` downloads NSE's equity list
(`nsearchives.nseindia.com/content/equities/EQUITY_L.csv`) and keeps the EQ
series only: BE (trade-to-trade) stocks must be delivered, so they can't be a
day trade. NSE often blocks scripts; if the download fails, ask the user to
save the CSV from a browser and run `scan.py universe --offline EQUITY_L.csv`.
`trader/universe.txt` holds SYMBOL|Company name lines; trader-news uses the
names to match NSE filings and trader-risk uses the list to block non-EQ
symbols.

Not checked here: stocks under ASM/GSM surveillance or in a 2%/5% price band.
Brokers often block intraday on those; check the broker app.

A chart is usable only when every 5-minute bar from 9:15 to the cutoff is
there; a missing bar means a halt or a thin stock. Null closes are dropped,
a bar off the 5-minute grid (the live tick, like 10:58:07) is dropped, and a
bar counts only once it is complete (start + 5 minutes). Before 9:35 AM, on a
weekend or holiday, after the close, or after `no_entries_after` (an expired
setup) it prints one plain line and writes nothing.

## Data and limits

- Yahoo's chart and spark endpoints are free, unofficial and can lag. Bars are
  5-minute bars, bar by bar, never tick by tick. query2 first, query1 on a 429
  or 5xx, one retry after a 5-second wait on a 429.
- Partial results are said as partial: "Fetched 4,980 of 5,259 charts (279
  failed or had no data)". Never round a partial scan up to "the whole market".
- NSE trading holidays for 2026 (circulars NSE/CMTR/71775 and NSE/CMTR/72260). 2027 is not
  published yet: the tool says the holiday list is unknown then.
- Charts come from Yahoo's .NS tickers (RELIANCE -> RELIANCE.NS).

## Steps

1. Once a week or so: `scan.py universe`.
2. Before the open: `scan.py daily`. Tell the user the counts (fetched,
   liquid, scanned, hits) and the top few by setup.
3. After 9:35 AM IST (10:15 is the classic): `scan.py orb`. Tell the user how
   many usable charts broke their range and when, and that a later hit is
   closer to the price now.
4. The user picks one chart. Hand it on: `/trader-news TICKER` (what is moving
   it), then `/trader-entry TICKER` (the entry bar by bar). Never pick for them.


## Rules

- Say what was scanned: how many symbols, how many charts came back, how many
  were usable, and the time of the data.
- Say "matched a rule", never "a buy", "a winner" or "a good trade".
- Never print a P&L, a return or a profit figure.
- A hit is stale once the price has moved on. Re-run before acting on it.

## What it never does

It never places, sizes or checks an order, never says which stock to buy,
never calls data real time, and never promises that a setup works.

## Safety

- Education and tooling, not financial advice. A PASS is a rules check, not a recommendation.
- Most people who day trade lose money: SEBI found 71% of individual intraday traders in the equity
  cash segment made a net loss in FY 2022-23 (PR 13/2024).
- Dry run by default (`"dry_run": true`): Claude never calls the broker, the user places the order.
  Going live is the user's own decision, in their own config.
- Nothing in this pack places an order except trader-broker, and only when trader-risk passed that
  exact order today and the user typed an explicit yes for that one order in the chat; live, the
  broker connector's order tool must be on "Needs approval" so Claude's card asks again.
- NSE cash-segment intraday only: no F&O, MTF, margin, short selling or delivery orders.
- Broker credentials never go in the chat.
