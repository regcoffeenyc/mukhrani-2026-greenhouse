# Keeping this project out of the shop

**The rule, set by the owner on 19 September 2026: gdsff.com, geotacticalmarket.com
and this greenhouse project are three different jobs. Nothing crosses between them —
not files, not facts, not infrastructure, not bills.**

The financial model never crossed: its own repository, its own Google Sheet, its own
bank statements. Only the Make automation did. This says exactly how to undo that.

## What is actually shared today

Checked against the live account on 22 September 2026.

| | |
|---|---|
| Organisation | `My Organization`, id `8279570`, **Core** plan, 10,000 operations a month |
| Team | `My Team`, id `2090805` — **the only one** |
| Greenhouse scenario | `7471723` — Mukhrani 2026 — Greenhouse expenses (Telegram) |
| Its webhook | `3740894` |

Everything in that one team: the shop's scenarios, GDSFF's scenarios and the
greenhouse bot, side by side. The greenhouse bot uses three connections:

| Connection | id | Also used by |
|---|---|---|
| `goderdzi's Telegram Bot connection` | `11015664` | **nothing else** — already exclusive |
| `My Google connection` | `8844591` | 8 other scenarios (shop + FBA) |
| `GTM Anthropic (agent brain)` | `10254078` | 7 other scenarios (shop + GDSFF) |

So only two things genuinely cross: **Google and Anthropic**. That is what caused
the real damage — on 18 September the Anthropic account hit zero and the greenhouse
bot and eight shop scenarios failed in the same minute, on one bill.

## The constraint that decides the shape of the fix

**The Core plan allows one team per organisation** (`license.teams: 1`). A second
team inside `My Organization` is therefore not possible without paying for a bigger
plan. Separation means a **second organisation**.

Make's API refuses to create one — `organizations_create` returns
`Organization-bound request can't be used outside of the Organization Context`,
confirmed again on 22 September. So step 1 has to be done by hand in a browser.
Everything after it can be rebuilt from this repository.

A new organisation starts on the **Free** plan: 1,000 operations a month. The bot
costs about 6 operations per expense logged and 5 per `/balance`, so 1,000 covers
roughly 150 expenses a month. Nothing needs to be paid for.

## The steps

### 1. Create the organisation — in the browser

Make → the organisation switcher, top left → **+ Create a new organization**.

| Field | Value |
|---|---|
| Name | `Mukhrani 2026 — Greenhouse` |
| Region | EU (`eu1.make.com`, same as the current one) |
| Country | Georgia |
| Timezone | Asia/Tbilisi |

### 2. Build three connections inside the new organisation

None of these may be shared with the shop. That is the entire point.

| Connection | What it needs |
|---|---|
| Telegram Bot | the BotFather token for the existing bot |
| Google | sign in as the account that owns the ledger spreadsheet |
| Anthropic Claude | a key from a **separate workspace** — see below |

**On the Anthropic key.** A second key on the same Anthropic account still draws on
the same balance, so a key alone does not separate the bills. Create a **workspace**
in the Anthropic console for the greenhouse, give it its own spend limit, and issue
the key inside that workspace. Then the greenhouse can never again exhaust the
shop's credit, or the other way round.

**On the Google connection.** The cleanest separation is a Google account that owns
nothing but the greenhouse ledger. At minimum it must be a *separate connection* in
the new organisation, even if it signs in as the same person — otherwise the shop's
scenarios and the greenhouse share one OAuth grant.

### 3. Import the scenario

`blueprints/01-telegram-expenses.blueprint.json` is the working flow. Import it into
the new organisation and replace three placeholders:

| Placeholder | Value |
|---|---|
| `<<OWNER_CHAT_ID>>` | module 2 — the owner's Telegram chat id |
| `<<LEDGER_SPREADSHEET_ID>>` | modules 4, 24 and 8 |
| `<<LEDGER_TAB_NAME>>` | module 8 — the tab name, not the file name |

Modules 4 and 24 read `summary!A1` and `summary!A2` and carry the sheet name
`summary` already; only the spreadsheet id needs filling.

Then paste the system prompt into module 6 from `prompts/00-conventions.md`
followed by `prompts/01-expense-agent.md`, and attach the three new connections —
**seven** modules need one: 4, 24, 8 (Google), 5, 9, 10, 11, 13, 15, 16, 23
(Telegram), 6 (Anthropic).

### 4. Move the webhook

The new organisation creates its own webhook with its own URL. Telegram must be told,
once, in a browser:

```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=<THE NEW HOOK URL>
```

The new hook must have **no API key authentication** — Telegram sends plain POSTs and
cannot add a header, and Make will not let you remove the authentication once set.
See `docs/02-setup.md`; this cost an evening the first time.

### 5. Test before deleting anything

Send `/balance` — one message, spent and record count matching the Budget sheet.
Then log a small expense and check the row lands. Only then go on.

### 6. Close the old one

1. Delete scenario `7471723` from the shop organisation.
2. Delete hook `3740894`.

**Do not switch `GTM — Facebook post` (`7191121`) back on.** The owner was asked on
19 September and said to leave it off. It is a shop decision, made deliberately, not
an oversight left behind by this migration.

## After the move

| | Geo Tactical Market | Mukhrani 2026 |
|---|---|---|
| Make organisation | `My Organization` (8279570) | `Mukhrani 2026 — Greenhouse` |
| Anthropic | shop key | greenhouse workspace, own spend limit |
| Google | `My Google connection` | its own |
| Telegram | — | its own bot connection |
| Repository | `regcoffeenyc-tactical-shop-agents` | `mukhrani-2026-greenhouse` |
| Bank | shop accounts | GE66CR0000009572073602 |

Neither can switch the other off, exhaust the other's credit, or read the other's
data. If a future task seems to need something from the other side, that is the
signal to stop and ask — not to reach across.

## One thing this does not fix

GDSFF is in that same team too — `GDSFF — Facebook post`, `GDSFF — Facebook comments`,
`GDSFF — Caption Agent`, and an IMAP/SMTP mailbox at `office@gdsff.org` that three
**shop** scenarios use to send and read mail. By the owner's own rule that is the
same violation, in the same place, one job over. Moving the greenhouse out does not
touch it. It is worth deciding whether GDSFF gets its own organisation too, or
whether the shop stops using the federation's mailbox.
