---
name: trader-budget
description: >-
  Budget Manager. Sizes every position to your budget and your max loss per
  trade. Reads the trade plan from trader-exit (entry, stop, target), finds
  the whole shares that fit inside four limits (max loss per trade, position
  cap, max order, cash after your buffer), says which limit decided it, and
  writes ONE NSE intraday order (entry, stop-loss, target) to
  trader/orders.json, broker-neutral. The max loss includes Indian charges
  (brokerage, STT, exchange, SEBI, stamp duty, GST). A stop
  too far away for your max loss is a plain refusal, not a smaller order.
  Nothing is placed. Use when the user says "how many shares", "size this
  trade", "how much should I buy", "I have ₹1 lakh", "I only want to risk ₹500
  a trade", "set my rules", "keep 10% in cash", or after /trader-exit writes
  a plan.
argument-hint: "[budget in rupees]"
---

# trader-budget

The Budget Manager turns a plan ("buy RELIANCE at 1513.50, stop 1505.00") into an
exact order ("buy 8 shares"), inside rules the user sets once. The stop
decides the size: the further away the stop, the fewer shares. It writes a
proposal only. trader-risk checks it and trader-broker asks the user yes or
no. Day trading loses most people money. Sizing to a max loss keeps each
loss small; it does not make a trade win.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/size.py"                        # trader/plan.json + trader/config.json
python3 "${CLAUDE_SKILL_DIR}/size.py" --write                # write trader/orders.json
python3 "${CLAUDE_SKILL_DIR}/size.py" --limit --write        # a limit order at the plan's entry
python3 "${CLAUDE_SKILL_DIR}/size.py" --limit 1513.00 --json  # a limit order at 1513.00
python3 "${CLAUDE_SKILL_DIR}/size.py" --weights HDFCBANK=40,KO=60 --config split.json   # weights mode, below
```

`--now "2026-11-06 10:15"` pins the clock (IST). A plan for
another day is refused: make a new one with trader-exit.

## What it reads and writes

| file | what |
| --- | --- |
| `trader/config.json` | the rules (start from `config.example.json` in this folder) |
| `trader/plan.json` | the trade: entry, stop, target, setup, flat-by time (trader-exit writes it) |
| `trader/prices.json` | optional: a fresh price above the plan's entry means a bigger risk (trader-alerts writes it) |
| `trader/portfolio.json` | optional: its cash caps the size (trader-broker keeps it) |
| `trader/orders.json` | the one proposed bracket order it writes with `--write` |

## Step 1: set the rules once

If `trader/config.json` does not exist, copy `config.example.json` into
`trader/config.json` and ask the user for each value in plain words:

- **budget**: how much money this is for. Only money they can afford to lose.
- **cash_buffer_pct**: how much always stays in cash (default 10).
- **max_loss_per_trade_inr**: the most one trade may lose if the stop fills at the stop (default 50).
- **max_position_pct**, **max_order_inr**, **min_order_inr**: the biggest position (75% of the
  budget), the biggest order (₹40,000) and the smallest order (₹500).
- The day limits trader-risk enforces: **max_daily_loss_inr** (1,500), **max_trades_per_day** (3),
  **min_reward_risk** (1.0), **require_stop** (true), **no_entries_before** / **no_entries_after**
  ("09:30" / "15:00") and **flat_by** ("15:10"), all IST.
- **blocked**: tickers they never want to trade.
- Keep **dry_run** true until they have watched it work for a while.
- **charges**: override the brokerage (default the lower of ₹20 or 0.03% an order) or any rate
  if their broker differs.

## Step 2: size the trade

```bash
python3 "${CLAUDE_SKILL_DIR}/size.py" --write
```

Whole shares only. The size is the smallest of four limits, then one share
less at a time until the loss at the stop PLUS the round trip's charges fits
the max loss:

| limit | shares |
| --- | --- |
| max loss | `max_loss_per_trade_inr` / risk a share (entry minus stop) |
| position cap | budget x `max_position_pct` / entry |
| max order | `max_order_inr` / entry |
| cash | (budget minus the cash buffer) / entry, never more than the cash in `trader/portfolio.json` |

The entry it sizes at: the limit price with `--limit`. For a market order, the
plan's entry, or the price in `trader/prices.json` if it is fresh (under 15
minutes old) and higher. A price that ran up since the plan means a bigger
loss at the same stop, so fewer shares. A lower price never shrinks the risk.

It refuses, and writes no order, when: the size is zero shares, the order is
under the minimum, reward:risk is under `min_reward_risk`, the stop is not
below the entry, the target is not above it (the move already happened), the
plan is for another day, the ticker is blocked, or the plan is a short. Say
the reason to the user in one line.

## Step 3: show the user

Show the four limits, which one decided the size, the shares, the rupees,
the max loss at the stop including charges, and the net at the target. Say plainly that a stop is an order, not a
promise: in a fast market it can fill below the stop. Then hand over to
`/trader-risk`.


## Weights mode (kept from v1)

`--weights RELIANCE=30,HDFCBANK=25` or `--targets FILE` (`targets.example.json`
here, illustrative only) splits a budget across a list by weight: cash buffer
off the top, weights renormalised, capped at `max_position_pct`, slices under
the minimum order dropped. These are plain buys with no stop: trader-risk
blocks them while `require_stop` is true. It is not a day-trade tool.

## Rules

- Proposals only. This skill never calls a broker tool.
- Never size money the user has not said is for this. Ask for the budget and the max loss.
- Every number comes from the config, the plan or the prices. Nothing is guessed.
- No projections: never say what a trade will make. A target is a plan, not a forecast.
- Free Yahoo prices are unofficial and can lag. The broker's price is the one that fills.

## What it never does

It never places, approves or schedules an order, never raises a limit on its
own, never shrinks a stop to fit more shares, and never sizes options,
margin or short positions.

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
