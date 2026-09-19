# Keeping this project out of the shop

**The rule, set by the owner on 19 September 2026: gdsff.com, geotacticalmarket.com
and this greenhouse project are three different jobs. Nothing crosses between them —
not files, not facts, not infrastructure, not bills.**

This document exists because the greenhouse bot broke that rule, and says how it gets
fixed.

## What went wrong

The expense bot was built inside the Geo Tactical Market Make organisation, because
that is where a Make account already existed. Three consequences followed, none of
them intended:

**It took the shop's scenario slot.** The plan allows two active scenarios. On
17 September `GTM — Facebook post` was switched off to make room for the greenhouse
bot, and stayed off. A greenhouse job disabled a shop automation.

**It spends the shop's Anthropic credit.** The bot calls Claude through connection
`GTM Anthropic (agent brain)` — the shop's API key. On 18 September that account hit
zero and the greenhouse bot and eight shop scenarios failed in the same minute, for
the same reason, on one bill.

**It reads through the shop's Google connection.** `My Google connection` is the
account the shop's order book and audit sheets run on. The greenhouse ledger has no
business being reachable from it.

The financial model was never mixed: it has its own repository, its own Google Sheet
and its own bank statements. Only the Make automation crossed over.

## The fix

A separate Make organisation, holding nothing but this project.

Make's API refuses to create an organisation from outside an organisation context
(`Organization-bound request can't be used outside of the Organization Context`), so
the first step has to be done by hand in the browser. The rest can be rebuilt from
this repository.

### 1. Create the organisation — in the Make UI

Make → the organisation switcher, top left → **+ Create a new organization**.

| Field | Value |
|---|---|
| Name | `Mukhrani 2026 — Greenhouse` |
| Region | EU |
| Country | Georgia |
| Timezone | Asia/Tbilisi |

A new organisation starts on the Free plan: 1,000 operations a month and two active
scenarios. The bot costs about six operations per expense logged, so 1,000 covers
roughly 160 expenses a month — far more than this project will produce. Nothing needs
to be paid for.

### 2. Build the connections — three, all inside the new organisation

None of these may be shared with the shop. That is the entire point.

| Connection | What it needs |
|---|---|
| Telegram Bot | the BotFather token for @Mukhrani2026bot |
| Google | sign in as the account that owns the ledger spreadsheet |
| Anthropic Claude | an API key **that is not the shop's** — see below |

**On the Anthropic key.** A second key on the same Anthropic account still draws on
the same balance, so a key alone does not separate the bills. To separate them
properly, create a **workspace** in the Anthropic console for the greenhouse, give it
its own spend limit, and issue the key inside that workspace. Then the greenhouse can
never again exhaust the shop's credit, or the other way round.

### 3. Import the scenario

`blueprints/01-telegram-expenses.blueprint.json` in this repository is the working
flow. Import it into the new organisation and replace three placeholders:

| Placeholder | Value |
|---|---|
| `<<OWNER_CHAT_ID>>` | `8831217917` |
| `<<LEDGER_SPREADSHEET_ID>>` | `1NULNFpgxhzAqM7IWPr8-gxtRbqQ4MxMXgyNwrDzktLE` |
| `<<LEDGER_TAB_NAME>>` | `Untitled` — the tab name, not the file name; check it in the Sheet Name dropdown rather than assuming |

Then paste the system prompt into module 6 from `prompts/00-conventions.md` followed
by `prompts/01-expense-agent.md`, and attach each of the three new connections.

### 4. Move the webhook

The new organisation creates its own webhook with its own URL. Telegram must be told,
once, in a browser:

```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=<THE NEW HOOK URL>
```

The new hook must have **no API key authentication** — Telegram sends plain POSTs and
cannot add a header. See `docs/02-setup.md`; this cost an evening the first time.

### 5. Close the old one

Only once the new bot answers `/balance` correctly:

1. Delete scenario `7471723` from the shop organisation.
2. Delete hook `3740894`.

That frees the shop's second scenario slot. **Do not switch `GTM — Facebook post`
(`7191121`) back on to fill it.** The owner was asked on 19 September and said to
leave it off for now. It is a shop decision, made deliberately, not an oversight
left behind by this migration — leave it alone until the owner says otherwise.

## After the move

| | Geo Tactical Market | Mukhrani 2026 |
|---|---|---|
| Make organisation | `My Organization` (8279570) | `Mukhrani 2026 — Greenhouse` |
| Anthropic | shop key | greenhouse workspace, own spend limit |
| Google | `My Google connection` | its own |
| Repository | `regcoffeenyc-tactical-shop-agents` | `mukhrani-2026-greenhouse` |
| Bank | shop accounts | GE66CR0000009572073602 |

Neither can switch the other off, exhaust the other's credit, or read the other's
data. If a future task seems to need something from the other side, that is the
signal to stop and ask — not to reach across.
