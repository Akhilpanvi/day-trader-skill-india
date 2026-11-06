---
name: trader-news
description: >-
  News Monitor (India). Tracks breaking news on every NSE stock you watch:
  Yahoo Finance headlines plus NSE's own filing feeds (corporate
  announcements, board meetings that will consider results, financial
  results), prints only what is new since the last check with how far each
  stock has moved today, and flags a results date or board meeting that can
  gap a day trade past its stop. Use when the user says "any news on
  RELIANCE", "what's moving my stocks", "check the news", "is there results
  today", "board meeting", "corporate announcement", "why is it up", or after
  /trader-scanner and before /trader-entry.
argument-hint: "[SYMBOL ...]"
---

# trader-news

```bash
python3 "${CLAUDE_SKILL_DIR}/news.py"                          # watchlist + plan + portfolio symbols
python3 "${CLAUDE_SKILL_DIR}/news.py" --tickers RELIANCE INFY
python3 "${CLAUDE_SKILL_DIR}/news.py" --tickers RELIANCE --all --hours 72
python3 "${CLAUDE_SKILL_DIR}/news.py" --no-nse                  # headlines only
```

Symbols are plain NSE symbols (RELIANCE, M&M, BAJAJ-AUTO). Without
`--tickers` it reads `trader/watchlist.json`, `trader/plan.json` and
`trader/portfolio.json`.

## Sources

- **Yahoo Finance headline RSS**, one request per symbol (RELIANCE.NS).
- **NSE's RSS feeds**, one request each, listed on
  https://www.nseindia.com/static/rss-feed: `Online_announcements.xml`,
  `Board_Meetings.xml`, `Financial_Results.xml` under
  `nsearchives.nseindia.com/content/RSS/`. NSE titles each item with the
  company name, so matching needs names: run `scan.py universe` once (it
  writes `trader/universe.txt`, SYMBOL|Name). Without it, only filings whose
  attachment file name starts with the symbol match, and the tool says so.
- **The move**: Yahoo's chart endpoint, last price vs yesterday's close; 3%
  or more is flagged MOVING.

NSE sometimes blocks scripts. When a feed fails the tool prints a note and
the headlines still run; never present a partial check as complete.

## Reading it

- `!` marks a board meeting or results filing for the symbol, or an
  announcement about results, fund raising, mergers, resignations, ratings,
  pledges, defaults, buybacks, bonus or split. Say it first.
- A board meeting to consider results on the trade's day, or results already
  out this session, means the stock can gap through any stop. Say so plainly
  before the user plans an entry.
- Tags (earnings, analyst, legal, deal, capital, people, risk, halt,
  regulatory, macro) are keyword guesses. Headlines are leads, not facts:
  open the filing or story before acting.

State lives in `trader/state/news.json` (30 days), so an item shows once.
Times are IST. Not financial advice.
