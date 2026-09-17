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

**One thing to do by hand:** open it and rename the first tab to exactly
`expenses` (Google names it after the file on import). The blueprint looks the
tab up by that name and will not find it otherwise.

Do not reorder the columns — the bot writes by position, not by header.

## 4. The scenario — already built

It exists in Make, **switched off**, with the Anthropic and Google connections
already attached and the ledger id and system prompt already filled in:

| | |
|---|---|
| Scenario | **Mukhrani 2026 — Greenhouse expenses (Telegram)**, id `7471723` |
| Webhook URL | `https://hook.eu1.make.com/jok35l9zggg7dqpqt6bzl6ms8i7pie9u` |
| Anthropic | `GTM Anthropic (agent brain)` — attached |
| Google Sheets | `My Google connection` — attached |
| Telegram | **not attached — this is yours to do** |

`blueprints/01-telegram-expenses.blueprint.json` is the same flow, kept in the
repo so the scenario can be rebuilt or reviewed without opening Make.

## 5. What is left to do

**a. Create the Telegram connection.** Make → **Connections** → **+ Add** →
**Telegram Bot** → paste the BotFather token → name it
`Mukhrani 2026 expenses bot` → Save.

Then open the scenario and pick that connection in the three reply modules
(*Reply: where we are*, *Reply: logged*, *Reply: ask*, *Reply: confirm first*).

**b. Fill in the owner gate.** Open module 2 (*Gate + normalise text*), open its
filter, and replace `<<OWNER_CHAT_ID>>` with your numeric chat id from step 2.

Until you do, the filter matches nothing and the bot answers nobody — the safe
failure, and the reason the scenario ships switched off.

**c. Rename the sheet tab** to `expenses`, if you have not already (step 3).

## 6. Point Telegram at Make

Visit this once in a browser, with your token in place of `<TOKEN>`:

```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://hook.eu1.make.com/jok35l9zggg7dqpqt6bzl6ms8i7pie9u
```

You should see `{"ok":true,"result":true,"description":"Webhook was set"}`.

Turn the scenario **ON**.

## 7. Test it — in this order

| Send | Expect |
|---|---|
| `/balance` | Budget 625,000 ₾ · spent 90,541.21 ₾ · left 534,458.79 ₾ |
| `ბეტონი 250 ლარი` | ✅ logged, materials, CAPEX — check the row landed in the sheet |
| `ჯიესენს გადავუხადე 20000 დოლარი` | ❓ a question about the exchange rate, and **no** new row |
| `ჯიესენ გრუპს ავანსი 35000 ლარი` | ⚠️ confirm buttons, and **no** row until you tap |
| From a different Telegram account | nothing at all — no reply, no row |

The last one is the important one. If a second account gets a reply, the gate in
module 2 is wrong and you must fix it before using the bot for real.

Delete the `ბეტონი 250 ლარი` test row from the sheet afterwards.

## 8. Wire the confirm buttons (optional, later)

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
| Anthropic API | about USD 0.01 per expense parsed; USD 1–2 a month at any realistic volume |
| Google Sheets, Telegram | free |

## If something breaks

| Symptom | Cause |
|---|---|
| Bot silent to everyone | Scenario is off, or `setWebhook` did not take — re-check step 6 |
| Bot silent to you only | `<<OWNER_CHAT_ID>>` does not match your chat id |
| "Parse JSON" errors in the run log | The model broke the output contract; open the run, read the raw text, and tighten the prompt |
| Rows land in the wrong columns | The sheet tab was edited — column order must match the CSV template |
| Telegram repeats an update | The scenario did not return 200; check module 12 is still last |
