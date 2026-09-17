# Greenhouse cash-flow model — 2,000 m², two harvests per year

**File:** `Greenhouse_CashFlow_2000m2.xlsx` (bilingual Georgian / English)
**Rebuild:** `python build_model.py` (requires `openpyxl`)

## Inputs given

| Item | Value |
|---|---|
| Greenhouse area | 2,000 m² |
| Harvest cycles | 2 per year (winter + summer) |
| Winter harvest | 80–90 → **85 t** used (see note) @ **4.50 GEL/kg** |
| Summer harvest | **70 t** @ **3.00 GEL/kg** |
| Annual OPEX | **150,000 GEL** |
| Bank credit | **625,000 GEL** — Cartu Bank, contract GA/1-876787–001 |

> **Note on the winter figure.** The request said "winter harvest 80-90 kg". For a 2,000 m²
> house that can only be tonnes — 85 t = 42.5 kg/m², against the summer crop's 35 kg/m².
> The midpoint (85 t) is used. Change `Assumptions!B10` if a different number was meant;
> every downstream sheet follows.

## Model's own assumptions (all editable, all flagged in the workbook)

| Assumption | Default | Where |
|---|---|---|
| FX rate | **2.6384 GEL/USD — actual, not assumed** (used for the USD contract) | `Assumptions!B28` |
| Loan terms | **all taken from the signed contract**, nothing assumed | `Assumptions!B27:B37` |
| Second interest rate | 13.40% from month 24 — **implied by the bank's own Annex 1**, not guessed | `Assumptions!B36` |
| Operating Year 1 | mapped to loan year 2 (Jul 2027 – Jun 2028), the first amortising year | `Assumptions!B48` |
| OPEX split | 8 categories summing to 150,000 GEL, with monthly seasonality | `OPEX` sheet |
| Sales seasonality | winter crop sold Dec–Apr, summer crop Jun–Sep | `CF_Monthly!B7:M8` |
| Growth (Years 2–5) | yield +2%, price +3%, OPEX +4% p.a. | `Assumptions!B39:B41` |
| Profit tax | 0% — Georgia taxes distributed profit only, and primary agri production is exempt below 200,000 GEL turnover | `Assumptions!B44` |
| Phase | Operating phase: credit already drawn, greenhouse already built (no CAPEX in Year 1) | `Assumptions!B46` |

## Sheets

1. **Instructions** — how to use, colour legend, every assumption and its source.
2. **Budget** — the 625,000 GEL budget and where it stands. Start here.
3. **Assumptions** — all drivers plus a Year-1 output panel.
4. **OPEX** — 150,000 GEL split into 8 categories × 12 months, with a 100% check per row.
5. **Loan** — the 120-month schedule with the agency co-financing, checked against the bank's Annex 1.
6. **CF_Monthly** — operating Year 1, month by month: volume, revenue, OPEX, EBITDA, debt service, cash.
7. **Annual** — Years 1–5: P&L, debt service, net and cumulative cash flow, DSCR, cost per kg.
8. **Sensitivity** — yield × price grids (−20% to +20%) for net cash flow and DSCR, plus break-even.
9. **Actuals** — the bank statement, verbatim. The only place spending is entered.

## Where the budget stands

The budget is the credit: **625,000 GEL**. Everything on the `Budget` sheet is derived from it.

| | GEL | of budget |
|---|---:|---:|
| **Budget — the credit** | 625,000.00 | 100.0% |
| Spent to date | 90,541.21 | 14.5% |
| Committed — contract N1 outstanding | 258,563.20 | 41.4% |
| **Used or committed** | **349,104.41** | **55.9%** |
| **Free budget left** | **275,895.59** | **44.1%** |

Drawdown by month, from the statement:

| Month | Spend | Cumulative | Budget left |
|---|---:|---:|---:|
| July 2026 | 68,664.21 | 68,664.21 | 556,335.79 |
| August 2026 | 21,477.00 | 90,141.21 | 534,858.79 |
| September 2026 (to the 8th) | 400.00 | 90,541.21 | 534,458.79 |

Contract N1 with LLC GSN Group is **USD 125,000**: USD 27,000 paid (**21.6%**), USD 98,000
outstanding, which is the 258,563 GEL commitment above. Of the 90,541 GEL spent, **78,971 is
capitalised** into the greenhouse and **11,570 is pre-operating** wages, taxes and services.
The capital/operating call is the model's — change it in column D of `Budget`.

To update the picture, add the new rows to `Actuals`; the `Budget` sheet re-adds itself.
Column E of `Budget` is an empty yellow column for a per-category plan, if you want one.

## The loan behind the budget

`Mukrlhranis loan contract` on Drive: **625,000 GEL from JSC Cartu Bank**, contract
GA/1-876787–001 of 17/06/2026, maturing 17/06/2036 over **120 months**. Interest is 12.64% to
17/06/2028, then the refinancing rate plus 5.14%. Months 1–12 pay nothing, month 13 clears the
accrued interest, then a 107-month annuity.

**The Rural Development Agency co-finances 11% p.a. of the principal for up to 48 months.** Over
those four years it pays **255,763 GEL** of interest. The contractual interest bill is 530,014
GEL; the company's share is **274,251 GEL**. That is also why the DSCR runs 9.4x → 8.1x → 7.8x
and then steps down to **4.3x in operating year 4**, when the co-financing ends.

### Reconciliation against the bank's own Annex 1

The contract's repayment schedule is printed per 1,000 units (principal 1,000.00, interest
847.49, total 1,847.49), so it scales by 625 for the 625,000 GEL credit. The model reproduces it:

| | Bank's Annex 1 | Model | Difference |
|---|---:|---:|---:|
| Total principal | 625,000.00 | 625,000.00 | 0.00 |
| Total interest | 529,681.25 | 530,014.14 | 332.89 |
| Total repayable | 1,154,681.25 | 1,155,014.14 | 332.89 |
| Annuity, months 14–23 | 9,768.75 | 9,766.07 | −2.68 |
| Annuity, months 24–120 | 10,012.50 | 10,018.25 | +5.75 |

0.06% apart, which is the bank accruing on actual days against the model's equal months. The
step in the annuity at month 24 is what pins the second rate: solving the bank's own figures
gives 13.40%, i.e. a refinancing rate of 8.26% plus the contractual 5.14% margin.

## The spending data

**`transaction_history_all_accounts_20260401_20260909.csv`** — account GE66CR0000009572073602,
LLC Mukhrani 2026 (შპს მუხრანი 2026). 15 payments between 1 July and 8 September 2026 totalling
**90,541.21 GEL**, and **no inflows at all** — no credit tranche reaches this account in this
period. The statement is reproduced verbatim on `Actuals` and drives the `Budget` sheet.

| Category | GEL | Treatment |
|---|---:|---|
| Construction advances (LLC GSN Group, contract N1 of 7/6/2026) | 71,144.80 | CAPEX |
| Materials (electrical, metal mounting) | 4,660.00 | CAPEX |
| Supplier invoices | 2,859.41 | CAPEX |
| Other (public registry) | 307.00 | CAPEX |
| Salaries | 8,000.00 | pre-operating |
| Services | 2,100.00 | pre-operating |
| Taxes & pension | 1,470.00 | pre-operating |
| **Total** | **90,541.21** | |

**The FX rate is now fact, not assumption.** The 9 July transfer of USD 22,000 = GEL 58,044.80
states the rate 2.6384 in its own payment description (the 4 August transfer of USD 5,000 =
GEL 13,100 implies 2.62; blended 2.6350). `Assumptions!B28` carries 2.6384, and it is what values
the USD 125,000 contract with GSN Group at 329,800 GEL.

## Year 1 results at the default assumptions

| | GEL |
|---|---|
| Revenue (85 t × 4.50 + 70 t × 3.00) | 592,500 |
| OPEX | (150,000) |
| **EBITDA** (74.7% margin) | **442,500** |
| Debt service (interest net of agency co-financing, plus principal) | (47,169) |
| **Net cash flow** | **395,331** |
| DSCR | 9.38x |

Debt service is 47,169 GEL in operating year 1 and stays near that while the agency co-finances,
then steps up to about 120,000 GEL a year once the 48 months end. Monthly cash never turns negative, so the *operating* year needs no extra
working capital. The construction phase is a separate question and lives on `Budget`.

The EBITDA margin is high because the stated 150,000 GEL OPEX is only 25% of revenue. If the
150,000 excludes items such as seedlings, heating or labour, add them on the `OPEX` sheet —
every other sheet recalculates.

## Verification

LibreOffice does not run in this environment, so the workbook was checked with the `formulas`
engine instead (`cache_values.py` runs it): 2,988 cells evaluated, **0 formula errors**. All
internal checks tie out — the statement categories against the statement total
(`Actuals!B39` = 0), the by-month split against the same total (`Budget!C28` = 0), the
capital/operating split against the spend total (`Budget!B40` = 0),
OPEX total vs. the stated 150,000 (`Assumptions!B24` = 0), Year 1 annual vs. monthly
(`Annual!B38` = 0), seasonality rows = 100%, the loan amortises to exactly zero in month 120,
and the schedule reconciles to the bank's Annex 1 within 333 GEL on 530,014. Cached results are stored in the file and `fullCalcOnLoad` is set, so
Excel and Google Sheets recalculate everything from the formulas on open.
