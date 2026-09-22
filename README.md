# მუხრანი 2026 — სათბური / Mukhrani 2026 — Greenhouse

შპს მუხრანი 2026 (ს/ნ 404801602) · ჰიდროპონიკული სათბური · ბიუჯეტი 625,000 ₾

LLC Mukhrani 2026 (ID 404801602) · hydroponic greenhouse · 625,000 GEL budget

---

## სად ვართ / Where the project stands

| | ₾ | ბიუჯეტიდან / of budget |
|---|---:|---:|
| ბიუჯეტი — კრედიტი / Budget — the credit | 625,000.00 | 100.0% |
| დახარჯული / Spent | 220,061.64 | 35.2% |
| ვალდებული — ხელშ. N1 / Committed — contract N1 | 150,127.20 | 24.0% |
| **დახარჯული ან ვალდებული / Used or committed** | **370,188.84** | **59.2%** |
| **თავისუფალი / Free** | **254,811.16** | **40.8%** |

*22 სექტემბერი 2026 · 30 საბანკო გადარიცხვა + 20 საწვავის ჩასხმა / as at 22 September 2026 —
30 bank payments plus 20 fuel-card fills. ორი საბანკო ჩანაწერი (19 და 21/09) მფლობელის
მონაცემია; საწვავი აპლიკაციიდანაა და ამონაწერში არ ჩანს. Two bank rows (19 and 21 Sep) are
owner-reported; the fuel comes from the fuel app and does not appear in the bank statement.*

## რა დევს აქ / What is here

```
├── finance/          ფინანსური მოდელი — 9-ფურცლიანი Excel + ამგები სკრიპტი
│                     The financial model — a 9-sheet workbook and the script that builds it
├── prompts/          Telegram აგენტის სისტემური პრომპტი
│                     The Telegram agent's system prompt
├── blueprints/       Make.com სცენარი
│                     The Make.com scenario
├── sheets/           ხარჯების ლეჯერის შაბლონი, ფაქტობრივი ჩანაწერებით
│                     The expense ledger template, seeded with the real payments
├── construction/     მასალის კალკულატორები — ბლოკი და საძირკველი
│                     Material calculators — blockwork and foundation
└── docs/             როგორ მუშაობს და როგორ აეწყოს
                      How it works and how to set it up
```

## სამი ნაწილი / Three parts

**ფინანსური მოდელი** (`finance/`) — 2,000 m², წელიწადში ორი მოსავალი, ბანკი ქართუს
625,000 ₾ კრედიტი სააგენტოს თანადაფინანსებით. ბიუჯეტი, სესხის გრაფიკი, თვიური
ფულადი ნაკადი, წლები 1–5, მგრძნობელობა. დეტალები — `finance/README.md`.

**ხარჯების აგენტი** (`prompts/`, `blueprints/`, `sheets/`) — Telegram-ბოტი,
რომელსაც ხარჯს ჩვეულებრივი შეტყობინებით უგზავნით („ბეტონი 1200 ლარი"), ის
შლის მონაცემებად, წერს Google Sheet-ში და პასუხობს იმით, თუ რამდენი დაგრჩათ.
დაყენება — `docs/02-setup.md`.

**მასალის კალკულატორები** (`construction/`) — ორი ცოცხალფორმულიანი Excel:
პერიმეტრის ბლოკის კედელი და ზოლოვანი საძირკველი. იგივე ციფრებს ბოტიც აბრუნებს
ბრძანებებით `/blocks` და `/foundation`.

Two live-formula workbooks — a perimeter blockwork wall and a strip foundation.
The bot returns the same numbers from `/blocks` and `/foundation`, so a quantity
can be checked on site without opening a spreadsheet. The constants are shared
between the two by hand: change one, change the other in the same commit.

The model is the plan; the agent keeps the plan honest by recording what is
actually spent, in the nine categories the model reads; the calculators say
what to order before it is spent.

## ბოტის ბრძანებები / Bot commands

| | |
|---|---|
| `/balance` | ბიუჯეტი, დახარჯული, დარჩენილი / budget, spent, left |
| `/blocks 180 0.8` | ბლოკი, ცემენტი, ქვიშა / blocks, cement, sand |
| `/foundation 180 0.4 0.5` | ბეტონი, ცემენტი, ქვიშა, ღორღი, არმატურა / concrete, cement, sand, stone, rebar |
| `/help` | ბრძანებების სია / the command list |
| ჩვეულებრივი ტექსტი / plain text | ხარჯი იწერება ლეჯერში / the expense is parsed and logged |

ციფრები არასავალდებულოა — უმათოდ პროექტის საკუთარი ზომები გამოიყენება.
თანხა გამყოფის გარეშე დაწერეთ: `104500`, არა `104 500`.

The numbers are optional; without them the project's own dimensions are used.
Write amounts without thousands separators.

მხოლოდ კატეგორიას სჭირდება მოდელი. თუ Anthropic-ის ბალანსი ცარიელია, ხარჯი
მაინც ჩაიწერება — კატეგორიით `other`, რომელიც ხელით უნდა შესწორდეს.

Only the *category* needs the model. If the Anthropic balance is empty the
expense is still recorded, with category `other` and channel `telegram-fallback`
so those rows can be found and classified later. Nothing is ever written that
the bot could not read with confidence — see `docs/02-setup.md` §8.

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
| ხარჯი / Spend | ბანკის ამონაწერი, ანგარიში GE66CR0000009572073602, 01/07–18/09/2026; 19–21/09 მფლობელის მონაცემი |
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
