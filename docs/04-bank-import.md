# სად ჩერდება ლეჯერი / Where the ledger stands against the bank

ლეჯერი ცხოვრობს Google Sheet-ში, არა ამ რეპოზიტორიაში. ეს ფაილი მხოლოდ ერთ
კითხვას პასუხობს: რომელ თარიღამდეა ამონაწერი შეტანილი და სად იწყება შემდეგი
შემოტანა.

The ledger lives in the Google Sheet, not in this repository. This file answers
one question: how far the bank statement has been imported, and where the next
import starts.

## ანგარიში / The account

GE66CR0000009572073602 (GEL) · შპს მუხრანი 2026 · სს „ბანკი ქართუ"
სესხი / credit line GA/1-876787-001, 17/06/2026, 625,000 ₾

## შემოტანის ჟურნალი / Import log

| ამონაწერი / Statement | შემოტანილია / Imported | ჩანაწერი / Rows |
|---|---|---|
| 01/07–18/09/2026 | 09/09 და 18/09/2026 | 28 |
| 19–21/09/2026 — მფლობელის მონაცემი / owner-reported | 21/09/2026 | 2 |
| 20/07–08/10/2026 (მოიცავს გამოტოვებულს / filled the gaps) | 09/10/2026 | 23 |
| 13/10–22/10/2026 | 26/10/2026 | 12 |

**ლეჯერი სრულია 22/10/2026-ის ჩათვლით.** შემდეგი შემოტანა 23/10/2026-დან
იწყება. / **The ledger is complete through 22 October 2026.** The next import
starts at 23 October.

26/10/2026-ის ამონაწერი (04/08–26/10) ზუსტად შედგა: 110 ხაზი, დებეტი
199,246.03 ₾, კრედიტი 213,583.00 ₾, ნაშთი 16,147.12 → 30,484.09 ₾, ყველა ხაზი
მიმდევრობით გადამოწმებული. / The 26 October statement (4 August to 26 October)
parses exactly: 110 lines, 199,246.03 GEL debit, 213,583.00 GEL credit, running
balance 16,147.12 → 30,484.09 with no line out of step.

## წესები / The conventions an import follows

- **საკომისიოები აგრეგირდება.** ერთი ჩანაწერი პერიოდზე, კონტრაგენტი „სს ბანკი
  ქართუ", შენიშვნაში გადარიცხვების რაოდენობა. / **Transfer commissions are
  aggregated** into one row per period rather than one row per 90-tetri charge.
- **ავანსი ხარჯი არ არის.** სვეტი `void` = `advance`; summary ფურცელი მას
  დახარჯულში არ ითვლის. რასაც ავანსი მოხმარდა, ცალკე იწერება. / **An advance is
  not an expense.** Column `void` reads `advance` and the summary tab keeps it out
  of the spend total; what it buys is recorded separately as receipts arrive.
- **ჩანაწერი არ იშლება.** შეცდომა `void`-ად მოინიშნება. / **A row is never
  deleted** — a wrong one is flagged `void`.
- **ბანკის დანიშნულება მართალია.** თუ ბანკი წერს „ხელფასი", ისე იწერება, თუნდაც
  ეჭვი იყოს, რომ ავანსია; ეჭვი შენიშვნაში ჩერდება. / **The bank's own wording
  wins.** If the statement says salary, the row says salary; any doubt goes in the
  note, not into a reclassification nobody asked for.

## რით გადამოწმდება / The check that proves the import

დახარჯული + ავანსის აუთვისებელი ნაწილი − ჩანაწერები გადახდის ხერხის გარეშე
= ანგარიშიდან გასული თანხა. 26/10/2026-ზე: 261,618.56 + 6,980.35 − 450.00 =
268,148.91 ₾.

Spend, plus the unaccounted part of the director's advance, less the rows with no
payment method, equals the total paid out of the account. At 26 October 2026:
261,618.56 + 6,980.35 − 450.00 = 268,148.91 GEL.

ამისგან 199,246.03 ₾ 04/08-ის შემდეგ ამონაწერშია, 68,902.88 ₾ — მის დაწყებამდე
(ივლისის ამონაწერი, 68,714.69 ₾ ცალკეული ჩანაწერით და 188.19 ₾ აგრეგირებულ
საკომისიოებში). / Of that, 199,246.03 sits in the statement from 4 August onward
and 68,902.88 predates it — the July statement, 68,714.69 in named rows plus
188.19 of July commissions that sit inside the aggregated fee rows.

საწვავი (3,019.65 ₾, ბარათით) ამ ჯამში არ შედის და არც უნდა შედიოდეს: ის
ავანსიდან დაფინანსდა. / The fuel, 3,019.65 paid by card, is outside that total
and belongs outside it: it was funded from the advance.

## სესხი / The credit line

| ათვისება / Drawdown | თანხა / Amount | საკომისიო / Fee |
|---|---:|---:|
| 25/08/2026 | 10,000.00 | 20.00 |
| 14/09/2026 | 30,000.00 | 60.00 |
| 21/09/2026 | 105,000.00 | 210.00 |
| 06/10/2026 | 50,000.00 | 100.00 |
| **ათვისებული / Drawn** | **195,000.00** | **390.00** |

აუთვისებელი / undrawn: 430,000.00 ₾.

## ღია საკითხები / Open questions

1. **450 ₾ შეიძლება ორჯერ ითვლებოდეს.** 24/09-ის ორი ტელეგრამ-ჩანაწერი (ცემენტი
   150 + 300, ხერხი `unknown`) შეიძლება იგივე იყოს, რაც 25/09-ის საბანკო 435 ₾.
   / The two Telegram cement rows of 24 September may be the same cement as the
   435 GEL bank row of 25 September. If so, flag the duplicate `void`.
2. **20/10-ის 5,000 ₾.** ბანკი წერს „ხელფასი", ანგარიში იგივეა, რომელზეც
   21/09-ის 10,000 ₾ ავანსი გავარდა. ხელფასად ჩაიწერა; თუ ნაწილი ავანსია,
   შესწორება ხელით. / The bank calls it salary and it went to the same account as
   the 10,000 advance of 21 September. Recorded as salary; correct it by hand if
   part of it is a further advance.
3. **18,583.00 ₾ დაბრუნება 16/10-ს.** ხაზინამ ზედმეტად გადახდილი თანხა
   დააბრუნა. ლეჯერი ხარჯების ლეჯერია და შემოსავალს არ იცნობს, ამიტომ ჩანაწერი
   არ გაკეთდა — წმინდა ხარჯი ამ თანხით ნაკლებია. / On 16 October the Treasury
   refunded 18,583.00 of overpaid tax. The ledger records expenses only and has no
   row shape for money coming back, so nothing was written: net cost is lower than
   the spend total by that amount. Decide whether the ledger should carry refunds.
4. **ტექნიკური ოთახი.** 10,000 $ ხელშეკრულების ნომერი ჯერ უცნობია; გადახდა არ
   ჩანს. / The 10,000 USD technical-room contract still has no reference and no
   payment against it.

## `sheets/expenses-ledger-template.csv`

შაბლონი 51 ჩანაწერზე გაიყინა (22/09/2026). ცოცხალ ფურცელში 90-ია. შაბლონი
ახალი ლეჯერის დასაწყებად არის, არა ასლისთვის — ციფრს ყოველთვის ფურცელს ან
`/balance`-ს ჰკითხეთ.

The template froze at 51 rows on 22 September; the live sheet now has 90. It
exists to seed a ledger, not to mirror one — for a figure, ask the sheet or
`/balance`.
