#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the greenhouse cash-flow model (2,000 m2, two harvest cycles, USD 140k bank loan)."""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment

OUT = str(Path(__file__).with_name("Greenhouse_CashFlow_2000m2.xlsx"))

F = "Arial"
TITLE = Font(name=F, size=14, bold=True, color="1F4E79")
H1 = Font(name=F, size=11, bold=True, color="FFFFFF")
SEC = Font(name=F, size=10, bold=True, color="1F4E79")
TXT = Font(name=F, size=10)
BOLD = Font(name=F, size=10, bold=True)
INP = Font(name=F, size=10, color="0000FF")            # hardcoded input
INPB = Font(name=F, size=10, bold=True, color="0000FF")
LNK = Font(name=F, size=10, color="008000")            # link to another sheet
LNKB = Font(name=F, size=10, bold=True, color="008000")
NOTE = Font(name=F, size=9, italic=True, color="808080")

FILL_H = PatternFill("solid", fgColor="1F4E79")
FILL_SEC = PatternFill("solid", fgColor="D9E1F2")
FILL_KEY = PatternFill("solid", fgColor="FFFF00")
FILL_TOT = PatternFill("solid", fgColor="F2F2F2")

THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
TOPLINE = Border(top=Side(style="thin", color="000000"))

GEL = '#,##0;(#,##0);"-"'
GEL2 = '#,##0.00;(#,##0.00);"-"'
KG = '#,##0;(#,##0);"-"'
PCT = '0.0%;(0.0%);"-"'
PCT2 = '0.00%'
MULT = '0.00x'

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTHS_KA = ["იან", "თებ", "მარ", "აპრ", "მაი", "ივნ",
             "ივლ", "აგვ", "სექ", "ოქტ", "ნოე", "დეკ"]

wb = Workbook()


def put(ws, cell, value, font=TXT, fmt=None, fill=None, align=None, border=None):
    c = ws[cell]
    c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if align:
        c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=False)
    if border:
        c.border = border
    return c


def section(ws, row, text, last_col="N"):
    for col in range(1, ws.max_column + 2):
        pass
    ws.cell(row=row, column=1).value = text
    ws.cell(row=row, column=1).font = SEC
    for i in range(1, ord(last_col) - ord("A") + 2):
        ws.cell(row=row, column=i).fill = FILL_SEC


# =====================================================================
# 1. INSTRUCTIONS
# =====================================================================
ws = wb.active
ws.title = "Instructions"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 46
ws.column_dimensions["C"].width = 78

put(ws, "B2", "სათბურის ფულადი ნაკადები / GREENHOUSE CASH-FLOW MODEL", TITLE)
put(ws, "B3", "2,000 m² · წელიწადში 2 მოსავალი / two harvest cycles per year · საბანკო სესხი / bank loan USD 140,000", NOTE)

rows = [
    ("", ""),
    ("როგორ ვიმუშაოთ / HOW TO USE", ""),
    ("1. Assumptions", "ყველა დაშვება აქ იცვლება. მხოლოდ ლურჯი და ყვითელი უჯრები შეავსეთ. / All drivers live here. Edit ONLY the blue and yellow cells."),
    ("2. OPEX", "150,000 GEL წლიური ხარჯის დაშლა 8 კატეგორიად + სეზონურობა თვეების მიხედვით. / The 150,000 GEL annual OPEX split into 8 categories with monthly seasonality."),
    ("Loan", "625,000 ₾ კრედიტის 120-თვიანი გრაფიკი სააგენტოს თანადაფინანსებით, ბანკის დანართ #1-თან შედარებით. / The 120-month schedule of the 625,000 GEL credit with the agency co-financing, checked against the bank Annex 1."),
    ("4. CF_Monthly", "წელი 1 — თვიური ფულადი ნაკადი (იან–დეკ). მთავარი ცხრილი. / Year 1 monthly cash flow (Jan–Dec). The main statement."),
    ("5. Annual", "წლები 1–5 — შემოსავალი, EBITDA, ვალის მომსახურება, DSCR. / Years 1–5 summary: revenue, EBITDA, debt service, DSCR."),
    ("6. Sensitivity", "ფასისა და მოსავლიანობის მგრძნობელობა + წაგება-მოგების ზღვარი. / Price & yield sensitivity plus break-even."),
    ("7. Actuals", "შპს მუხრანი 2026-ის ბანკის ამონაწერი — ფაქტობრივი გადარიცხვები 01/07–08/09/2026. / LLC Mukhrani 2026 bank statement — actual payments 1 Jul – 8 Sep 2026."),
    ("Budget", "ბიუჯეტი 625,000 ₾ და სად ვართ: დახარჯული, ვალდებული, თავისუფალი ნაშთი, ხარჯი კატეგორიებად და თვეებად. / The 625,000 GEL budget and where it stands: spent, committed, free, by category and by month."),
    ("", ""),
    ("ფერების ლეგენდა / COLOUR LEGEND", ""),
]
r = 5
for a, b in rows:
    put(ws, f"B{r}", a, SEC if a and not a[0].isdigit() else BOLD)
    put(ws, f"C{r}", b, TXT)
    r += 1

legend = [
    ("ლურჯი ციფრი / Blue number", "ხელით შეყვანილი დაშვება — შეცვალეთ თავისუფლად. / Hardcoded input — edit freely."),
    ("ყვითელი ფონი / Yellow fill", "კრიტიკული დაშვება, გადაამოწმეთ. / Key assumption, verify before use."),
    ("შავი ციფრი / Black number", "ფორმულა — ნუ შეცვლით. / Formula — do not overwrite."),
    ("მწვანე ციფრი / Green number", "სხვა ფურცელზე მიბმული ფორმულა. / Link to another sheet."),
]
r += 0
for a, b in legend:
    put(ws, f"B{r}", a, INPB if "ლურჯი" in a else (BOLD if "შავი" in a else (LNKB if "მწვანე" in a else BOLD)))
    if "ყვითელი" in a:
        ws[f"B{r}"].fill = FILL_KEY
    put(ws, f"C{r}", b, TXT)
    r += 1

r += 1
put(ws, f"B{r}", "წყაროები და დაშვებები / SOURCES & ASSUMPTIONS", SEC)
r += 1
src = [
    ("ფართობი / Area — 2,000 m²", "მომხმარებლის მონაცემი / Given by the user."),
    ("ციკლები / Cycles — 2 per year", "მომხმარებლის მონაცემი / Given by the user."),
    ("ზამთრის მოსავალი / Winter harvest — 85 t (80–90 range)",
     "მომხმარებელმა მიუთითა „80-90 kg\". 2,000 m²-ზე ეს ფიზიკურად ტონებია (42.5 kg/m²), ამიტომ მოდელში ჩადებულია 85 ტონა (80–90-ის შუალედი). თუ სხვა რიცხვია — შეცვალეთ Assumptions!B10. / User wrote \"80-90 kg\"; for 2,000 m² this can only mean tonnes (42.5 kg/m²), so 85 t (mid-range) is used. Correct Assumptions!B10 if the intent differed."),
    ("ზამთრის ფასი / Winter price — 4.50 GEL/kg", "მომხმარებლის მონაცემი / Given by the user."),
    ("ზაფხულის მოსავალი / Summer harvest — 70 t", "მომხმარებლის მონაცემი / Given by the user (35 kg/m²)."),
    ("ზაფხულის ფასი / Summer price — 3.00 GEL/kg", "მომხმარებლის მონაცემი / Given by the user."),
    ("OPEX — 150,000 GEL/წელი", "მომხმარებლის მონაცემი. 8 კატეგორიად დაშლა და თვიური სეზონურობა მოდელის დაშვებაა — შეცვლადია OPEX ფურცელზე. / Total given by the user; the split into 8 categories and the monthly seasonality are the model's own assumptions and are editable on the OPEX sheet."),
    ("კრედიტი / Credit — 625,000 ₾, სს „ბანკი ქართუ\"",
     "ხელშეკრულება GA/1-876787–001, 17/06/2026, მსესხებელი შპს მუხრანი 2026 (ს/ნ 404801602); ვადა 17/06/2036, "
     "120 თვე; შეღავათიანი აგრო კრედიტი, მიზნობრიობა — ძირითადი საშუალებების ფინანსირება (პუნქტები 3.6, 3.8, 3.11). / "
     "Contract GA/1-876787–001 of 17/06/2026 with LLC Mukhrani 2026; matures 17/06/2036 over 120 months; preferential "
     "agro credit for financing fixed assets (clauses 3.6, 3.8, 3.11)."),
    ("განაკვეთი / Rate — 12.64%, შემდეგ 13.40%",
     "12.64% 17/06/2028-მდე; შემდეგ ინდექსირებული = რეფინანსირება + 5.14%, არანაკლებ 10% და არაუმეტეს 18%. ეფექტური "
     "13.77% / 13.78%. მე-2 განაკვეთი 13.40% ბანკის დანართ #1-იდანაა ნაგულისხმევი (რეფინანსირება 8.26% + 5.14%). / "
     "12.64% to 17/06/2028, then indexed at refinancing + 5.14%, floor 10%, cap 18%. Effective APR 13.77% / 13.78%. "
     "The 13.40% second rate is what the bank's own Annex 1 implies (refinancing 8.26% + 5.14%)."),
    ("თანადაფინანსება / Co-financing — 11% p.a., 48 თვე",
     "სოფლის განვითარების სააგენტო აფინანსებს ძირითადი თანხის წლიურ 11%-ს, არაუმეტეს 48 თვისა (პუნქტი 3.5). მოდელში "
     "ეს ამცირებს პროცენტის ტვირთს დაახლოებით 256,000 ₾-ით. / The Rural Development Agency co-finances 11% p.a. of "
     "the principal for up to 48 months (clause 3.5) — worth about 256,000 GEL of the interest bill."),
    ("გრაფიკი / Schedule — 12 თვე შეღავათი",
     "დანართი #1: თვე 1–12 გადახდის გარეშე, მე-13 თვეს იფარება დაგროვილი პროცენტი, შემდეგ ანუიტეტი 107 თვის "
     "განმავლობაში. / Annex 1: months 1–12 pay nothing, month 13 clears the accrued interest, then a 107-month annuity."),
    ("კურსი / FX — 2.6384 ₾/$",
     "ფაქტი: ბანკის ამონაწერი 09/07/2026 — 22,000 USD = 58,044.80 GEL, დანიშნულებაში მითითებული კურსი 2.6384. "
     "(04/08/2026: 5,000 USD = 13,100 GEL → 2.62.) / Actual: bank statement 09/07/2026 — USD 22,000 = GEL 58,044.80, "
     "rate 2.6384 stated in the payment description. (04/08/2026: USD 5,000 = GEL 13,100 → 2.62.)"),
    ("ფაქტობრივი ხარჯი / Actual spend — 90,541.21 GEL",
     "წყარო: transaction_history_all_accounts_20260401_20260909.csv, ანგარიში GE66CR0000009572073602, შპს მუხრანი 2026. "
     "15 გადარიცხვა 01/07–08/09/2026, შემოსავალი ამონაწერში არ ფიქსირდება. / Source: the Drive file "
     "transaction_history_all_accounts_20260401_20260909.csv, account GE66CR0000009572073602, LLC Mukhrani 2026. "
     "15 payments 1 Jul – 8 Sep 2026; the statement shows no inflows."),
    ("ხელშეკრულება N1 / Contract N1 — 7/6/2026, შპს ჯიესენ გრუპ",
     "ავანსები 22,000 + 5,000 USD გადახდილია (Actuals ფურცელი). ხელშეკრულების PDF სკანირებულია და ტექსტურად არ "
     "იკითხება, ამიტომ ჯამური ღირებულება ხელით შესავსებია — Project!B31. / Advances of USD 22,000 + 5,000 are paid "
     "(see the Actuals sheet). The contract PDF is a scan with no text layer, so its total value has to be typed in "
     "by hand — Project!B31."),
    ("გაყიდვების სეზონურობა / Sales seasonality", "მოდელის დაშვება: ზამთრის მოსავალი იყიდება დეკ–აპრ, ზაფხულის — ივნ–სექ. / Model assumption: winter crop sold Dec–Apr, summer crop Jun–Sep. Editable on CF_Monthly rows 7–8."),
    ("გადასახადი / Profit tax — 0%",
     "საქართველოში მოგების გადასახადი მხოლოდ განაწილებისას იბეგრება, ხოლო პირველადი სასოფლო წარმოება 200,000 GEL ბრუნვამდე გათავისუფლებულია. მოდელში ნაგულისხმევია 0% — შეიყვანეთ თქვენი განაკვეთი Assumptions!B42. / Georgia taxes distributed profit only, and primary agricultural production is exempt below 200,000 GEL turnover. Default is 0% — set your own rate in Assumptions!B42."),
    ("კაპიტალური ხარჯი / CAPEX", "მოდელი ასახავს ოპერირების ფაზას: სესხი უკვე ათვისებულია, სათბური აშენებულია. თუ 1-ელ წელს გსურთ ჩარიცხვა+CAPEX — Assumptions!B44 = 1. / The model runs the operating phase (loan already drawn, greenhouse built). Set Assumptions!B44 = 1 to show the drawdown and matching CAPEX in Year 1."),
]
for a, b in src:
    put(ws, f"B{r}", a, BOLD)
    c = put(ws, f"C{r}", b, TXT)
    c.alignment = Alignment(vertical="top", wrap_text=True)
    ws.row_dimensions[r].height = 30
    r += 1

r += 1
put(ws, f"B{r}", "შენიშვნა / NOTE", SEC)
put(ws, f"C{r}", "ეს არის ფინანსური მოდელი დაშვებებზე დაყრდნობით და არა საინვესტიციო რჩევა. / This is an assumption-driven model, not investment advice.", NOTE)


# =====================================================================
# 2. ASSUMPTIONS
# =====================================================================
a = wb.create_sheet("Assumptions")
a.sheet_view.showGridLines = False
a.column_dimensions["A"].width = 58
a.column_dimensions["B"].width = 16
a.column_dimensions["C"].width = 12
a.column_dimensions["D"].width = 60

put(a, "A1", "დაშვებები / ASSUMPTIONS", TITLE)
put(a, "A2", "შეცვალეთ მხოლოდ ლურჯი/ყვითელი უჯრები / Edit blue & yellow cells only", NOTE)

for col, head in zip("ABCD", ["მაჩვენებელი / Item", "მნიშვნელობა / Value", "ერთეული / Unit", "კომენტარი / Comment"]):
    put(a, f"{col}4", head, H1, fill=FILL_H, align="center")


def arow(row, label, value, unit, comment, font=INP, fmt=GEL2, key=False):
    put(a, f"A{row}", label, TXT, border=BOX)
    c = put(a, f"B{row}", value, font, fmt=fmt, border=BOX, align="right")
    if key:
        c.fill = FILL_KEY
    put(a, f"C{row}", unit, TXT, border=BOX, align="center")
    put(a, f"D{row}", comment, NOTE, border=BOX)


section(a, 5, "1. ობიექტი / FACILITY", "D")
arow(6, "სათბურის ფართობი / Greenhouse area", 2000, "m²", "მომხმარებლის მონაცემი / Given", fmt='#,##0')
arow(7, "მოსავლის ციკლები წელიწადში / Harvest cycles per year", 2, "cycles", "ზამთარი + ზაფხული / Winter + summer", fmt='0')

section(a, 9, "2. მოსავალი და ფასი / YIELD & PRICE", "D")
arow(10, "ზამთრის მოსავალი / Winter harvest", 85, "tons", "მითითებული დიაპაზონი 80–90 / Stated range 80–90; midpoint used", fmt='#,##0.0', key=True)
put(a, "A11", "  ზამთრის მოსავალი / Winter harvest (kg)", TXT, border=BOX)
put(a, "B11", "=B10*1000", TXT, fmt=KG, border=BOX, align="right")
put(a, "C11", "kg", TXT, border=BOX, align="center")
put(a, "D11", "ავტომატური / Calculated", NOTE, border=BOX)
put(a, "A12", "  ზამთრის მოსავლიანობა / Winter yield per m²", TXT, border=BOX)
put(a, "B12", "=B11/B6", TXT, fmt='#,##0.0', border=BOX, align="right")
put(a, "C12", "kg/m²", TXT, border=BOX, align="center")
put(a, "D12", "ავტომატური / Calculated", NOTE, border=BOX)
arow(13, "ზამთრის ფასი / Winter selling price", 4.5, "GEL/kg", "მომხმარებლის მონაცემი / Given", fmt=GEL2, key=True)
arow(14, "ზაფხულის მოსავალი / Summer harvest", 70, "tons", "მომხმარებლის მონაცემი / Given", fmt='#,##0.0', key=True)
put(a, "A15", "  ზაფხულის მოსავალი / Summer harvest (kg)", TXT, border=BOX)
put(a, "B15", "=B14*1000", TXT, fmt=KG, border=BOX, align="right")
put(a, "C15", "kg", TXT, border=BOX, align="center")
put(a, "D15", "ავტომატური / Calculated", NOTE, border=BOX)
put(a, "A16", "  ზაფხულის მოსავლიანობა / Summer yield per m²", TXT, border=BOX)
put(a, "B16", "=B15/B6", TXT, fmt='#,##0.0', border=BOX, align="right")
put(a, "C16", "kg/m²", TXT, border=BOX, align="center")
put(a, "D16", "ავტომატური / Calculated", NOTE, border=BOX)
arow(17, "ზაფხულის ფასი / Summer selling price", 3.0, "GEL/kg", "მომხმარებლის მონაცემი / Given", fmt=GEL2, key=True)
put(a, "A18", "სულ მოსავალი / Total annual harvest", BOLD, border=BOX)
put(a, "B18", "=B10+B14", BOLD, fmt='#,##0.0', border=BOX, align="right")
put(a, "C18", "tons", TXT, border=BOX, align="center")
put(a, "D18", "ავტომატური / Calculated", NOTE, border=BOX)
put(a, "A19", "საშუალო შეწონილი ფასი / Blended average price", BOLD, border=BOX)
put(a, "B19", "=(B11*B13+B15*B17)/(B11+B15)", BOLD, fmt=GEL2, border=BOX, align="right")
put(a, "C19", "GEL/kg", TXT, border=BOX, align="center")
put(a, "D19", "ავტომატური / Calculated", NOTE, border=BOX)

section(a, 21, "3. საოპერაციო ხარჯი / OPERATING EXPENSES", "D")
arow(22, "წლიური OPEX (მითითებული) / Annual OPEX as stated", 150000, "GEL", "მომხმარებლის მონაცემი / Given", fmt=GEL, key=True)
put(a, "A23", "OPEX ფურცლის ჯამი / Total from OPEX sheet", TXT, border=BOX)
put(a, "B23", "=OPEX!B14", LNK, fmt=GEL, border=BOX, align="right")
put(a, "C23", "GEL", TXT, border=BOX, align="center")
put(a, "D23", "8 კატეგორიის ჯამი / Sum of the 8 categories", NOTE, border=BOX)
put(a, "A24", "შედარება / Check (must be 0)", TXT, border=BOX)
put(a, "B24", "=B23-B22", BOLD, fmt=GEL, border=BOX, align="right")
put(a, "C24", "GEL", TXT, border=BOX, align="center")
put(a, "D24", "თუ ≠ 0, გაასწორეთ OPEX კატეგორიები / If ≠ 0, adjust the OPEX categories", NOTE, border=BOX)

section(a, 26, "4. საბანკო სესხი — სს „ბანკი ქართუ\" / BANK LOAN — CARTU BANK", "D")
arow(27, "კრედიტის თანხა / Credit amount", 625000, "GEL",
     "ხელშეკრულება GA/1-876787–001, პუნქტი 3.11 / contract clause 3.11", fmt='#,##0', key=True)
arow(28, "გაცვლითი კურსი / FX rate", 2.6384, "GEL/USD",
     "ფაქტი 09/07/2026 გადარიცხვიდან, USD ხელშეკრულებებისთვის / actual, used for the USD contracts", fmt='0.0000', key=True)
a["B28"].comment = Comment(
    "წყარო: ბანკის ამონაწერი, 09/07/2026 — 22,000 USD = 58,044.80 GEL, დანიშნულებაში კურსი 2.6384. იხ. Actuals.\n"
    "Source: bank statement, 09/07/2026 — USD 22,000 = GEL 58,044.80, rate 2.6384 stated in the description. See Actuals.",
    "Model")
put(a, "A29", "მოდელში გამოყენებული ძირი / Principal used in the model (GEL)", BOLD, border=BOX)
put(a, "B29", "=B27", BOLD, fmt=GEL, border=BOX, align="right")
put(a, "C29", "GEL", TXT, border=BOX, align="center")
put(a, "D29", "სრულად ათვისებულად ითვლება / assumed fully drawn", NOTE, border=BOX)
arow(30, "წლიური საპროცენტო განაკვეთი / Annual interest rate", 0.1264, "%",
     "12.64% 17/06/2028-მდე; შემდეგ რეფინანსირება + 5.14%, min 10%, max 18% / 12.64% to 17/06/2028, indexed after",
     fmt=PCT2, key=True)
arow(31, "ვადა / Term", 120, "months", "17/06/2026 – 17/06/2036 (პუნქტი 3.9) / clause 3.9", fmt='0')
arow(32, "საშეღავათო პერიოდი / Grace period, no payments", 12, "months",
     "დანართი #1: თვე 1–12 გადახდის გარეშე / Annex 1: months 1–12 pay nothing", fmt='0')
put(a, "A33", "ყოველთვიური ანუიტეტი / Monthly annuity", BOLD, border=BOX)
put(a, "B33", "=PMT(B30/12,B31-B32-1,-B29)", BOLD, fmt=GEL, border=BOX, align="right")
put(a, "C33", "GEL", TXT, border=BOX, align="center")
put(a, "D33", "107 შენატანი მე-14 თვიდან / 107 instalments from month 14", NOTE, border=BOX)
arow(34, "სააგენტოს თანადაფინანსება / Agency co-financing rate", 0.11, "%",
     "სოფლის განვითარების სააგენტო — ძირის 11% წლიურად (პუნქტი 3.5) / Rural Development Agency, clause 3.5",
     fmt=PCT2, key=True)
arow(35, "თანადაფინანსების ვადა / Co-financing period", 48, "months",
     "არაუმეტეს 48 თვისა (პუნქტი 3.5) / up to 48 months, clause 3.5", fmt='0')
arow(36, "განაკვეთი 17/06/2028-ის შემდეგ / Rate after 17/06/2028", 0.134, "%",
     "რეფინანსირება 8.26% + მარჟა 5.14%; ბანკის დანართ #1-იდან ნაგულისხმევი / implied by the bank's Annex 1: "
     "refinancing 8.26% + 5.14% margin", fmt=PCT2, key=True)
arow(37, "თვე, საიდანაც მოქმედებს მე-2 განაკვეთი / Month the second rate starts", 24, "month",
     "19/06/2028, გრაფიკის 24-ე შენატანი / instalment 24, 19/06/2028", fmt='0')

section(a, 38, "5. ზრდა და ინფლაცია (წლები 2–5) / GROWTH & INFLATION (YEARS 2–5)", "D")
arow(39, "მოსავლის ზრდა / Yield growth p.a.", 0.02, "%", "მოდელის დაშვება / Model assumption", fmt=PCT2)
arow(40, "ფასის ზრდა / Price growth p.a.", 0.03, "%", "მოდელის დაშვება / Model assumption", fmt=PCT2)
arow(41, "OPEX ინფლაცია / OPEX inflation p.a.", 0.04, "%", "მოდელის დაშვება / Model assumption", fmt=PCT2)

section(a, 43, "6. სხვა / OTHER", "D")
arow(44, "მოგების გადასახადი / Profit tax rate applied", 0.0, "%", "0% ნაგულისხმევად — იხ. Instructions / 0% by default", fmt=PCT2, key=True)
arow(45, "საწყისი ფულადი ნაშთი / Opening cash balance", 0, "GEL", "საოპერაციო წელი 1-ის დასაწყისი / start of operating Year 1", fmt=GEL)
arow(46, "კრედიტის ათვისება წელი 1-ში? / Credit drawn in Year 1? (1=yes, 0=no)", 0, "1/0",
     "0 = უკვე ათვისებული / 0 = already drawn", fmt='0')
put(a, "A47", "კაპიტალური ხარჯი წელი 1 / CAPEX in Year 1", TXT, border=BOX)
put(a, "B47", "=B46*B29", TXT, fmt=GEL, border=BOX, align="right")
put(a, "C47", "GEL", TXT, border=BOX, align="center")
put(a, "D47", "ტოლი ათვისებული კრედიტისა / equals the drawdown, net zero", NOTE, border=BOX)
arow(48, "სესხის წელი = საოპერაციო წელი 1 / Loan year mapped to operating Year 1", 2, "yr",
     "სესხის მე-2 წელი = 07/2027–06/2028, ამორტიზაციის პირველი წელი / loan year 2 = Jul 2027 – Jun 2028",
     fmt='0', key=True)

put(a, "A50", "შედეგები / KEY OUTPUTS (operating Year 1)", SEC, fill=FILL_SEC)
for col in "BCD":
    a[f"{col}50"].fill = FILL_SEC
outs = [
    (51, "წლიური შემოსავალი / Annual revenue", "=CF_Monthly!N19", GEL),
    (52, "წლიური OPEX / Annual OPEX", "=CF_Monthly!N30", GEL),
    (53, "EBITDA", "=CF_Monthly!N32", GEL),
    (54, "EBITDA მარჟა / margin", "=IFERROR(B53/B51,0)", PCT),
    (55, "ვალის მომსახურება / Debt service", "=CF_Monthly!N36", GEL),
    (56, "წმინდა ფულადი ნაკადი / Net cash flow", "=CF_Monthly!N43", GEL),
    (57, "DSCR (EBITDA / ვალის მომსახურება)", "=IFERROR(B53/B55,0)", MULT),
    (58, "პროექტში ჩადებული დღემდე / Project spend to date", "=Budget!B21", GEL),
    (59, "აქედან კაპიტალური / of which capitalised", "=Budget!B38", GEL),
]
for row, label, formula, fmt in outs:
    put(a, f"A{row}", label, BOLD, border=BOX)
    put(a, f"B{row}", formula, LNKB, fmt=fmt, border=BOX, align="right")
    put(a, f"C{row}", "GEL" if fmt == GEL else "", TXT, border=BOX, align="center")
    put(a, f"D{row}", "სხვა ფურცლიდან / from another sheet", NOTE, border=BOX)


# =====================================================================
# 3. OPEX
# =====================================================================
o = wb.create_sheet("OPEX")
o.sheet_view.showGridLines = False
o.column_dimensions["A"].width = 46
o.column_dimensions["B"].width = 14
for i in range(3, 16):
    o.column_dimensions[get_column_letter(i)].width = 9.5
o.column_dimensions["O"].width = 11

put(o, "A1", "საოპერაციო ხარჯები / OPERATING EXPENSES", TITLE)
put(o, "A2", "სულ 150,000 GEL/წელი. კატეგორიების დაშლა და თვიური წილები მოდელის დაშვებაა — შეცვლადია. / "
             "150,000 GEL total per year. The category split and monthly weights are model assumptions — editable.", NOTE)

# annual, then 12 monthly weights (fractions summing to 1.00)
cats = [
    ("ხელფასები / Labour & wages", 48000,
     [.09, .09, .09, .08, .07, .09, .09, .09, .08, .07, .07, .09]),
    ("გათბობა (გაზი/საწვავი) / Heating (gas & fuel)", 36000,
     [.25, .22, .13, .03, .00, .00, .00, .00, .00, .04, .13, .20]),
    ("ელექტროენერგია და წყალი / Electricity & water", 12000,
     [.08, .08, .08, .08, .09, .10, .11, .11, .09, .06, .06, .06]),
    ("ნერგები და თესლი / Seedlings & seeds", 14000,
     [.00, .00, .20, .25, .00, .00, .00, .30, .25, .00, .00, .00]),
    ("სასუქი და მცენარეთა დაცვა / Fertiliser & crop protection", 18000,
     [.08, .10, .12, .10, .08, .08, .08, .08, .10, .10, .04, .04]),
    ("შეფუთვა და ლოგისტიკა / Packaging & logistics", 10000,
     [.12, .14, .14, .08, .00, .07, .11, .11, .07, .00, .00, .16]),
    ("რემონტი და მოვლა / Maintenance & repairs", 6000,
     [.02, .02, .02, .04, .20, .10, .02, .02, .03, .25, .25, .03]),
    ("ადმინისტრაცია, დაზღვევა, ბუღალტერია / Admin, insurance, accounting", 6000,
     [.08, .08, .09, .08, .08, .09, .08, .08, .09, .08, .08, .09]),
]

put(o, "A4", "ბლოკი 1 — წლიური თანხა და თვიური წილი (%) / BLOCK 1 — annual amount and monthly weight (%)", SEC, fill=FILL_SEC)
for i in range(1, 16):
    o.cell(row=4, column=i).fill = FILL_SEC

put(o, "A5", "კატეგორია / Category", H1, fill=FILL_H)
put(o, "B5", "წლიური GEL / Annual", H1, fill=FILL_H, align="center")
for i, m in enumerate(MONTHS):
    put(o, f"{get_column_letter(3+i)}5", f"{m} / {MONTHS_KA[i]}", H1, fill=FILL_H, align="center")
put(o, "O5", "ჯამი % / Check", H1, fill=FILL_H, align="center")

r0 = 6
for i, (name, annual, weights) in enumerate(cats):
    r = r0 + i
    put(o, f"A{r}", name, TXT, border=BOX)
    put(o, f"B{r}", annual, INP, fmt=GEL, border=BOX, align="right")
    for j, w in enumerate(weights):
        put(o, f"{get_column_letter(3+j)}{r}", w, INP, fmt=PCT, border=BOX, align="right")
    put(o, f"O{r}", f"=SUM(C{r}:N{r})", BOLD, fmt=PCT, border=BOX, align="right")

rtot = r0 + len(cats)
put(o, f"A{rtot}", "სულ / TOTAL", BOLD, fill=FILL_TOT, border=BOX)
put(o, f"B{rtot}", f"=SUM(B{r0}:B{rtot-1})", BOLD, fmt=GEL, fill=FILL_TOT, border=BOX, align="right")
for j in range(12):
    cl = get_column_letter(3 + j)
    put(o, f"{cl}{rtot}", f"=IFERROR(SUMPRODUCT($B${r0}:$B${rtot-1},{cl}{r0}:{cl}{rtot-1})/$B${rtot},0)",
        BOLD, fmt=PCT, fill=FILL_TOT, border=BOX, align="right")
put(o, f"O{rtot}", f"=SUM(C{rtot}:N{rtot})", BOLD, fmt=PCT, fill=FILL_TOT, border=BOX, align="right")
put(o, f"A{rtot+1}", "თითოეული სტრიქონის „ჯამი %\" უნდა იყოს 100.0%. / Every row's check must read 100.0%.", NOTE)

# Block 2 — monthly GEL
b2h = rtot + 3          # section row
b2hdr = b2h + 1         # header row
b2r0 = b2hdr + 1        # first data row
put(o, f"A{b2h}", "ბლოკი 2 — თვიური ხარჯი (GEL) / BLOCK 2 — monthly cost (GEL)", SEC, fill=FILL_SEC)
for i in range(1, 16):
    o.cell(row=b2h, column=i).fill = FILL_SEC
put(o, f"A{b2hdr}", "კატეგორია / Category", H1, fill=FILL_H)
for i, m in enumerate(MONTHS):
    put(o, f"{get_column_letter(2+i)}{b2hdr}", f"{m} / {MONTHS_KA[i]}", H1, fill=FILL_H, align="center")
put(o, f"N{b2hdr}", "სულ / Total", H1, fill=FILL_H, align="center")

for i, (name, _, _) in enumerate(cats):
    r = b2r0 + i
    src_r = r0 + i
    put(o, f"A{r}", name, TXT, border=BOX)
    for j in range(12):
        col_out = get_column_letter(2 + j)
        col_src = get_column_letter(3 + j)
        put(o, f"{col_out}{r}", f"=$B${src_r}*{col_src}{src_r}", TXT, fmt=GEL, border=BOX, align="right")
    put(o, f"N{r}", f"=SUM(B{r}:M{r})", BOLD, fmt=GEL, border=BOX, align="right")

b2tot = b2r0 + len(cats)
put(o, f"A{b2tot}", "სულ OPEX / TOTAL OPEX", BOLD, fill=FILL_TOT, border=BOX)
for j in range(12):
    cl = get_column_letter(2 + j)
    put(o, f"{cl}{b2tot}", f"=SUM({cl}{b2r0}:{cl}{b2tot-1})", BOLD, fmt=GEL, fill=FILL_TOT, border=BOX, align="right")
put(o, f"N{b2tot}", f"=SUM(B{b2tot}:M{b2tot})", BOLD, fmt=GEL, fill=FILL_TOT, border=BOX, align="right")

OPEX_M_R0 = b2r0        # first monthly category row (col B = Jan)
OPEX_M_TOT = b2tot


# =====================================================================
# 4. LOAN — Cartu Bank agro credit GA/1-876787-001, per the signed contract
# =====================================================================
ln = wb.create_sheet("Loan")
ln.sheet_view.showGridLines = False
widths = {"A": 8, "B": 12, "C": 7, "D": 15, "E": 13, "F": 15, "G": 14, "H": 13,
          "I": 15, "J": 15, "K": 15, "L": 3, "M": 8, "N": 14, "O": 15, "P": 14,
          "Q": 13, "R": 15, "S": 15}
for k, v in widths.items():
    ln.column_dimensions[k].width = v

put(ln, "A1", "სესხის გრაფიკი / LOAN SCHEDULE — სს „ბანკი ქართუ\" / CARTU BANK", TITLE)
put(ln, "A2", "ხელშეკრულება GA/1-876787–001, 17/06/2026 · შეღავათიანი აგრო კრედიტი · ყველა პირობა ხელშეკრულებიდან / "
              "Contract GA/1-876787–001 of 17/06/2026 · preferential agro credit · every term is taken from the contract", NOTE)

hdr = ["თვე / M", "თარიღი / Date", "წელი / Yr", "საწყისი ძირი / Opening",
       "დარიცხული % / Interest", "სააგენტო / Agency", "წმინდა % / Net interest",
       "ძირი / Principal", "გადახდა / Payment", "დარჩენილი ძირი / Closing",
       "დაგროვილი % / Accrued"]
for i, h in enumerate(hdr):
    put(ln, f"{get_column_letter(1+i)}4", h, H1, fill=FILL_H, align="center")

TERM = 120
LR0 = 5
LREND = LR0 + TERM - 1
for m in range(1, TERM + 1):
    r = LR0 + m - 1
    put(ln, f"A{r}", m, TXT, fmt='0', border=BOX, align="center")
    put(ln, f"B{r}", f"=EDATE(DATE(2026,6,17),A{r})", TXT, fmt='DD/MM/YYYY', border=BOX, align="center")
    put(ln, f"C{r}", f"=INT((A{r}-1)/12)+1", TXT, fmt='0', border=BOX, align="center")
    put(ln, f"D{r}", "=Assumptions!$B$29" if m == 1 else f"=J{r-1}", LNK if m == 1 else TXT,
        fmt=GEL, border=BOX, align="right")
    # interest accrued on the outstanding balance
    put(ln, f"E{r}", f"=IF(A{r}>Assumptions!$B$31,0,D{r}*IF(A{r}<Assumptions!$B$37,Assumptions!$B$30,"
                     f"Assumptions!$B$36)/12)", TXT, fmt=GEL, border=BOX, align="right")
    # Rural Development Agency co-financing, capped at its own rate and its own window
    put(ln, f"F{r}", f"=IF(A{r}>Assumptions!$B$35,0,MIN(E{r},D{r}*Assumptions!$B$34/12))", TXT, fmt=GEL, border=BOX, align="right")
    put(ln, f"G{r}", f"=E{r}-F{r}", TXT, fmt=GEL, border=BOX, align="right")
    # principal: nothing during the grace year, nothing in the catch-up month, then the annuity
    put(ln, f"H{r}", f"=IF(A{r}>Assumptions!$B$31,0,IF(A{r}<=Assumptions!$B$32+1,0,MIN(D{r},"
                     f"PMT(IF(A{r}<Assumptions!$B$37,Assumptions!$B$30,Assumptions!$B$36)/12,"
                     f"Assumptions!$B$31-A{r}+1,-D{r})-E{r})))",
        TXT, fmt=GEL, border=BOX, align="right")
    # borrower's cash: nothing in the grace year, the accrued lump in the catch-up month, then annuity less agency
    prevK = f"K{r-1}" if m > 1 else "0"
    put(ln, f"I{r}", f"=IF(A{r}>Assumptions!$B$31,0,IF(A{r}<=Assumptions!$B$32,0,"
                     f"IF(A{r}=Assumptions!$B$32+1,{prevK}+G{r},H{r}+G{r})))",
        TXT, fmt=GEL, border=BOX, align="right")
    put(ln, f"J{r}", f"=D{r}-H{r}", TXT, fmt=GEL, border=BOX, align="right")
    put(ln, f"K{r}", f"=IF(A{r}<=Assumptions!$B$32,{prevK}+G{r},0)", TXT, fmt=GEL, border=BOX, align="right")

rtotl = LREND + 1
put(ln, f"A{rtotl}", "სულ / TOTAL", BOLD, fill=FILL_TOT, border=BOX)
for cl in "BCD":
    put(ln, f"{cl}{rtotl}", "", TXT, fill=FILL_TOT, border=BOX)
for cl in "EFGHI":
    put(ln, f"{cl}{rtotl}", f"=SUM({cl}{LR0}:{cl}{LREND})", BOLD, fmt=GEL, fill=FILL_TOT, border=BOX, align="right")
for cl in "JK":
    put(ln, f"{cl}{rtotl}", "", TXT, fill=FILL_TOT, border=BOX)

# ---- annual summary by loan year ----
put(ln, "M4", "წელი / Yr", H1, fill=FILL_H, align="center")
put(ln, "N4", "დარიცხული % / Interest", H1, fill=FILL_H, align="center")
put(ln, "O4", "სააგენტო / Agency", H1, fill=FILL_H, align="center")
put(ln, "P4", "წმინდა % / Net interest", H1, fill=FILL_H, align="center")
put(ln, "Q4", "ძირი / Principal", H1, fill=FILL_H, align="center")
put(ln, "R4", "გადახდა / Cash paid", H1, fill=FILL_H, align="center")
put(ln, "S4", "ნაშთი წლის ბოლოს / Closing", H1, fill=FILL_H, align="center")
LOAN_Y_R0 = 5
for y in range(1, 11):
    r = 4 + y
    put(ln, f"M{r}", y, TXT, fmt='0', border=BOX, align="center")
    for cl_out, cl_src in (("N", "E"), ("O", "F"), ("P", "G"), ("Q", "H"), ("R", "I")):
        put(ln, f"{cl_out}{r}", f"=SUMIF($C${LR0}:$C${LREND},$M{r},${cl_src}${LR0}:${cl_src}${LREND})",
            TXT, fmt=GEL, border=BOX, align="right")
    put(ln, f"S{r}", f"=INDEX($J${LR0}:$J${LREND},MATCH($M{r}*12,$A${LR0}:$A${LREND},0))",
        TXT, fmt=GEL, border=BOX, align="right")
put(ln, "M15", "სულ / TOTAL", BOLD, fill=FILL_TOT, border=BOX)
for cl in "NOPQR":
    put(ln, f"{cl}15", f"=SUM({cl}5:{cl}14)", BOLD, fmt=GEL, fill=FILL_TOT, border=BOX, align="right")
put(ln, "S15", "", TXT, fill=FILL_TOT, border=BOX)

# ---- cross-check against the bank's own Annex 1 ----
put(ln, "M17", "შედარება ბანკის გრაფიკთან (დანართი #1) / CROSS-CHECK vs THE BANK'S OWN SCHEDULE", SEC, fill=FILL_SEC)
for i in range(13, 20):
    ln.cell(row=17, column=i).fill = FILL_SEC
put(ln, "M18", "მაჩვენებელი / Item", H1, fill=FILL_H)
put(ln, "P18", "ბანკის გრაფიკი / Bank", H1, fill=FILL_H, align="center")
put(ln, "Q18", "მოდელი / Model", H1, fill=FILL_H, align="center")
put(ln, "R18", "სხვაობა / Diff", H1, fill=FILL_H, align="center")
checks = [
    ("სულ ძირი / Total principal", 625000.0, f"=H{rtotl}"),
    ("სულ პროცენტი / Total interest", 529681.25, f"=E{rtotl}"),
    ("სულ გადასახდელი / Total repayable", 1154681.25, "=Q19+Q20"),
]
for i, (lab, bank, model_f) in enumerate(checks):
    r = 19 + i
    put(ln, f"M{r}", lab, TXT, border=BOX)
    put(ln, f"P{r}", bank, INP, fmt=GEL, border=BOX, align="right")
    put(ln, f"Q{r}", model_f, TXT, fmt=GEL, border=BOX, align="right")
    put(ln, f"R{r}", f"=Q{r}-P{r}", BOLD, fmt=GEL, border=BOX, align="right")
put(ln, "M22",
    "ბანკის გრაფიკი დანართ #1-ში 1,000-ზეა დაყვანილი (სულ ძირი 1,000.00, პროცენტი 847.49, ჯამი 1,847.49); "
    "აქ გამრავლებულია 625-ზე, რადგან კრედიტი 625,000 ლარია. / The bank's Annex 1 is stated per 1,000 units "
    "(principal 1,000.00, interest 847.49, total 1,847.49); these are scaled by 625 for the 625,000 GEL credit.", NOTE)
put(ln, "M23",
    "სხვაობა მცირეა, რადგან ბანკი დღეების მიხედვით ითვლის, მოდელი კი თანაბარ თვეებზე. / A small difference is "
    "expected: the bank accrues on actual days, the model on equal months.", NOTE)

put(ln, "M25", "ანუიტეტი 1 (17/06/2028-მდე) / Annuity 1", BOLD, border=BOX)
put(ln, "N25", "=H18+E18", BOLD, fmt=GEL, border=BOX, align="right")
put(ln, "O25", "ბანკის გრაფიკი / bank: 9,768.75", NOTE, border=BOX)
put(ln, "M26", "ანუიტეტი 2 (17/06/2028-ის შემდეგ) / Annuity 2", BOLD, border=BOX)
put(ln, "N26", "=H28+E28", BOLD, fmt=GEL, border=BOX, align="right")
put(ln, "O26", "ბანკის გრაფიკი / bank: 10,012.50", NOTE, border=BOX)
put(ln, "M28", "წყარო: Mukrlhranis loan contract, GA/1-876787–001 (Google Drive) / "
               "Source: the signed contract on Drive", NOTE)

ln.freeze_panes = "A5"


# =====================================================================
# 5. CF_MONTHLY
# =====================================================================
c = wb.create_sheet("CF_Monthly")
c.sheet_view.showGridLines = False
c.column_dimensions["A"].width = 50
for i in range(2, 14):
    c.column_dimensions[get_column_letter(i)].width = 11.5
c.column_dimensions["N"].width = 14

put(c, "A1", "ფულადი ნაკადი — წელი 1 / CASH FLOW — YEAR 1", TITLE)
put(c, "A2", "ყველა თანხა GEL-ში / All amounts in GEL", NOTE)

put(c, "A4", "მაჩვენებელი / Item", H1, fill=FILL_H)
for i, m in enumerate(MONTHS):
    put(c, f"{get_column_letter(2+i)}4", f"{m} / {MONTHS_KA[i]}", H1, fill=FILL_H, align="center")
put(c, "N4", "სულ / TOTAL", H1, fill=FILL_H, align="center")

winter_dist = [.20, .25, .25, .15, .00, .00, .00, .00, .00, .00, .00, .15]
summer_dist = [.00, .00, .00, .00, .00, .20, .30, .30, .20, .00, .00, .00]


def cf_section(row, text):
    put(c, f"A{row}", text, SEC, fill=FILL_SEC)
    for i in range(1, 15):
        c.cell(row=row, column=i).fill = FILL_SEC


def cf_row(row, label, formulas, font=TXT, fmt=GEL, total="sum", fill=None, bold=False):
    f = BOLD if bold else font
    put(c, f"A{row}", label, f, border=BOX, fill=fill)
    for j in range(12):
        cl = get_column_letter(2 + j)
        put(c, f"{cl}{row}", formulas[j], f, fmt=fmt, border=BOX, align="right", fill=fill)
    if total == "sum":
        put(c, f"N{row}", f"=SUM(B{row}:M{row})", BOLD if not bold else BOLD, fmt=fmt, border=BOX, align="right", fill=fill)
    elif total == "first":
        put(c, f"N{row}", f"=B{row}", BOLD, fmt=fmt, border=BOX, align="right", fill=fill)
    elif total == "last":
        put(c, f"N{row}", f"=M{row}", BOLD, fmt=fmt, border=BOX, align="right", fill=fill)
    elif total == "avg":
        put(c, f"N{row}", f"=IFERROR(AVERAGE(B{row}:M{row}),0)", BOLD, fmt=fmt, border=BOX, align="right", fill=fill)
    else:
        put(c, f"N{row}", "", TXT, border=BOX, fill=fill)


cf_section(6, "გაყიდვების სეზონურობა / SALES SEASONALITY (edit the blue cells; each row must total 100%)")
cf_row(7, "ზამთრის მოსავლის რეალიზაცია / Winter crop sold (%)", winter_dist, font=INP, fmt=PCT)
cf_row(8, "ზაფხულის მოსავლის რეალიზაცია / Summer crop sold (%)", summer_dist, font=INP, fmt=PCT)

cf_section(10, "მოცულობა / VOLUME (kg)")
cf_row(11, "ზამთრის მოსავალი / Winter crop", [f"=Assumptions!$B$11*{get_column_letter(2+j)}7" for j in range(12)], fmt=KG)
cf_row(12, "ზაფხულის მოსავალი / Summer crop", [f"=Assumptions!$B$15*{get_column_letter(2+j)}8" for j in range(12)], fmt=KG)
cf_row(13, "სულ გაყიდული / Total sold", [f"=SUM({get_column_letter(2+j)}11:{get_column_letter(2+j)}12)" for j in range(12)], fmt=KG, bold=True, fill=FILL_TOT)

cf_section(15, "შემოსავალი / REVENUE (GEL)")
cf_row(16, "ზამთრის შემოსავალი / Winter revenue", [f"={get_column_letter(2+j)}11*Assumptions!$B$13" for j in range(12)])
cf_row(17, "ზაფხულის შემოსავალი / Summer revenue", [f"={get_column_letter(2+j)}12*Assumptions!$B$17" for j in range(12)])
cf_row(18, "საშუალო ფასი / Realised price", [f"=IFERROR({get_column_letter(2+j)}19/{get_column_letter(2+j)}13,0)" for j in range(12)], fmt=GEL2, total="avg")
cf_row(19, "სულ შემოსავალი / TOTAL REVENUE", [f"=SUM({get_column_letter(2+j)}16:{get_column_letter(2+j)}17)" for j in range(12)], bold=True, fill=FILL_TOT)

cf_section(21, "საოპერაციო ხარჯი / OPERATING EXPENSES (GEL)")
for i, (name, _, _) in enumerate(cats):
    row = 22 + i
    src = OPEX_M_R0 + i
    cf_row(row, name, [f"=OPEX!{get_column_letter(2+j)}{src}" for j in range(12)], font=LNK)
cf_row(30, "სულ OPEX / TOTAL OPEX", [f"=SUM({get_column_letter(2+j)}22:{get_column_letter(2+j)}29)" for j in range(12)], bold=True, fill=FILL_TOT)

cf_section(32 - 1, "მოგება და ვალის მომსახურება / EBITDA & DEBT SERVICE (GEL)")
cf_row(32, "EBITDA", [f"={get_column_letter(2+j)}19-{get_column_letter(2+j)}30" for j in range(12)], bold=True, fill=FILL_TOT)
cf_row(33, "EBITDA მარჟა / margin", [f"=IFERROR({get_column_letter(2+j)}32/{get_column_letter(2+j)}19,0)" for j in range(12)], fmt=PCT, total="none")
put(c, "N33", "=IFERROR(N32/N19,0)", BOLD, fmt=PCT, border=BOX, align="right")
cf_row(34, "სესხის პროცენტი, სააგენტოს გამოკლებით / Loan interest, net of agency",
       [f"=-INDEX(Loan!$G$5:$G$124,(Assumptions!$B$48-1)*12+{j+1})" for j in range(12)], font=LNK)
cf_row(35, "სესხის ძირი / Loan principal repayment",
       [f"=-INDEX(Loan!$H$5:$H$124,(Assumptions!$B$48-1)*12+{j+1})" for j in range(12)], font=LNK)
cf_row(36, "სულ ვალის მომსახურება / Total debt service", [f"=-({get_column_letter(2+j)}34+{get_column_letter(2+j)}35)" for j in range(12)], bold=True, fill=FILL_TOT)
cf_row(37, "მოგების გადასახადი / Profit tax", [f"=-MAX(0,{get_column_letter(2+j)}32+{get_column_letter(2+j)}34)*Assumptions!$B$44" for j in range(12)])

cf_section(39, "საინვესტიციო და საფინანსო ნაკადი / INVESTING & FINANCING (GEL)")
cf_row(40, "სესხის ათვისება / Loan drawdown",
       ["=Assumptions!$B$46*Assumptions!$B$29"] + ["=0"] * 11)
cf_row(41, "კაპიტალური ხარჯი / CAPEX", ["=-Assumptions!$B$47"] + ["=0"] * 11)

cf_section(42, "ფულადი ნაშთი / CASH POSITION (GEL)")
cf_row(43, "წმინდა ფულადი ნაკადი / NET CASH FLOW",
       [f"={get_column_letter(2+j)}32+{get_column_letter(2+j)}34+{get_column_letter(2+j)}35+"
        f"{get_column_letter(2+j)}37+{get_column_letter(2+j)}40+{get_column_letter(2+j)}41" for j in range(12)],
       bold=True, fill=FILL_TOT)
put(c, "A44", "საწყისი ნაშთი / Opening cash", TXT, border=BOX)
put(c, "B44", "=Assumptions!$B$45", LNK, fmt=GEL, border=BOX, align="right")
for j in range(1, 12):
    cl = get_column_letter(2 + j)
    prev = get_column_letter(1 + j)
    put(c, f"{cl}44", f"={prev}45", TXT, fmt=GEL, border=BOX, align="right")
put(c, "N44", "=B44", BOLD, fmt=GEL, border=BOX, align="right")
cf_row(45, "საბოლოო ნაშთი / CLOSING CASH", [f"={get_column_letter(2+j)}44+{get_column_letter(2+j)}43" for j in range(12)],
       total="last", bold=True, fill=FILL_TOT)
cf_row(46, "კუმულატიური ნაკადი / Cumulative net cash flow",
       [f"=SUM($B$43:{get_column_letter(2+j)}43)" for j in range(12)], total="last")

put(c, "A48", "საბრუნავი კაპიტალის საჭიროება / Working-capital requirement (largest cash shortfall)", BOLD)
put(c, "B48", "=MIN(0,MIN(B45:M45))", INPB, fmt=GEL, align="right")
put(c, "C48", "თუ უარყოფითია, ეს თანხა უნდა შეივსოს საბრუნავი კაპიტალით / If negative, this much extra working capital is needed", NOTE)
put(c, "A49", "DSCR (EBITDA / ვალის მომსახურება), წელი 1", BOLD)
put(c, "B49", "=IFERROR(N32/N36,0)", INPB, fmt=MULT, align="right")
put(c, "C49", "ბანკები ჩვეულებრივ ითხოვენ ≥ 1.20x / Banks typically require ≥ 1.20x", NOTE)
put(c, "A50", "შემოწმება — სეზონურობის ჯამი / Check — seasonality totals (both must be 100%)", BOLD)
put(c, "B50", "=SUM(B7:M7)", INPB, fmt=PCT, align="right")
put(c, "C50", "=SUM(B8:M8)", INPB, fmt=PCT, align="right")

c.freeze_panes = "B5"


# =====================================================================
# 6. ANNUAL
# =====================================================================
an = wb.create_sheet("Annual")
an.sheet_view.showGridLines = False
an.column_dimensions["A"].width = 50
for i in range(2, 7):
    an.column_dimensions[get_column_letter(i)].width = 15

put(an, "A1", "წლიური მიმოხილვა / ANNUAL SUMMARY — YEARS 1–5", TITLE)
put(an, "A2", "წლები 2–5 იზრდება Assumptions!B37:B39 პარამეტრებით / Years 2–5 are grown with the rates in Assumptions!B37:B39", NOTE)

put(an, "A4", "მაჩვენებელი / Item", H1, fill=FILL_H)
for y in range(5):
    put(an, f"{get_column_letter(2+y)}4", f"წელი {y+1} / Year {y+1}", H1, fill=FILL_H, align="center")


def an_row(row, label, y1, later, fmt=GEL, font=TXT, bold=False, fill=None):
    f = BOLD if bold else font
    put(an, f"A{row}", label, f, border=BOX, fill=fill)
    put(an, f"B{row}", y1, f, fmt=fmt, border=BOX, align="right", fill=fill)
    for y in range(1, 5):
        cl = get_column_letter(2 + y)
        prev = get_column_letter(1 + y)
        put(an, f"{cl}{row}", later.replace("{prev}", prev).replace("{col}", cl), f,
            fmt=fmt, border=BOX, align="right", fill=fill)


section(an, 5, "მოცულობა და ფასი / VOLUME & PRICE", "F")
an_row(6, "ზამთრის მოსავალი / Winter crop (kg)", "=Assumptions!$B$11", "={prev}6*(1+Assumptions!$B$39)", fmt=KG)
an_row(7, "ზაფხულის მოსავალი / Summer crop (kg)", "=Assumptions!$B$15", "={prev}7*(1+Assumptions!$B$39)", fmt=KG)
an_row(8, "სულ / Total (kg)", "=B6+B7", "={col}6+{col}7", fmt=KG, bold=True)
an_row(9, "ზამთრის ფასი / Winter price (GEL/kg)", "=Assumptions!$B$13", "={prev}9*(1+Assumptions!$B$40)", fmt=GEL2)
an_row(10, "ზაფხულის ფასი / Summer price (GEL/kg)", "=Assumptions!$B$17", "={prev}10*(1+Assumptions!$B$40)", fmt=GEL2)

section(an, 12, "მოგება-ზარალი / PROFIT & LOSS (GEL)", "F")
an_row(13, "ზამთრის შემოსავალი / Winter revenue", "=B6*B9", "={col}6*{col}9")
an_row(14, "ზაფხულის შემოსავალი / Summer revenue", "=B7*B10", "={col}7*{col}10")
an_row(15, "სულ შემოსავალი / TOTAL REVENUE", "=B13+B14", "={col}13+{col}14", bold=True, fill=FILL_TOT)
an_row(16, "საოპერაციო ხარჯი / Operating expenses", "=-CF_Monthly!$N$30", "={prev}16*(1+Assumptions!$B$41)", font=LNK)
an_row(17, "EBITDA", "=B15+B16", "={col}15+{col}16", bold=True, fill=FILL_TOT)
an_row(18, "EBITDA მარჟა / margin", "=IFERROR(B17/B15,0)", "=IFERROR({col}17/{col}15,0)", fmt=PCT)

section(an, 20, "ვალის მომსახურება / DEBT SERVICE (GEL)", "F")
for y in range(5):
    cl = get_column_letter(2 + y)
    put(an, "A21", "სესხის პროცენტი, სააგენტოს გამოკლებით / Loan interest, net of agency", LNK, border=BOX)
    put(an, f"{cl}21", f"=-SUMIF(Loan!$C$5:$C$124,Assumptions!$B$48+{y},Loan!$G$5:$G$124)",
        LNK, fmt=GEL, border=BOX, align="right")
    put(an, "A22", "სესხის ძირი / Loan principal", LNK, border=BOX)
    put(an, f"{cl}22", f"=-SUMIF(Loan!$C$5:$C$124,Assumptions!$B$48+{y},Loan!$H$5:$H$124)",
        LNK, fmt=GEL, border=BOX, align="right")
an_row(23, "სულ ვალის მომსახურება / Total debt service", "=-(B21+B22)", "=-({col}21+{col}22)", bold=True)
put(an, "A24", "ნაშთი წლის ბოლოს / Loan balance, year-end", LNK, border=BOX)
for y in range(5):
    cl = get_column_letter(2 + y)
    put(an, f"{cl}24",
        f"=INDEX(Loan!$J$5:$J$124,MATCH((Assumptions!$B$48+{y})*12,Loan!$A$5:$A$124,0))",
        LNK, fmt=GEL, border=BOX, align="right")

section(an, 26, "ფულადი ნაკადი / CASH FLOW (GEL)", "F")
an_row(27, "მოგების გადასახადი / Profit tax", "=-MAX(0,B17+B21)*Assumptions!$B$44", "=-MAX(0,{col}17+{col}21)*Assumptions!$B$44")
an_row(28, "საინვესტიციო/საფინანსო / Investing & financing",
       "=CF_Monthly!$N$40+CF_Monthly!$N$41", "=0", font=LNK)
an_row(29, "წმინდა ფულადი ნაკადი / NET CASH FLOW", "=B17+B21+B22+B27+B28",
       "={col}17+{col}21+{col}22+{col}27+{col}28", bold=True, fill=FILL_TOT)
an_row(30, "კუმულატიური / Cumulative", "=Assumptions!$B$45+B29", "={prev}30+{col}29", bold=True)

section(an, 32, "მაჩვენებლები / METRICS", "F")
an_row(33, "DSCR (EBITDA / ვალის მომსახურება)", "=IFERROR(B17/B23,0)", "=IFERROR({col}17/{col}23,0)", fmt=MULT, bold=True)
an_row(34, "OPEX / შემოსავალი", "=IFERROR(-B16/B15,0)", "=IFERROR(-{col}16/{col}15,0)", fmt=PCT)
an_row(35, "შემოსავალი 1 m²-ზე / Revenue per m²", "=B15/Assumptions!$B$6", "={col}15/Assumptions!$B$6", fmt=GEL2)
an_row(36, "თვითღირებულება 1 კგ-ზე / Cash cost per kg", "=IFERROR(-B16/B8,0)", "=IFERROR(-{col}16/{col}8,0)", fmt=GEL2)

put(an, "A38", "შემოწმება — წელი 1 ემთხვევა CF_Monthly-ს / Check — Year 1 ties to CF_Monthly (must be 0)", BOLD)
put(an, "B38", "=B29-CF_Monthly!$N$43", INPB, fmt=GEL, align="right")

an.freeze_panes = "B5"


# =====================================================================
# 7. SENSITIVITY
# =====================================================================
s = wb.create_sheet("Sensitivity")
s.sheet_view.showGridLines = False
s.column_dimensions["A"].width = 34
for i in range(2, 8):
    s.column_dimensions[get_column_letter(i)].width = 15

put(s, "A1", "მგრძნობელობა და წაგება-მოგების ზღვარი / SENSITIVITY & BREAK-EVEN", TITLE)
put(s, "A2", "წელი 1 / Year 1 · ყველა თანხა GEL-ში / all amounts in GEL", NOTE)

steps = [-0.20, -0.10, 0.0, 0.10, 0.20]

# Table 1 — net cash flow
put(s, "A4", "ცხრილი 1 — წმინდა ფულადი ნაკადი / TABLE 1 — Net cash flow after debt service", SEC, fill=FILL_SEC)
for i in range(1, 8):
    s.cell(row=4, column=i).fill = FILL_SEC
put(s, "A5", "მოსავალი ↓ / ფასი → | Yield ↓ / Price →", H1, fill=FILL_H, align="center")
for j, st in enumerate(steps):
    put(s, f"{get_column_letter(2+j)}5", st, H1, fmt=PCT, fill=FILL_H, align="center")
for i, st in enumerate(steps):
    r = 6 + i
    put(s, f"A{r}", st, H1, fmt=PCT, fill=FILL_H, align="center")
    for j in range(5):
        cl = get_column_letter(2 + j)
        f = (f"=(Assumptions!$B$11*(1+$A{r})*Assumptions!$B$13*(1+{cl}$5)"
             f"+Assumptions!$B$15*(1+$A{r})*Assumptions!$B$17*(1+{cl}$5))"
             f"-CF_Monthly!$N$30-CF_Monthly!$N$36")
        put(s, f"{cl}{r}", f, TXT, fmt=GEL, border=BOX, align="right")

# Table 2 — DSCR
put(s, "A12", "ცხრილი 2 — DSCR / TABLE 2 — Debt service coverage ratio", SEC, fill=FILL_SEC)
for i in range(1, 8):
    s.cell(row=12, column=i).fill = FILL_SEC
put(s, "A13", "მოსავალი ↓ / ფასი →", H1, fill=FILL_H, align="center")
for j, st in enumerate(steps):
    put(s, f"{get_column_letter(2+j)}13", st, H1, fmt=PCT, fill=FILL_H, align="center")
for i, st in enumerate(steps):
    r = 14 + i
    put(s, f"A{r}", st, H1, fmt=PCT, fill=FILL_H, align="center")
    for j in range(5):
        cl = get_column_letter(2 + j)
        f = (f"=IFERROR(((Assumptions!$B$11*(1+$A{r})*Assumptions!$B$13*(1+{cl}$13)"
             f"+Assumptions!$B$15*(1+$A{r})*Assumptions!$B$17*(1+{cl}$13))"
             f"-CF_Monthly!$N$30)/CF_Monthly!$N$36,0)")
        put(s, f"{cl}{r}", f, TXT, fmt=MULT, border=BOX, align="right")

# Break-even
put(s, "A20", "წაგება-მოგების ზღვარი / BREAK-EVEN (Year 1)", SEC, fill=FILL_SEC)
for i in range(1, 8):
    s.cell(row=20, column=i).fill = FILL_SEC
be = [
    ("საჭირო შემოსავალი (OPEX + ვალი) / Revenue needed to cover OPEX + debt service",
     "=CF_Monthly!$N$30+CF_Monthly!$N$36", GEL),
    ("ფაქტობრივი შემოსავალი / Actual revenue", "=CF_Monthly!$N$19", GEL),
    ("უსაფრთხოების ზღვარი / Margin of safety", "=IFERROR((B22-B21)/B22,0)", PCT),
    ("საჭირო საშუალო ფასი / Break-even blended price", "=IFERROR(B21/CF_Monthly!$N$13,0)", GEL2),
    ("ფაქტობრივი საშუალო ფასი / Actual blended price", "=Assumptions!$B$19", GEL2),
    ("საჭირო მოცულობა მოქმედ ფასებში / Break-even volume at current prices",
     "=IFERROR(B21/B25,0)", KG),
    ("ფაქტობრივი მოცულობა / Actual volume", "=CF_Monthly!$N$13", KG),
    ("დასაშვები მოსავლის კლება / Yield cushion", "=IFERROR(1-B26/B27,0)", PCT),
]
for i, (label, formula, fmt) in enumerate(be):
    r = 21 + i
    put(s, f"A{r}", label, TXT, border=BOX)
    put(s, f"B{r}", formula, BOLD, fmt=fmt, border=BOX, align="right")

put(s, "A31", "ცხრილები ითვლის: შემოსავალი (მოსავალი × ფასი) − OPEX − ვალის მომსახურება. ვალის მომსახურება და OPEX ფიქსირებულია. / "
             "The tables compute revenue (yield × price) − OPEX − debt service, holding OPEX and debt service fixed.", NOTE)

# =====================================================================
# 8. ACTUALS — the bank statement
# =====================================================================
from datetime import date

ac = wb.create_sheet("Actuals")
ac.sheet_view.showGridLines = False
for col, w in {"A": 13, "B": 54, "C": 34, "D": 36, "E": 15, "F": 12}.items():
    ac.column_dimensions[col].width = w

put(ac, "A1", "ფაქტობრივი გადარიცხვები / ACTUAL BANK TRANSACTIONS", TITLE)
put(ac, "A2", "ეს ფურცელი ამონაწერის ასლია — ნუ შეცვლით. მოდელი მას მხოლოდ კურსისთვის იყენებს. / "
              "A verbatim copy of the statement — do not edit. The model uses it only for the FX rate.", NOTE)

meta = [
    ("წყარო / Source files", "transaction_history_all_accounts_20260401_20260909.csv · "
                             "transaction_history_all_accounts_20260911_20260918.xlsx (Google Drive) · "
                             "19–21/09 მფლობელის მონაცემი, ამონაწერით დასადასტურებელი / reported by the owner, to be confirmed against the statement"),
    ("ანგარიში / Account", "GE66CR0000009572073602"),
    ("მფლობელი / Account name", "შპს მუხრანი 2026 / LLC Mukhrani 2026"),
    ("მოთხოვნილი პერიოდი / Period requested", "01/04/2026 – 21/09/2026"),
    ("ფაქტობრივი ჩანაწერები / Entries present", "01/07/2026 – 21/09/2026 · 30 გადარიცხვა / 30 payments"),
    ("ჩარიცხვა / Inflow", "14/09/2026 — 30,000 ₾, კრედიტის ტრანში GA/1-876787-001 — ხარჯი არ არის, ქვემოთ არ ითვლება / "
                          "a tranche of the credit, not an expense, excluded below"),
]
for i, (k, v) in enumerate(meta):
    put(ac, f"A{4+i}", k, BOLD, border=BOX)
    put(ac, f"B{4+i}", v, TXT, border=BOX)

section(ac, 11, "გადარიცხვები / PAYMENTS", "E")
for col, h in zip("ABCDE", ["თარიღი / Date", "დანიშნულება / Description", "მიმღები / Counterparty",
                            "კატეგორია / Category", "თანხა GEL / Amount"]):
    put(ac, f"{col}12", h, H1, fill=FILL_H, align="center")

CAT_BUILD = "მშენებლობის ავანსი / Construction advance"
CAT_PAY = "ხელფასი / Salaries"
CAT_TAX = "გადასახადები / Taxes & pension"
CAT_SVC = "მომსახურება / Services"
CAT_MAT = "მასალები / Materials"
CAT_INV = "მომწოდებლის ინვოისი / Supplier invoice"
CAT_FUEL = "საწვავი / Fuel"
CAT_FOOD = "მუშების კვება / Worker meals"
CAT_OTH = "სხვა / Other"

txns = [
    (date(2026, 7, 1), "ინვოისი", "შპს ტერმინალ ვესტ თრეიდინგ", CAT_INV, -1409.41),
    (date(2026, 7, 1), "მომსახურების ანაზღაურება", "ნუგზარი ბუნტური", CAT_SVC, -500.00),
    (date(2026, 7, 1), "ხელფასი", "ნატალია ქანანელი", CAT_PAY, -1000.00),
    (date(2026, 7, 1), "თანახმად ხელშეკრულებისა; მომსახურება", "გიორგი მღებრიშვილი", CAT_SVC, -1600.00),
    (date(2026, 7, 9), "ავანსი თანახმად ხელშეკრულება N1 7/6/2026 (22 000 აშშ დოლარი, ერ.კ. 2.6384)",
     "შპს ჯიესენ გრუპ", CAT_BUILD, -58044.80),
    (date(2026, 7, 13), "ელექტრო მასალების შეძენა; ლითონის სამონტაჟო მასალები", "ი.მ. შოთა კერესელიძე", CAT_MAT, -4660.00),
    (date(2026, 7, 16), "ინვოისი 154-729 27/06/2026", "შპს ენ ბი სი ჯგუფი", CAT_INV, -1450.00),
    (date(2026, 8, 4), "ავანსი თანახმად ხელშეკრულება N1 7/6/2026 (5 000 აშშ დოლარი)",
     "შპს ჯიესენ გრუპ", CAT_BUILD, -13100.00),
    (date(2026, 8, 4), "ხელფასი", "გოდერძი მეტრეველი", CAT_PAY, -2000.00),
    (date(2026, 8, 10), "საქვეანგარიშოდ საჯარო რეესტრში გაწეული ხარჯისათვის", "გოდერძი მეტრეველი", CAT_OTH, -307.00),
    (date(2026, 8, 10), "საპენსიო გადასახადი", "სსიპ საქართველოს საპენსიო ფონდი", CAT_TAX, -170.00),
    (date(2026, 8, 26), "გადასახადების ერთიანი კოდი", "ხაზინის ერთიანი ანგარიში (RS)", CAT_TAX, -900.00),
    (date(2026, 8, 26), "ხელფასი", "ნატალია ქანანელი", CAT_PAY, -2000.00),
    (date(2026, 8, 31), "ხელფასი", "გოდერძი მეტრეველი", CAT_PAY, -3000.00),
    (date(2026, 9, 8), "საპენსიო გადასახადი", "სსიპ საქართველოს საპენსიო ფონდი", CAT_TAX, -400.00),
    # --- ამონაწერი 11–18/09/2026 / statement of 11–18 September 2026 ---
    (date(2026, 9, 14), "ავანსი თანახმად ხელშეკრულება (ხელშ. N1)", "შპს ჯიესენ გრუპ", CAT_BUILD, -1500.00),
    (date(2026, 9, 14), "ავანსი თანახმად ხელშეკრულება (ხელშ. N1)", "შპს ჯიესენ გრუპ", CAT_BUILD, -1400.00),
    (date(2026, 9, 14), "ხელფასი", "გოდერძი მეტრეველი", CAT_PAY, -2000.00),
    (date(2026, 9, 14), "ინვოისი 12866 14/09/2026", "შპს კლუგერი 1", CAT_INV, -1616.00),
    (date(2026, 9, 14), "მომსახურება", "ვაჟა ბოდაველი", CAT_SVC, -150.00),
    (date(2026, 9, 14), "სესხის ერთჯერადი მომსახურების საკომისიო GA/1-876787-001", "სს ბანკი ქართუ", CAT_OTH, -60.00),
    (date(2026, 9, 16), "ინვოისი 20260916A 16/09/2026", "შპს იბოსთარ", CAT_INV, -3030.00),
    (date(2026, 9, 16), "სასაქონლო ზედნადებებით პროდუქციის საფასური", "ი.მ. ლალი ზეიკიძე", CAT_MAT, -467.70),
    (date(2026, 9, 16), "ცემენტის ღირებულება", "სოსო ხლუსიძე", CAT_MAT, -170.00),
    (date(2026, 9, 18), "ცემენტის ღირებულება, ზედნადები 1008422939 18/09/2026", "სოსო ხლუსიძე", CAT_MAT, -425.00),
    (date(2026, 9, 18), "მომსახურება", "რაუფ ბაირამოვი", CAT_SVC, -820.00),
    (date(2026, 9, 18), "ამწე მომსახურება — სამონტაჟო სამუშაო, კაპიტალიზებული", "აკაკი ბუჩაშვილი", CAT_OTH, -550.00),
    (date(2026, 9, 18), "საბანკო საკომისიოები — 11 გადარიცხვა, 11–18/09/2026", "სს ბანკი ქართუ", CAT_OTH, -12.08),
    # --- მფლობელის მონაცემი, 21/09/2026 / reported by the owner, 21 September ---
    (date(2026, 9, 19), "ავანსი ხელშეკრულება N1 (40 000 აშშ დოლარი, ერ.კ. 2.6125)",
     "შპს ჯიესენ გრუპ", CAT_BUILD, -104500.00),
    (date(2026, 9, 21), "მუშების კვება — საქვეანგარიშოდ დირექტორზე", "გოდერძი მეტრეველი", CAT_FOOD, -10000.00),
]
TR0 = 13
for i, (d, desc, cp, cat, amt) in enumerate(txns):
    r = TR0 + i
    put(ac, f"A{r}", d, INP, fmt='DD/MM/YYYY', border=BOX, align="center")
    put(ac, f"B{r}", desc, INP, border=BOX)
    put(ac, f"C{r}", cp, INP, border=BOX)
    put(ac, f"D{r}", cat, INP, border=BOX)
    put(ac, f"E{r}", amt, INP, fmt=GEL2, border=BOX, align="right")
TREND = TR0 + len(txns) - 1
RTOT = TREND + 1
put(ac, f"A{RTOT}", "სულ / TOTAL", BOLD, fill=FILL_TOT, border=BOX)
for col in "BCD":
    put(ac, f"{col}{RTOT}", "", TXT, fill=FILL_TOT, border=BOX)
put(ac, f"E{RTOT}", f"=SUM(E{TR0}:E{TREND})", BOLD, fmt=GEL2, fill=FILL_TOT, border=BOX, align="right")

CATS_A = [CAT_BUILD, CAT_PAY, CAT_TAX, CAT_SVC, CAT_FUEL, CAT_FOOD,
          CAT_MAT, CAT_INV, CAT_OTH]
CS = RTOT + 2
section(ac, CS, "კატეგორიების მიხედვით / BY CATEGORY", "E")
put(ac, f"A{CS+1}", "კატეგორია / Category", H1, fill=FILL_H)
put(ac, f"B{CS+1}", "თანხა GEL / Amount", H1, fill=FILL_H, align="center")
put(ac, f"C{CS+1}", "% ჯამიდან / of total", H1, fill=FILL_H, align="center")
for i, cat in enumerate(CATS_A):
    r = CS + 2 + i
    put(ac, f"A{r}", cat, TXT, border=BOX)
    put(ac, f"B{r}", f"=-SUMIF($D${TR0}:$D${TREND},$A{r},$E${TR0}:$E${TREND})", TXT, fmt=GEL2, border=BOX, align="right")
    put(ac, f"C{r}", f"=IFERROR($B{r}/$B${CS+2+len(CATS_A)},0)", TXT, fmt=PCT, border=BOX, align="right")
CATTOT = CS + 2 + len(CATS_A)
put(ac, f"A{CATTOT}", "სულ / TOTAL", BOLD, fill=FILL_TOT, border=BOX)
put(ac, f"B{CATTOT}", f"=SUM(B{CS+2}:B{CATTOT-1})", BOLD, fmt=GEL2, fill=FILL_TOT, border=BOX, align="right")
put(ac, f"C{CATTOT}", f"=IFERROR(B{CATTOT}/B{CATTOT},0)", BOLD, fmt=PCT, fill=FILL_TOT, border=BOX, align="right")
put(ac, f"A{CATTOT+1}", "შემოწმება / Check vs statement total (must be 0)", BOLD)
put(ac, f"B{CATTOT+1}", f"=B{CATTOT}+E{RTOT}", INPB, fmt=GEL2, align="right")

MS = CATTOT + 3
section(ac, MS, "თვეების მიხედვით / BY MONTH", "E")
put(ac, f"A{MS+1}", "თვე / Month", H1, fill=FILL_H)
put(ac, f"B{MS+1}", "თანხა GEL / Amount", H1, fill=FILL_H, align="center")
for i, (lab, y, m, last) in enumerate([("ივლისი 2026 / July", 2026, 7, 31),
                                       ("აგვისტო 2026 / August", 2026, 8, 31),
                                       ("სექტემბერი 2026 (21-მდე) / September (to the 21st)", 2026, 9, 30)]):
    r = MS + 2 + i
    put(ac, f"A{r}", lab, TXT, border=BOX)
    put(ac, f"B{r}",
        f"=-SUMPRODUCT(($A${TR0}:$A${TREND}>=DATE({y},{m},1))*($A${TR0}:$A${TREND}<=DATE({y},{m},{last}))*$E${TR0}:$E${TREND})",
        TXT, fmt=GEL2, border=BOX, align="right")
MTOT = MS + 5
put(ac, f"A{MTOT}", "სულ / TOTAL", BOLD, fill=FILL_TOT, border=BOX)
put(ac, f"B{MTOT}", f"=SUM(B{MS+2}:B{MTOT-1})", BOLD, fmt=GEL2, fill=FILL_TOT, border=BOX, align="right")

KF = MTOT + 2
section(ac, KF, "ძირითადი ფაქტები / KEY FACTS", "E")
facts = [
    ("გაცვლითი კურსი 09/07/2026 (22,000 USD) / FX rate on the 09/07/2026 transfer",
     f"=-E{TR0+4}/22000", '0.0000', "დანიშნულებაში მითითებული კურსი 2.6384 / the description states 2.6384"),
    ("გაცვლითი კურსი 04/08/2026 (5,000 USD) / FX rate on the 04/08/2026 transfer",
     f"=-E{TR0+7}/5000", '0.0000', "დანიშნულებაში კურსი არ არის მითითებული / no rate stated in the description"),
    ("მშენებლობის ავანსები / Construction advances paid (USD)", "=22000+5000", '#,##0',
     "ხელშეკრულება N1, 7/6/2026, შპს ჯიესენ გრუპ / contract N1 of 7/6/2026 with LLC GSN Group"),
    ("მშენებლობის ავანსები / Construction advances paid (GEL)", f"=B{CS+2}", GEL2,
     "ორივე გადარიცხვის ჯამი / the two transfers above"),
    ("სულ გადახდილი / Total paid out (GEL)", f"=-E{RTOT}", GEL2, "01/07–08/09/2026"),
    ("შემოსავალი ამონაწერში / Inflows in the statement (GEL)", "=0", GEL2,
     "ამონაწერში შემოსავალი არ ფიქსირდება — 140,000 USD სესხი ამ ანგარიშზე ამ პერიოდში არ ჩანს. / "
     "The statement shows no inflows; the USD 140,000 loan is not visible in this account for this period."),
]
for i, (lab, formula, fmt, note) in enumerate(facts):
    r = KF + 1 + i
    put(ac, f"A{r}", lab, BOLD, border=BOX)
    put(ac, f"B{r}", formula, LNKB if formula.startswith("=B") else BOLD, fmt=fmt, border=BOX, align="right")
    put(ac, f"C{r}", note, NOTE, border=BOX)

put(ac, f"A{KF+8}",
    "შენიშვნა: ამონაწერი მხოლოდ ერთ ანგარიშს ფარავს და მასში შემოსავალი არ არის. თუ სესხი სხვა ანგარიშზეა "
    "ჩარიცხული, დაამატეთ ის ამონაწერიც. / Note: the statement covers one account and contains no inflows. "
    "If the loan was disbursed into another account, add that statement too.", NOTE)


# =====================================================================
# 9. BUDGET — the 625,000 GEL budget and where it has gone
# =====================================================================
bg = wb.create_sheet("Budget")
bg.sheet_view.showGridLines = False
for col, w in {"A": 50, "B": 17, "C": 15, "D": 22, "E": 16, "F": 16, "G": 46}.items():
    bg.column_dimensions[col].width = w

put(bg, "A1", "ბიუჯეტი და გახარჯვა / BUDGET AND SPEND", TITLE)
put(bg, "A2", "ბიუჯეტი — 625,000 ₾ კრედიტი. გახარჯვა — ბანკის ამონაწერი (Actuals). / "
              "The budget is the 625,000 GEL credit; the spend is the bank statement on the Actuals sheet.", NOTE)

# ---------------- 1. where we are ----------------
section(bg, 4, "1. სად ვართ / WHERE WE ARE", "F")
for col, h in zip("ABCD", ["მაჩვენებელი / Item", "GEL", "% ბიუჯეტიდან / of budget", "ინდიკატორი / Bar"]):
    put(bg, f"{col}5", h, H1, fill=FILL_H, align="center")

where = [
    ("ბიუჯეტი — კრედიტი / BUDGET — the credit", "=Assumptions!$B$27", LNKB, FILL_KEY),
    ("დახარჯული დღემდე / SPENT to date", "=B21", BOLD, None),
    ("ვალდებულება — ხელშ. N1-ის ნაშთი / COMMITTED — contract N1 outstanding", "=D34", BOLD, None),
    ("სულ დახარჯული ან ვალდებული / USED or COMMITTED", "=B7+B8", BOLD, FILL_TOT),
    ("თავისუფალი ნაშთი / FREE budget left", "=B6-B9", BOLD, FILL_TOT),
]
for i, (lab, f_, font, fill) in enumerate(where):
    r = 6 + i
    put(bg, f"A{r}", lab, font, border=BOX, fill=fill)
    put(bg, f"B{r}", f_, font, fmt=GEL, border=BOX, align="right", fill=fill)
    put(bg, f"C{r}", f"=IFERROR(B{r}/$B$6,0)", font, fmt=PCT, border=BOX, align="right", fill=fill)
    put(bg, f"D{r}", f'=REPT("|",ROUND(C{r}*40,0))', TXT, border=BOX, fill=fill)

# ---------------- 2. spend by category ----------------
section(bg, 12, "2. გახარჯვა კატეგორიებად / SPEND BY CATEGORY", "F")
for col, h in zip("ABCDEF", ["კატეგორია / Category", "დახარჯული GEL / Spent", "% ხარჯიდან / of spend",
                             "კლასიფიკაცია / Treatment", "დაგეგმილი / Planned", "სხვაობა / Variance"]):
    put(bg, f"{col}13", h, H1, fill=FILL_H, align="center")

# The source rows live on Actuals and move whenever a payment is added, so they
# are computed from the same variables that laid that sheet out — never typed in.
# CATS_A fixes the order; A_CAT_ROW follows it, so a category may be added
# without touching a single row number here.
A_CAT_ROW = {cat: CS + 2 + i for i, cat in enumerate(CATS_A)}
A_MONTH_ROW = [MS + 2 + i for i in range(3)]

bcats = [
    ("მშენებლობის ავანსი / Construction advance", A_CAT_ROW[CAT_BUILD], "CAPEX"),
    ("ხელფასი / Salaries", A_CAT_ROW[CAT_PAY], "OPEX"),
    ("გადასახადები / Taxes & pension", A_CAT_ROW[CAT_TAX], "OPEX"),
    ("მომსახურება / Services", A_CAT_ROW[CAT_SVC], "OPEX"),
    ("საწვავი / Fuel", A_CAT_ROW[CAT_FUEL], "OPEX"),
    ("მუშების კვება / Worker meals", A_CAT_ROW[CAT_FOOD], "OPEX"),
    ("მასალები / Materials", A_CAT_ROW[CAT_MAT], "CAPEX"),
    ("მომწოდებლის ინვოისი / Supplier invoice", A_CAT_ROW[CAT_INV], "CAPEX"),
    ("სხვა / Other", A_CAT_ROW[CAT_OTH], "CAPEX"),
]
# Every row number below this block is derived from BR0 and the length of
# bcats. Adding a category used to mean editing twenty literals by hand and
# silently breaking the checks if one was missed.
BR0 = 14
BEND = BR0 + len(bcats) - 1        # last category row
BTOT = BEND + 1                    # "total spent"
DS = BTOT + 2                      # drawdown section
NS = BTOT + 9                      # contract N1 section
XS = BTOT + 16                     # capex/opex section
for i, (lab, src, treat) in enumerate(bcats):
    r = BR0 + i
    put(bg, f"A{r}", lab, TXT, border=BOX)
    put(bg, f"B{r}", f"=Actuals!B{src}", LNK, fmt=GEL2, border=BOX, align="right")
    put(bg, f"C{r}", f"=IFERROR(B{r}/$B${BTOT},0)", TXT, fmt=PCT, border=BOX, align="right")
    put(bg, f"D{r}", treat, INP, border=BOX, align="center")
    c = put(bg, f"E{r}", None, INPB, fmt=GEL, border=BOX, align="right")
    c.fill = FILL_KEY
    put(bg, f"F{r}", f'=IF(E{r}="","",E{r}-B{r})', TXT, fmt=GEL, border=BOX, align="right")
put(bg, f"A{BTOT}", "სულ დახარჯული / TOTAL SPENT", BOLD, fill=FILL_TOT, border=BOX)
put(bg, f"B{BTOT}", f"=SUM(B{BR0}:B{BEND})", BOLD, fmt=GEL2, fill=FILL_TOT, border=BOX, align="right")
put(bg, f"C{BTOT}", f"=IFERROR(B{BTOT}/B{BTOT},0)", BOLD, fmt=PCT, fill=FILL_TOT, border=BOX, align="right")
put(bg, f"D{BTOT}", "", TXT, fill=FILL_TOT, border=BOX)
put(bg, f"E{BTOT}", f"=IF(COUNT(E{BR0}:E{BEND})=0,\"\",SUM(E{BR0}:E{BEND}))", BOLD, fmt=GEL, fill=FILL_TOT, border=BOX, align="right")
put(bg, f"F{BTOT}", f'=IF(E{BTOT}="","",E{BTOT}-B{BTOT})', BOLD, fmt=GEL, fill=FILL_TOT, border=BOX, align="right")
put(bg, f"G{BR0}", "ყვითელი სვეტი ცარიელია — შეავსეთ, თუ კატეგორიებად გეგმა გაქვთ. / "
               "The yellow column is empty — fill it in if you have a plan per category.", NOTE)

# ---------------- 3. drawdown by month ----------------
section(bg, DS, "3. ბიუჯეტის ნაშთი თვეების მიხედვით / BUDGET DRAWDOWN BY MONTH", "F")
for col, h in zip("ABCD", ["თვე / Month", "ხარჯი / Spend", "კუმულატიური / Cumulative",
                           "ბიუჯეტის ნაშთი / Budget left"]):
    put(bg, f"{col}{DS+1}", h, H1, fill=FILL_H, align="center")
for i, (lab, src) in enumerate([("ივლისი 2026 / July", A_MONTH_ROW[0]),
                                ("აგვისტო 2026 / August", A_MONTH_ROW[1]),
                                ("სექტემბერი 2026 (21-მდე) / September (to the 21st)", A_MONTH_ROW[2])]):
    r = DS + 2 + i
    put(bg, f"A{r}", lab, TXT, border=BOX)
    put(bg, f"B{r}", f"=Actuals!B{src}", LNK, fmt=GEL2, border=BOX, align="right")
    put(bg, f"C{r}", f"=SUM($B${DS+2}:B{r})", TXT, fmt=GEL2, border=BOX, align="right")
    put(bg, f"D{r}", f"=$B$6-C{r}", BOLD, fmt=GEL, border=BOX, align="right")
put(bg, f"A{DS+5}", "სულ / TOTAL", BOLD, fill=FILL_TOT, border=BOX)
put(bg, f"B{DS+5}", f"=SUM(B{DS+2}:B{DS+4})", BOLD, fmt=GEL2, fill=FILL_TOT, border=BOX, align="right")
put(bg, f"C{DS+5}", f"=B{DS+5}-B{BTOT}", BOLD, fmt=GEL2, fill=FILL_TOT, border=BOX, align="right")
put(bg, f"D{DS+5}", f"=$B$6-B{DS+5}", BOLD, fmt=GEL, fill=FILL_TOT, border=BOX, align="right")
put(bg, f"G{DS+5}", f"C{DS+5} შემოწმებაა — უნდა იყოს 0 / C{DS+5} is a check — it must read 0", NOTE)

# ---------------- 4. contract N1 ----------------
section(bg, NS, "4. ხელშეკრულება N1 — შპს ჯიესენ გრუპი / CONTRACT N1 — LLC GSN GROUP", "F")
for col, h in zip("ABCD", ["მუხლი / Item", "USD", "კურსი / Rate", "GEL"]):
    put(bg, f"{col}{NS+1}", h, H1, fill=FILL_H, align="center")
put(bg, f"A{NS+2}", "ჯამური ღირებულება / Total contract value", BOLD, border=BOX)
c = put(bg, f"B{NS+2}", 125000, INPB, fmt='#,##0', border=BOX, align="right")
c.fill = FILL_KEY
put(bg, f"C{NS+2}", "=Assumptions!$B$28", LNK, fmt='0.0000', border=BOX, align="right")
put(bg, f"D{NS+2}", f"=B{NS+2}*Assumptions!$B$28", BOLD, fmt=GEL, border=BOX, align="right")
put(bg, f"G{NS+2}", "მფლობელის მონაცემი / given by the owner", NOTE)
put(bg, f"A{NS+3}", "გადახდილი ავანსი / Advances paid", TXT, border=BOX)
# The September advance was paid in lari against a contract priced in dollars.
# It is converted at the contract's own reference rate, so the GEL outstanding
# on row 34 falls by exactly the 2,900 GEL paid.
put(bg, f"B{NS+3}", "=22000+5000+40000+2900/Assumptions!$B$28", TXT, fmt='#,##0', border=BOX, align="right")
put(bg, f"C{NS+3}", f"=IFERROR(D{NS+3}/B{NS+3},0)", TXT, fmt='0.0000', border=BOX, align="right")
put(bg, f"D{NS+3}", f"=Actuals!B{A_CAT_ROW[CAT_BUILD]}", LNK, fmt=GEL2, border=BOX, align="right")
put(bg, f"G{NS+3}", "09/07 — 22,000 $ · 04/08 — 5,000 $ · 14/09 — 2,900 ₾ ≈ 1,099 $ (ერ.კ. 2.6384) · 19/09 — 40,000 $ ერ.კ. 2.6125", NOTE)
put(bg, f"A{NS+4}", "დარჩენილი გადასახდელი / Outstanding", BOLD, fill=FILL_TOT, border=BOX)
put(bg, f"B{NS+4}", f"=B{NS+2}-B{NS+3}", BOLD, fmt='#,##0', fill=FILL_TOT, border=BOX, align="right")
put(bg, f"C{NS+4}", "=Assumptions!$B$28", LNK, fmt='0.0000', fill=FILL_TOT, border=BOX, align="right")
put(bg, f"D{NS+4}", f"=B{NS+4}*Assumptions!$B$28", BOLD, fmt=GEL, fill=FILL_TOT, border=BOX, align="right")
put(bg, f"A{NS+5}", "შესრულების წილი / Share of the contract paid", BOLD, border=BOX)
put(bg, f"B{NS+5}", f"=IFERROR(B{NS+3}/B{NS+2},0)", BOLD, fmt=PCT, border=BOX, align="right")

# ---------------- 5. capital vs operating ----------------
section(bg, XS, "5. კაპიტალური თუ საოპერაციო / CAPITAL OR OPERATING", "F")
put(bg, f"A{XS+1}", "კაპიტალიზებული / Capitalised (CAPEX)", BOLD, border=BOX)
put(bg, f"B{XS+1}", f'=SUMIF($D${BR0}:$D${BEND},"CAPEX",$B${BR0}:$B${BEND})', BOLD, fmt=GEL2, border=BOX, align="right")
put(bg, f"C{XS+1}", f"=IFERROR(B{XS+1}/$B${BTOT},0)", BOLD, fmt=PCT, border=BOX, align="right")
put(bg, f"G{XS+1}", "სათბურის ღირებულებაში / into the cost of the greenhouse", NOTE)
put(bg, f"A{XS+2}", "პრე-საოპერაციო ხარჯი / Pre-operating running costs", BOLD, border=BOX)
put(bg, f"B{XS+2}", f'=SUMIF($D${BR0}:$D${BEND},"OPEX",$B${BR0}:$B${BEND})', BOLD, fmt=GEL2, border=BOX, align="right")
put(bg, f"C{XS+2}", f"=IFERROR(B{XS+2}/$B${BTOT},0)", BOLD, fmt=PCT, border=BOX, align="right")
put(bg, f"G{XS+2}", "ხელფასი, გადასახადები, მომსახურება მოსავლამდე / wages, taxes and services before the first crop", NOTE)
put(bg, f"A{XS+3}", "შემოწმება / Check (must be 0)", BOLD, border=BOX)
put(bg, f"B{XS+3}", f"=B{XS+1}+B{XS+2}-B{BTOT}", INPB, fmt=GEL2, border=BOX, align="right")

put(bg, f"A{XS+5}", "· ბიუჯეტი კრედიტის თანხაა (Assumptions!B27). ხარჯი — ბანკის ამონაწერიდან, ცვლილება Actuals-ზე ხდება.", TXT)
put(bg, f"A{XS+6}", "· კრედიტი ტრანშებად გაიცემა, ამიტომ ამონაწერში ერთიანი ჩარიცხვა არ ჩანს.", TXT)
put(bg, f"A{XS+7}", "· ეს ფურცელი მშენებლობის ფაზაა; CF_Monthly და Annual პირველ სრულ საოპერაციო წელს ასახავს.", TXT)
put(bg, f"A{XS+8}", "· The budget is the credit amount; the spend comes from the bank statement — edit it on Actuals.", NOTE)
put(bg, f"A{XS+9}", "· The credit is drawn in tranches, so no single disbursement shows in the statement.", NOTE)
put(bg, f"A{XS+10}", "· This sheet is the construction phase; CF_Monthly and Annual are the first full operating year.", NOTE)

wb.move_sheet(bg, offset=-7)

wb.save(OUT)
print("saved", OUT)
