# მუხრანი 2026 — სათბური / Mukhrani 2026 — Greenhouse

შპს მუხრანი 2026 (ს/ნ 404801602) · ჰიდროპონიკული სათბური · ბიუჯეტი 625,000 ₾

LLC Mukhrani 2026 (ID 404801602) · hydroponic greenhouse · 625,000 GEL budget

---

## სად ვართ / Where the project stands

| | ₾ | ბიუჯეტიდან / of budget |
|---|---:|---:|
| ბიუჯეტი — კრედიტი / Budget — the credit | 625,000.00 | 100.0% |
| დახარჯული / Spent | 313,618.56 | 50.2% |
| ავანსი დირექტორზე, ანგარიშგების გარეშე / Advance not yet accounted | 6,980.35 | 1.1% |
| ვალდებული — ხელშეკრულებები / Committed — contracts | 121,525.65 | 19.4% |
| **დახარჯული ან ვალდებული / Used or committed** | **442,124.56** | **70.7%** |
| **თავისუფალი / Free** | **182,875.44** | **29.3%** |

*26 ოქტომბერი 2026 · 66 საბანკო ჩანაწერი + 21 საწვავი + 2 გადახდის ხერხის გარეშე ·
ანგარიშის ნაშთი 30,484.09 ₾ / as at 26 October 2026 — 65 bank rows, 21 fuel entries and
2 rows with no payment method; the account itself stood at 30,484.09 GEL at 09:55 that
morning. და მას შემდეგ, 26/10-ს, ჯიესენზე 52,000 ₾ გავიდა — მფლობელის
მონაცემით, შემდეგ ამონაწერით დასადასტურებელი. / A further 52,000 GEL went to GSN
on 26 October on the owner's word, to be confirmed by the next statement. The
account itself held only 30,484.09 that morning, so a drawdown should appear
beside it. Two September bank rows are owner-reported; the fuel comes from the
fuel app and does not appear in the bank statement. The import log is in
`docs/04-bank-import.md`.*

**შემოწმება / The reconciliation that ties it together.** დახარჯული + ავანსის
აუთვისებელი ნაწილი − ორი ჩანაწერი გადახდის ხერხის გარეშე = 313,618.56 + 6,980.35
− 450.00 = **320,148.91 ₾**. ამისგან 268,148.91 ₾ ამონაწერებით დასტურდა
22/10-ის ჩათვლით, 52,000 ₾ — ტერიტორიალურია. / Spend plus the unaccounted part
of the advance, less the two rows that have no payment method, equals 320,148.91
GEL. Of that, 268,148.91 is confirmed by statements through 22 October and the
52,000 of 26 October is still on the owner's word alone. The fuel adds nothing on top
because all of it was funded from the advance: 2,819.65 was paid personally before
21 September and repaid out of it, and 200 came from it directly. Nothing is owed
to the director.

ის ორი ჩანაწერი (24/09, ცემენტი 150 + 300 ₾, ტელეგრამიდან, ხერხი `unknown`) შეიძლება
იგივე ცემენტი იყოს, რაც 25/09-ის საბანკო ჩანაწერში 435 ₾-ად დევს. თუ ასეა, 450 ₾
ორჯერ ითვლება და ზედმეტი `void`-ად უნდა მოინიშნოს. / Those two rows — 24 September,
cement for 150 and 300 GEL, logged from Telegram with method `unknown` — may be the
same cement that the bank row of 25 September records as 435 GEL. If they are, 450 GEL
is counted twice and the duplicate should be flagged `void`. It is the one open
question in the figures above.

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
| სად ჩერდება ლეჯერი ამონაწერში / where the ledger stands against the bank | `docs/04-bank-import.md` |
| რა წერია ჯიესენის ხელშეკრულებაში / what the GSN contract actually says | `docs/05-contract-n1.md` |

## წყაროები / Sources

ყველა ციფრი დოკუმენტიდანაა, არა დაშვებიდან. Every figure traces to a document.

| | |
|---|---|
| ბიუჯეტი / Budget | სესხის ხელშეკრულება GA/1-876787–001, 17/06/2026, სს „ბანკი ქართუ" |
| ხარჯი / Spend | ბანკის ამონაწერი, ანგარიში GE66CR0000009572073602, 01/07–22/10/2026; 19 და 21/09 მფლობელის მონაცემი / bank statements for the account, 1 July to 22 October 2026; the 19 and 21 September rows are owner-reported |
| საწვავი / Fuel | Gulf-ის აპლიკაცია, 02/07–22/09/2026 — ბარათით, ამონაწერში არ ჩანს / the Gulf fuel app, paid by card and absent from the bank statement |
| ხელშეკრულება N1 / Contract N1 | შპს ჯიესენ გრუპი (ს/კ 406230528), 7/6/2026, 125,000 $ **დღგ-ს გარეშე** — სათბური; პირობები `docs/05-contract-n1.md` / the greenhouse, price **excluding VAT**; terms in `docs/05-contract-n1.md` |
| ტექნიკური ოთახი / Technical room | შპს ჯიესენ გრუპი, 10,000 $ — 200 მ², პერიმეტრის ბეტონი და ბლოკი; ნომერი დასადასტურებელია / contract reference to be confirmed |
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
