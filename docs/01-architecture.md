# How the expense agent works

## The shape

```
Telegram ──▶ Make webhook ──▶ owner gate ──▶ router
                                               │
                    ┌──────────────────────────┴───────────────────────┐
                    │                                                  │
              /command                                        free text or photo
                    │                                                  │
            read the ledger                                   Claude parses it
                    │                                                  │
                    │                              ┌────────────┬──────┴────────┐
                    │                          log_expense  ask_clarification  confirm_first
                    │                              │            │               │
                    │                       append a row    ask, write     buttons, write
                    │                              │          nothing        nothing yet
                    └──────────────┬───────────────┘            │               │
                                   ▼                            ▼               ▼
                            reply in Telegram ◀─────────────────────────────────┘
```

Six Make operations per expense. Nothing is stored in Make; the Google Sheet is
the only record.

## Why each piece is where it is

**The owner gate is the second module, before anything else.** A message from any
other chat stops there — no model call, no row, no reply. Putting the gate first
means a leaked bot username costs nothing: strangers can message the bot and it
will sit there silently.

**The trigger is a plain webhook, not a Telegram app trigger.** Telegram pushes
updates to a URL; a gateway webhook receives them instantly with no polling and
no extra connection to maintain. It also means the same scenario can later
receive button taps (`callback_query`) through the same door.

**Claude only reads and returns JSON. It never writes.** The model's output goes
through a JSON parse and then a filter on `action`. A malformed reply fails at
the parse step and writes nothing. A reply asking for something outside the four
allowed actions matches no filter and writes nothing. The worst a bad parse can
do is put a wrong number in a row you can see and fix.

**Two gates on money.** Anything at or above 10,000 GEL comes back for a tap
instead of being written, and so does anything the model is less than 60% sure
about. The threshold lives in the prompt, not the scenario, so you can change it
by editing `prompts/01-expense-agent.md`.

**Nothing is ever deleted.** `/undo` writes `void` into column P; the row stays.
The ledger is the audit trail for a bank-financed project — it has to be
append-only or it is not evidence of anything.

## The seven categories

The bot may only use these, because the financial model reads them by name:

| Code | Treatment | |
|---|---|---|
| `construction_advance` | CAPEX | payments to GSN Group under contract N1 |
| `materials` | CAPEX | concrete, electrical, metal, anything built in |
| `supplier_invoice` | CAPEX | a supplier invoice that is not clearly materials |
| `salaries` | OPEX | wages |
| `taxes` | OPEX | tax office, pension fund |
| `services` | OPEX | consultants, accounting, contracted services |
| `other` | CAPEX | registry fees, permits |

CAPEX lands in the cost of the greenhouse; OPEX is money spent running the
project before there is a crop. The split is the difference between 78,971 GEL
of asset and 11,570 GEL of cost in the numbers as they stand.

## Receipt photos

Telegram delivers a photo as `message.photo[]` (an array of sizes, largest last)
plus `message.caption`. The blueprint already normalises caption into the text
variable, so a captioned photo is parsed like any message.

To have the model actually *read* the image, add a second content block to
module 6's user message:

```json
{ "type": "image", "source": { "type": "url", "url": "<file url from getFile>" } }
```

That needs a `getFile` call first — Telegram file URLs are built from the token —
which is why it is not in the blueprint by default. Until then, photograph the
receipt and type the amount; the caption path works today.

## What this is not

It is not a bookkeeping system and it does not talk to the bank. The bank
statement remains the source of truth: every month, export it and reconcile it
against the ledger. Anything logged here that never appeared on the statement
is either a cash payment or a mistake, and you want to know which.

It also does not write into `finance/Greenhouse_CashFlow_2000m2.xlsx`. That
workbook is rebuilt from the ledger when you want a fresh picture — see
`finance/README.md`.

## Prompt injection

Receipts, forwarded messages and file names are **data**. The conventions prompt
says so explicitly, and the four-action contract means a model that is talked
into something still cannot express it: there is no action code for "send money",
"change the budget" or "delete a row". The blast radius of a successful injection
is one wrong row in a sheet you read every week.
