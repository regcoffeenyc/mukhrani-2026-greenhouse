# Setup — from nothing to a working bot

Ten steps. Everything that needs a password or a tap is yours; everything else
is in this repo. Budget about an hour.

The bot is **running**. Steps 1–6 are the record of how it was built; steps 7–10
are how to test it and what it does. Only step 5c is still open, and the bot
works without it.

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

It exists in Make and is **switched on**, with the Anthropic and Google
connections attached and the ledger id and system prompt filled in:

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

**c. Put credit on the Anthropic account — STILL OPEN, but no longer blocking.**
Connection `GTM Anthropic (agent brain)` (id `10254078`) is attached and its key
is valid. The account behind it has no credit: every call returns
`[400] Your credit balance is too low to access the Anthropic API`. That killed
the whole scenario on 17, 18 and 21 September, which is what section 8 is about.

Since 21 September it no longer stops anything — expenses are still recorded,
without a category. Top up at console.anthropic.com → **Plans & Billing** and
the categories come back on their own; nothing in Make needs touching.

Note that this is the **shop's** Anthropic account, shared with eight other
scenarios. Separating it is `docs/03-separation.md`.

*(An earlier problem on this connection — `401 API key is invalid` on
17 September — was fixed by re-entering the key. If you see a 401 rather than a
400, that is the fix: Make → **Connections** → **Edit** → paste a valid key.)*

## 6. Point Telegram at Make

Visit this once in a browser, with your token in place of `<TOKEN>`:

```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://hook.eu1.make.com/jok35l9zggg7dqpqt6bzl6ms8i7pie9u
```

You should see `{"ok":true,"result":true,"description":"Webhook was set"}`.

The scenario is already **ON**.

**A note on the plan's active-scenario cap.** The cap was two when this was
built, and both slots were taken, so *GTM — Facebook post* was paused on
17 September 2026 to make room. The cap is no longer binding — eleven scenarios
are active — but *GTM — Facebook post* stays off because the owner said on
19 September to leave it off. That is a shop decision, not leftover from this
project: do not switch it back on.

## 7. Test it — in this order

| Send | Expect |
|---|---|
| `/help` | the command list |
| `/balance` | **one** message: spent 220,261.64 ₾ · left 404,738.36 ₾ · 51 records |
| `/blocks 180 0.8` | 1,757 blocks · 17 bags of cement · 2.5 m³ sand |
| `/foundation 180 0.4 0.5` | 37.8 m³ concrete · 257 bags · 1,133 kg rebar |
| `ბეტონი 250 ლარი` | ✅ logged, materials, CAPEX — check the row landed in the sheet |
| `ჯიესენს გადავუხადე 20000 დოლარი` | ❓ a question about the exchange rate, and **no** new row |
| `ჯიესენ გრუპს ავანსი 35000 ლარი` | ⚠️ asked to confirm, and **no** row |
| the same line again with `დიახ` on the end | ✅ now it is written — see section 10 |
| `104 500 ცემენტი` | ❓ told to write the amount without a separator, and **no** row |
| From a different Telegram account | nothing at all — no reply, no row |

The two calculator lines must match `construction/Block_Calculator.xlsx` and
`construction/Foundation_Calculator.xlsx` to the digit. If they do not, one of
the two has been changed without the other — see *The calculators* below.

The last one is the important one. If a second account gets a reply, the gate in
module 2 is wrong and you must fix it before using the bot for real.

Delete the `ბეტონი 250 ლარი` test row from the sheet afterwards.

## 8. What happens when the model is not available

The expense line has two readers, and the second one does not need Anthropic.

**Module 20** reads the message by pattern match, before the model is called,
and cannot fail: it pulls out the first number as the amount, takes what is left
as the description, and sets two safety flags. **Module 6** calls Claude as
before. **Module 22** then picks: the model's answer if there is one, the
pattern match if there is not.

That is why modules 6 and 7 use `builtin:Resume` and not `builtin:Ignore`.
Ignore drops the message; Resume carries on with an empty output so module 22
can fall back. The practical result: an empty Anthropic balance, a rejected key
or a broken JSON reply now costs you the *category*, not the *expense*.

**What the fallback will not do.** It refuses to guess, and writes nothing, in
three cases:

| The message | What comes back |
|---|---|
| no digits at all | write it as description then number |
| a thousands separator — `104 500`, `104,500` | write `104500`; otherwise it would read `104` |
| a foreign currency with no rate — `$`, `დოლარი`, `euro` | send the lari amount, or the rate |

The 10,000 GEL confirm gate still applies. A fallback reading at or above it is
returned for confirmation, exactly as the model's would be.

**Rows written this way need a category.** The fallback cannot classify, so it
writes `other`, confidence `0.5`, channel `telegram-fallback` in column L, and a
note in column Q — and the reply tells you at the time. To find them all later,
filter column L for `telegram-fallback` and set the category by hand before the
month is closed. That column is the only reason those rows are findable, so do
not remove it.

## 9. The calculators

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

## 10. The 10,000 GEL gate

Anything at or above 10,000 GEL is never written on the first message. The bot
replies with what it read and hands back the exact line to send:

```
ცემენტი 104500 დიახ
```

The word `დიახ` in the message is what releases it. Module 20 reads it into
`ok`; module 22 turns `confirm_first` into `log_expense` when it is present —
for the model's decision and the fallback's alike, so the gate behaves the same
whether or not Anthropic is answering.

**This was broken until 21 September 2026 and worth understanding.** The reply
told the owner to re-send with `დიახ`, but nothing anywhere read that word. The
re-send was parsed exactly like the first message, hit the same threshold, and
produced the same reply — forever. No payment at or above 10,000 could be
recorded through the bot at all. It was found trying to log 104,500 GEL, which
is most of a month's spend.

The lesson is not about this one word. A gate is only a gate if something on the
other side opens it; an instruction in a reply is not an implementation. If you
add another confirmation step, wire the exit before you write the prompt.

Buttons would be nicer than a word. To add them, put a route on the top router
filtered on `{{1.callback_query.data}} = "confirm"` that re-runs the append from
the values carried in `callback_query.message.text`. Optional — the word works.

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
| Expenses log but the category is always `other` | The model is not answering — almost always an empty Anthropic balance. The row is still recorded; see section 8. Top up at console.anthropic.com → Plans & Billing |
| `Unable to parse range: '<name>'!P2:...` | `sheetId` in module 4 or 8 does not match the tab name character for character |
| `/balance` answers 0 records when the sheet has rows | The read filter points at a column that is blank in every row — see below |

**How `/balance` works, and the bug that hid in it for five days.**

It does **not** read the ledger row by row. The spent total and the record
count are SUMIF/COUNTIF formulas on a separate **`summary`** tab, and the bot
reads two cells:

| Cell | Formula |
|---|---|
| `summary!A1` | `=SUMIF(Untitled!$P$2:$P,"live",Untitled!$F$2:$F)` |
| `summary!A2` | `=COUNTIF(Untitled!$P$2:$P,"live")` |
| `summary!A3`, `A4` | the same two for `"void"` |

Until 22 September 2026 it used `google-sheets:filterRows` (Search Rows).
**That module emits one bundle per matching row.** Two things followed, and
both were invisible until the ledger got big:

- the reply module fired **once per row** — 51 rows, 51 identical Telegram
  messages;
- `4.array` is not a field on a row bundle, so every reply summed nothing and
  answered `0.00 ₾ · 0 records`.

`/balance` had therefore *never once been right*. The first symptom was
reported on 17 September and misdiagnosed twice — first as a blank-column
problem, then as a void-filter problem — because `0.00 ₾ · 0 records` is
exactly what an empty ledger looks like, and both wrong explanations predicted
it. What finally gave it away was the volume of duplicate messages, which only
a per-row loop can produce.

Two lessons worth keeping. A Make search module is a *loop*, not a query —
if you want one answer, aggregate before you reply. And a wrong number that
equals the empty case is the hardest kind to spot: it looks like no data
rather than bad code.

**Why the sheet does the arithmetic.** It is less code than a Make aggregator,
Google recomputes it the instant a row lands, and the void rule lives in exactly
one place. The cost is that column P must never be blank — module 8 writes
`live` on every append, and fifteen old rows that predated the flag were filled
in on 22 September.

**The blank-column trap (still true, still worth knowing).** Google Sheets
returns an *empty range* for a column that is blank in every row, so a filter
on that column matches nothing and the module succeeds with zero rows. No
error, no warning. That is why column P could not be filtered on until every
row carried a value.

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
