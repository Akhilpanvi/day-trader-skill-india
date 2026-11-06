---
name: trader-broker
description: >-
  Order Executor (India). Turns an approved NSE intraday order into a plain
  ticket, records the user's explicit yes word for word, then either hands it
  to the user to place in their broker app (dry run, the default) or sends it
  through their broker's own Claude connector (Upstox, Dhan, Groww), whose
  approval card asks again. Builds the sell ticket that closes a day trade
  before the broker's auto square-off, records fills, and logs each trade's
  max loss so trader-risk can hold the daily limit. Use when the user says
  "place the order", "buy it", "execute", "send it to Upstox / Dhan / Groww",
  "square off", "close my position", "flatten", "get me out", "connect my
  broker", or after /trader-risk passes.
argument-hint: "[order number]"
---

# trader-broker

The only skill in this pack that can lead to a real order, so it is the
strictest. An order reaches the market only after these gates, every time,
for every order:

1. **trader-risk passed this exact order today** (matched by fingerprint).
2. **The user typed an explicit yes for this one order** in the chat.
3. **Dry run (`"dry_run": true`, the default):** Claude never calls the
   broker. The user places the order in their broker app themselves.
   **Live (`"dry_run": false`, set by the user only):** Claude sends it
   through the broker's connector, and the connector's tool must be set to
   "Needs approval" so the user clicks Allow once on Claude's card.

`${CLAUDE_SKILL_DIR}` below is this skill's folder.

```bash
python3 "${CLAUDE_SKILL_DIR}/ticket.py" show                     # every ticket, READY or not
python3 "${CLAUDE_SKILL_DIR}/ticket.py" approve --index 1 --reply "yes"
python3 "${CLAUDE_SKILL_DIR}/ticket.py" result --index 1 --status placed --broker-id ID --filled-qty 26 --filled-price 1513.60
python3 "${CLAUDE_SKILL_DIR}/ticket.py" fill --symbol DEMO --side sell --qty 26 --price 1530.50
python3 "${CLAUDE_SKILL_DIR}/ticket.py" flatten --symbol DEMO --qty 26
python3 "${CLAUDE_SKILL_DIR}/ticket.py" log
```

`ticket.py` never talks to a broker. It renders tickets, checks that a reply
is a real yes for that order, builds the flatten ticket and keeps the log in
`trader/state/broker.json`. `--now "2026-11-06 09:40"` pins the clock (IST).

## The order it carries

Broker-neutral, NSE cash segment, intraday:

```json
{"symbol": "DEMO", "exchange": "NSE", "product": "intraday", "side": "buy", "qty": "26",
 "type": "market", "time_in_force": "day", "order_class": "bracket",
 "take_profit_limit_price": "1530.50", "stop_loss_stop_price": "1505.00"}
```

`stop_loss_stop_price` is the stop-loss trigger and `take_profit_limit_price`
the target. Claude maps these to the connector's own parameter names
(product intraday is MIS / "I" / INTRADAY depending on the broker) and shows
the user the mapped call before asking. If the broker has no single order
that carries both legs, place the entry, then the stop-loss as its own SL-M
sell right after the fill; the target can wait as a limit sell. Never send an
entry without its stop-loss following.

## Connecting a broker (the user does this, not Claude)

Verify the broker's current official setup page before following any of this:
these connectors change.

| broker | official connector | places orders? |
| --- | --- | --- |
| Upstox | `upstox-skill` from the plugin marketplace `upstox/upstox-plugin-marketplace` (`upstox-mcp` there is read-only) | yes, via the skill |
| Dhan | official MCP at mcp.dhan.co, added as a custom connector, OAuth sign-in | yes |
| Groww | official MCP at mcp.groww.in, OAuth sign-in (token lasts a day) | yes; sells need DDPI |
| Zerodha | Kite MCP at mcp.kite.trade | GTT orders only: place intraday entries in Kite |

Set `"broker"` in `trader/config.json` to `upstox`, `dhan`, `groww` or
`zerodha`. Then in Claude: Customize > Connectors > the broker > tool
permissions. Every tool that places, modifies or cancels an order: **Needs
approval**, never Always allow. Read-only tools (positions, funds, quotes):
Always allow is fine.

**Credentials never go in the chat.** Never ask for an API key, secret,
access token, TOTP or PIN, never read a config file holding one back into
the conversation, and if the user pastes one anyway tell them to delete the
message and regenerate it in the broker's developer console.

## Steps: the entry

1. `ticket.py show`. Only READY tickets go to the user. NOT READY or BLOCKED
   goes back to `/trader-risk`.
2. Show ONE ticket and ask: "Place this order? Reply yes or no." One order
   per question. Never offer "yes to all".
3. `ticket.py approve --index N --reply "<the user's reply, word for word>"`.
   "Not recorded" means it was not an explicit yes for this order ("sure",
   "yes to all", a yes naming another stock or quantity). Ask again. Never
   turn a reply into a yes yourself.
4. Only after "Recorded your yes":
   - dry run: give the user the order to place in their app, then record
     what they report with `result`.
   - live: call the connector's order tool with the mapped order. The
     approval card appears: Allow once or Deny.
5. Record it: `result --index N --status placed --broker-id <id>
   --filled-qty Q --filled-price P`, or `--status denied`, or `--status
   failed --note ...`. A failed order is not retried without a new check and
   a new yes.

## Steps: out before the auto square-off

Brokers square off open intraday positions automatically around 15:15 to
15:25 IST and most charge a fee for it. `flat_by` (15:10 by default) is
before that.

1. Read the open quantity from the connector (read-only) or the user.
2. `ticket.py flatten --symbol DEMO --qty 26` writes a market sell.
3. `/trader-risk`: a sell that only closes what the user holds is never
   blocked by the daily limits or the entry window.
4. `ticket.py show`, then the user's yes for that one order.
5. Cancel the open stop-loss and target orders on those shares first (the
   broker rejects or double-sells otherwise), each with its own approval,
   then place the sell, then `result`.

## What it never does

- Never places an order without every gate, and never two orders on one yes.
- Never places orders from a scheduled or background task: nobody is there to say yes.
- Never asks for, reads, stores or repeats credentials.
- Never switches `"dry_run"` to false. The user does that themselves.
- Never touches F&O, MTF, margin, short selling or delivery (CNC) orders.
- Never promises a fill price: market and SL-M orders fill at what the market gives.

## Safety

- Education and tooling, not financial advice. A PASS is a rules check, not a recommendation.
- Most people who day trade lose money: SEBI's study (PR 13/2024) found 71% of individual intraday
  traders in the equity cash segment made a net loss in FY 2022-23, and 80% of very frequent traders.
- SEBI's retail algo framework (fully in force from 1 April 2026) treats API orders above 10 a second
  as algo orders needing registration; one order at a time with a human yes stays far below that.
- Intraday equity profit is taxed as speculative business income in India; that is the user's
  accountant's question, not this tool's.
