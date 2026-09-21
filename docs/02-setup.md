# Setup — from nothing to a working bot

Eight steps. Everything that needs a password or a tap is yours; everything else
is in this repo. Budget about an hour.

---

## 1. Create the bot

In Telegram, open **@BotFather** → `/newbot` → give it a name
(`Mukhrani 2026 expenses`) and a username ending in `bot`.

BotFather replies with a token like `8123456789:AAH...`. **That token is a
password** — it lets anyone who has it read and send everything the bot does.
Keep it out of this repo, out of chat, and out of screenshots.

Then `/setprivacy` → **Disable**, so the bot can read messages in a group if you
ever add one.

## 2. Find your chat id

Send the bot any message, then open in a browser:

```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

Read `message.chat.id` — a number like `123456789`. That is the only chat that
will ever be allowed to write to the ledger.

## 3. The ledger — already created

The Google Sheet exists and is seeded with the 15 payments from the bank
statement, 1 July – 8 September 2026, totalling **90,541.21 GEL**:

**`მუხრანი 2026 — ხარჯები / expenses`**
`1NULNFpgxhzAqM7IWPr8-gxtRbqQ4MxMXgyNwrDzktLE`
https://docs.google.com/spreadsheets/d/1NULNFpgxhzAqM7IWPr8-gxtRbqQ4MxMXgyNwrDzktLE/edit

**The tab is called `Untitled`.** That is Google's doing — a CSV import names the
file after the CSV and leaves the tab itself unnamed. The scenario reads the
tab, not the file, so `Untitled` is what modules 4 and 8 carry. Renaming the tab
is fine, but you have to change both modules to match on the same day, or the
bot answers `Unable to parse range` and nothing else.

Do not reorder the columns — the bot writes by position, not by header.

## 4. The scenario — already built

It exists in Make, **switched off**, with the Anthropic and Google connections
already attached and the ledger id and system prompt already filled in:

| | |
|---|---|
| Scenario | **Mukhrani 2026 — Greenhouse expenses (Telegram)**, id `7471723` — **active** |
| Webhook | hook `3740894` · `https://hook.eu1.make.com/jok35l9zggg7dqpqt6bzl6ms8i7pie9u` |
| Anthropic | `GTM Anthropic (agent brain)` — attached |
| Google Sheets | `My Google connection` — attached |
| Telegram | `goderdzi's Telegram Bot connection` — attached to all four reply modules |

**The webhook must not require an API key.** Telegram sends plain POSTs and
cannot add a custom header, so a hook with API key authentication turned on
rejects every update and the bot goes silent. Make's editor creates
authenticated hooks by default when you add a new one, and Make will not let you
remove the authentication afterwards ("The Header name cannot be changed once
set") — you have to create a fresh unauthenticated hook and point the scenario
at it. Hook `3740894` above is unauthenticated; leave it alone.

`blueprints/01-telegram-expenses.blueprint.json` is the same flow, kept in the
repo so the scenario can be rebuilt or reviewed without opening Make.

## 5. What is left to do

**a. ~~Create the Telegram connection~~ — done.**

Original text kept for reference: The quickest route is from inside the
scenario: open it, click the Telegram bubble *Reply: logged*, and next to
**Connection** choose **Create a connection**. Two fields:

| Field | Value |
|---|---|
| Connection name | `Mukhrani 2026 expenses bot` |
| **Token** | the BotFather token |

Make validates it on Save. Some versions of the dialog label the field
**API Key** — it is the same BotFather token; Telegram has no separate API key,
and the token is never typed into Telegram itself.

Then pick that same connection from the dropdown in the other **three** Telegram
modules: *Reply: where we are*, *Reply: ask*, *Reply: confirm first*. Four
modules in total.

(The other route: Make → **Connections** → **+ Add** → **Telegram Bot**.)

**b. ~~Fill in the owner gate~~ — done.** Module 2 carries `8831217917`, the
Telegram id of @geotacticalmarket. Every other chat stops there.

**c. Fix the Anthropic connection — STILL OPEN.** Connection
`GTM Anthropic (agent brain)` (id `10254078`) holds an API key that Anthropic
now rejects with `401 API key is invalid`. Make cannot fetch the model list for
module 6, so it marks the module unconfigured, the scenario carries
`isinvalid: true`, and **it silently refuses to switch on** — the API reports
"activated" and the scenario stays off.

Make → **Connections** → `GTM Anthropic (agent brain)` → **Edit** → paste a
valid key from console.anthropic.com. Eight other scenarios share this
connection, so they are broken too until it is fixed.

## 6. Point Telegram at Make

Visit this once in a browser, with your token in place of `<TOKEN>`:

```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://hook.eu1.make.com/jok35l9zggg7dqpqt6bzl6ms8i7pie9u
```

You should see `{"ok":true,"result":true,"description":"Webhook was set"}`.

The scenario is already **ON**.

**A note on the plan's active-scenario cap.** Make allows two active scenarios on
this plan, and both slots were taken (*GTM — Order intake* and *GTM — Facebook
post*). *GTM — Facebook post* was paused on 17 September 2026 to make room for
this one. If you want it back, either pause the expense bot or raise the plan.

## 7. Test it — in this order

| Send | Expect |
|---|---|
| `/help` | the command list |
| `/balance` | Budget 625,000 ₾ · spent 217,241.99 ₾ · left 407,758.01 ₾ · 30 records |
| `/blocks 180 0.8` | 1,757 blocks · 17 bags of cement · 2.5 m³ sand |
| `/foundation 180 0.4 0.5` | 37.8 m³ concrete · 257 bags · 1,133 kg rebar |
| `ბეტონი 250 ლარი` | ✅ logged, materials, CAPEX — check the row landed in the sheet |
| `ჯიესენს გადავუხადე 20000 დოლარი` | ❓ a question about the exchange rate, and **no** new row |
| `ჯიესენ გრუპს ავანსი 35000 ლარი` | ⚠️ confirm buttons, and **no** row until you tap |
| From a different Telegram account | nothing at all — no reply, no row |

The two calculator lines must match `construction/Block_Calculator.xlsx` and
`construction/Foundation_Calculator.xlsx` to the digit. If they do not, one of
the two has been changed without the other — see *The calculators* below.

The last one is the important one. If a second account gets a reply, the gate in
module 2 is wrong and you must fix it before using the bot for real.

Delete the `ბეტონი 250 ლარი` test row from the sheet afterwards.

## 8. The calculators

The bot answers three commands with no model call at all:

| Command | Arguments | Defaults | Answers |
|---|---|---|---|
| `/help`, `/start` | — | — | the command list |
| `/blocks` | perimetre, wall height, in metres | `180 0.8` | blocks, cement bags, sand |
| `/foundation` | length, width, depth, in metres | `180 0.40 0.50` | concrete, blinding, gravel, cement, sand, stone, rebar, excavation |

Arguments are optional: `/blocks` on its own uses the greenhouse's own
perimetre. Numbers use a full stop, not a comma — `0.8`, never `0,8`.

**Why no model call.** The Anthropic balance has run dry three times, and each
time it took the whole scenario down with it. Material take-offs are arithmetic;
they do not need a model and must keep working when the credit does not. The
sums live in the reply text of modules 13 and 15 as Make expressions.

**The constants are copies.** Every figure in those expressions is lifted from
the two spreadsheets in `construction/`:

| | Block calculator | Foundation calculator |
|---|---|---|
| Per unit | 11.6144 blocks/m², 0.0141723 m³ mortar/m² | 0.45 m³ sand and 0.85 m³ stone per m³ |
| Cement | 350 kg per m³ of mortar | 320 kg per m³ of concrete **plus** 200 kg per m³ of blinding |
| Waste | 5% blocks, 15% mortar | 5% concrete, 5% steel |
| Assumed | 40×20×20 block, 1 cm joints | 5 cm blinding, 10 cm gravel, 4×Ø12 + Ø8@300, 40 mm cover |

Change one and you must change the other in the same commit, or the bot and the
spreadsheet will quietly give the owner two different orders. That has already
happened once: the bot left the blinding layer's cement out and answered 242
bags where the sheet said 257.

Two things the bot does not do that the spreadsheets do: deduct gate openings
from the wall area, and let you change the block size or the mix. For anything
other than a quick number on site, open the spreadsheet.

The foundation figures are a take-off, not a design. The section and the
reinforcement come from GSN Group's drawings; the reply says so every time.

## 9. Wire the confirm buttons (optional, later)

Out of the box, a confirmation shows buttons but the tap does nothing — you
re-send the expense with the word `დიახ` and it goes through. To make the buttons
live, add a route at the top router filtered on
`{{1.callback_query.data}} = "confirm"` that re-runs the append using the values
carried in `callback_query.message.text`. It is genuinely optional; the manual
path is safe, just slower.

---

## Running cost

| | Per month |
|---|---|
| Make.com | free tier covers this — roughly 6 operations per expense, so ~600 operations for 100 expenses |
| Anthropic API | about USD 0.01 per expense parsed; USD 1–2 a month at any realistic volume. `/balance`, `/blocks` and `/foundation` cost nothing — they never call the model |
| Google Sheets, Telegram | free |

## If something breaks

| Symptom | Cause |
|---|---|
| Bot silent to everyone | Scenario is off, or `setWebhook` did not take — re-check step 6 |
| Bot silent to you only | `<<OWNER_CHAT_ID>>` does not match your chat id |
| "Parse JSON" errors in the run log | The model broke the output contract; open the run, read the raw text, and tighten the prompt |
| Rows land in the wrong columns | The sheet tab was edited — column order must match the CSV template |
| Telegram repeats an update | Make did not return 200 — check the scenario is active and not erroring |
| Bot silent, Make shows no runs at all | The webhook has API key authentication on, or `setWebhook` points at a different hook |
| Cannot switch the scenario on | Either the plan's active-scenario slots are full, or the scenario is flagged `isinvalid` — see below |
| Bot answers `/balance` and the calculators but not free text | The Anthropic balance is empty. The reply says so. Top up at console.anthropic.com → Plans & Billing; nothing else needs touching |
| `Unable to parse range: '<name>'!P2:...` | `sheetId` in module 4 or 8 does not match the tab name character for character |
| `/balance` answers 0 records when the sheet has rows | The read filter points at a column that is blank in every row — see below |

**The blank-column trap.** Google Sheets returns an *empty range* for a column
that is blank in every row, so a filter on that column matches nothing and the
module succeeds with zero rows. No error, no warning — `/balance` just answers
`0.00 ₾ · 0 records` and looks like an empty ledger. The read filter therefore
uses column A (date), which every row has. Column P is written `live` on every
new row so it will be safe to filter on later.

**The invalid-scenario trap.** Make marks a scenario `isinvalid` when any module
fails configuration validation, and then activation quietly does nothing — the
API even replies "Scenario has been activated". Nothing in the editor says
which module is at fault. Four causes hit this scenario on 17 September 2026:

| What | Fix |
|---|---|
| Anthropic API key rejected (401) | re-enter the key on the connection |
| filter operator written as `ne` | use a full operator: `text:notequal` |
| a `mode` field on `google-sheets:filterRows` | remove it — that module has no such field |
| a `messages[]` entry with no `inputType` | add `"inputType": "single"` for a plain string |

To find the cause without guessing, validate each module against the Make API
rather than reading the blueprint.

There is a fifth cause, and it is not a configuration mistake at all: **Make
also flags a scenario `isinvalid` when a module keeps failing at run time.**
An empty Anthropic balance did it on 17, 18 and 21 September — the model call
returned `[400] Your credit balance is too low`, Make gave up on the scenario
and switched it off, and `/balance` died along with it. Re-saving the blueprint
does not clear it while the queued messages are still waiting to fail again.

The fix is in the blueprint now: module 6 carries an error handler that tells
the owner what happened and ends in `builtin:Ignore`, so a model failure costs
one message instead of the whole bot. Keep it. If you ever rebuild the scenario
by hand, rebuild that too — it is the difference between one unparsed expense
and a silent bot nobody notices for a day.
