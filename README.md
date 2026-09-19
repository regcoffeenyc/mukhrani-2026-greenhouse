# მუხრანი 2026 — სათბური / Mukhrani 2026 — Greenhouse

შპს მუხრანი 2026 (ს/ნ 404801602) · ჰიდროპონიკული სათბური · ბიუჯეტი 625,000 ₾

LLC Mukhrani 2026 (ID 404801602) · hydroponic greenhouse · 625,000 GEL budget

---

## სად ვართ / Where the project stands

| | ₾ | ბიუჯეტიდან / of budget |
|---|---:|---:|
| ბიუჯეტი — კრედიტი / Budget — the credit | 625,000.00 | 100.0% |
| დახარჯული / Spent | 102,741.99 | 16.4% |
| ვალდებული — ხელშ. N1 / Committed — contract N1 | 255,663.20 | 40.9% |
| **დახარჯული ან ვალდებული / Used or committed** | **358,405.19** | **57.3%** |
| **თავისუფალი / Free** | **266,594.81** | **42.7%** |

*18 სექტემბერი 2026-ის ბანკის ამონაწერით, 28 გადარიცხვა / as at the bank statement of 18 September 2026, 28 payments*

## რა დევს აქ / What is here

```
├── finance/          ფინანსური მოდელი — 9-ფურცლიანი Excel + ამგები სკრიპტი
│                     The financial model — a 9-sheet workbook and the script that builds it
├── prompts/          Telegram აგენტის სისტემური პრომპტი
│                     The Telegram agent's system prompt
├── blueprints/       Make.com სცენარი
│                     The Make.com scenario
├── sheets/           ხარჯების ლეჯერის შაბლონი, 15 ფაქტობრივი ჩანაწერით
│                     The expense ledger template, seeded with the 15 real payments
└── docs/             როგორ მუშაობს და როგორ აეწყოს
                      How it works and how to set it up
```

## ორი ნაწილი / Two parts

**ფინანსური მოდელი** (`finance/`) — 2,000 m², წელიწადში ორი მოსავალი, ბანკი ქართუს
625,000 ₾ კრედიტი სააგენტოს თანადაფინანსებით. ბიუჯეტი, სესხის გრაფიკი, თვიური
ფულადი ნაკადი, წლები 1–5, მგრძნობელობა. დეტალები — `finance/README.md`.

**ხარჯების აგენტი** (`prompts/`, `blueprints/`, `sheets/`) — Telegram-ბოტი,
რომელსაც ხარჯს ჩვეულებრივი შეტყობინებით უგზავნით („ბეტონი 1200 ლარი"), ის
შლის მონაცემებად, წერს Google Sheet-ში და პასუხობს იმით, თუ რამდენი დაგრჩათ.
დაყენება — `docs/02-setup.md`.

The model is the plan; the agent keeps the plan honest by recording what is
actually spent, in the seven categories the model reads.

## დაწყება / Getting started

| გინდათ / You want | წაიკითხეთ / Read |
|---|---|
| ბიუჯეტის ნახვა / to see the budget | `finance/Greenhouse_CashFlow_2000m2.xlsx`, ფურცელი `Budget` |
| ბოტის აწყობა / to set up the bot | `docs/02-setup.md` |
| როგორ მუშაობს / to understand how it works | `docs/01-architecture.md` |
| მოდელის თავიდან აგება / to rebuild the model | `finance/README.md` |

## წყაროები / Sources

ყველა ციფრი დოკუმენტიდანაა, არა დაშვებიდან. Every figure traces to a document.

| | |
|---|---|
| ბიუჯეტი / Budget | სესხის ხელშეკრულება GA/1-876787–001, 17/06/2026, სს „ბანკი ქართუ" |
| ხარჯი / Spend | ბანკის ამონაწერი, ანგარიში GE66CR0000009572073602, 01/07–18/09/2026 |
| ხელშეკრულება N1 / Contract N1 | შპს ჯიესენ გრუპი, 7/6/2026, 125,000 $ |
| კურსი / FX 2.6384 | 09/07/2026 გადარიცხვის დანიშნულება / stated in the payment description |

მოსავლიანობა, ფასები და OPEX მფლობელის მონაცემია და მოდელში ყვითლად არის
მონიშნული. Yield, prices and OPEX come from the owner and are marked yellow in
the workbook.

## უსაფრთხოება / Security

ეს რეპოზიტორია **პრივატულია** — შიგნით საბანკო ანგარიში, სესხის პირობები და
კონტრაგენტებია. არასდროს ჩადოთ აქ: Telegram-ბოტის ტოკენი, Anthropic-ის API
გასაღები, Make-ის კავშირები, ბანკის წვდომა.

This repository is **private**: it carries the bank account, the loan terms and
the counterparties. Never commit the Telegram bot token, the Anthropic API key,
Make connection details, or anything that opens the bank.

## სამი ცალკე საქმე / Three separate jobs

gdsff.com, geotacticalmarket.com და ეს სათბურის პროექტი სამი სხვადასხვა საქმეა.
არაფერი გადადის ერთიდან მეორეში — არც ფაილი, არც ფაქტი, არც ინფრასტრუქტურა, არც
ანგარიში.

gdsff.com, geotacticalmarket.com and this greenhouse project are three different
jobs. Nothing crosses between them — not files, not facts, not infrastructure, not
bills. The Make automation currently breaks that rule and is being moved out;
`docs/03-separation.md` says what went wrong and how it gets fixed.
