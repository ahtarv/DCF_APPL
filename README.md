# DCF Model — Apple (AAPL)

A beginner-friendly Discounted Cash Flow model built in Python + Excel.
Pulls real financial data, projects Free Cash Flow, computes intrinsic share price,
and outputs a sensitivity table showing how assumptions drive valuation.

---

## What This Model Does

1. Fetches Apple's historical financials (income statement, balance sheet, cash flow)
2. Computes historical Free Cash Flow
3. Projects FCF forward 5 years using a growth assumption
4. Calculates WACC from first principles (CAPM for cost of equity, after-tax cost of debt)
5. Discounts projected FCFs back to present value
6. Adds Terminal Value (Gordon Growth Model)
7. Derives intrinsic share price
8. Outputs a sensitivity table (WACC × terminal growth rate)
9. Writes everything to a formatted Excel workbook

---

## Project Structure

```
dcf-model/
│
├── dcf.py                  # Main script — run this
├── fetch_data.py           # Pulls financials from yfinance
├── wacc.py                 # WACC calculation module
├── projections.py          # FCF projection logic
├── terminal_value.py       # Terminal value + PV math
├── sensitivity.py          # Sensitivity table builder
├── excel_output.py         # Writes model to Excel
│
├── outputs/
│   └── AAPL_DCF.xlsx       # Generated Excel model
│
├── requirements.txt
└── README.md
```

---

## Concepts Used

| Concept | Where It Appears |
|---|---|
| Free Cash Flow | `fetch_data.py`, `projections.py` |
| Time Value of Money | `terminal_value.py` |
| WACC | `wacc.py` |
| CAPM (Cost of Equity) | `wacc.py` |
| Gordon Growth Model | `terminal_value.py` |
| Sensitivity Analysis | `sensitivity.py` |
| Net Present Value | `terminal_value.py` |

---

## Key Formulas

**Free Cash Flow**
```
FCF = Net Income + D&A − CapEx − ΔNWC
```

**Cost of Equity (CAPM)**
```
Ke = Rf + β × (Rm − Rf)

Rf  = risk-free rate (10-year US Treasury yield)
β   = beta (Apple's sensitivity to market movements)
Rm  = expected market return (~10% historically for S&P 500)
```

**WACC**
```
WACC = (E/V) × Ke  +  (D/V) × Kd × (1 − Tax Rate)

E = market value of equity (market cap)
D = market value of debt
V = E + D
```

**Discounted FCF**
```
PV(FCFₜ) = FCFₜ / (1 + WACC)^t
```

**Terminal Value (Gordon Growth Model)**
```
TV = FCF₅ × (1 + g) / (WACC − g)

g = perpetuity growth rate (typically 2–3%, close to long-run GDP growth)
```

**Intrinsic Share Price**
```
Enterprise Value  = Σ PV(FCFs) + PV(Terminal Value)
Equity Value      = Enterprise Value − Net Debt
Intrinsic Price   = Equity Value / Diluted Shares Outstanding
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt**
```
yfinance
pandas
numpy
openpyxl
```

### 2. Run the model
```bash
python dcf.py
```

Output is written to `outputs/AAPL_DCF.xlsx`.

---

## Inputs & Assumptions

All assumptions live at the top of `dcf.py` — change them freely:

| Input | Default | Notes |
|---|---|---|
| Ticker | `AAPL` | Any ticker yfinance supports |
| Projection years | `5` | How many years to forecast FCF |
| Revenue growth rate | `8%` | Applied to project forward |
| EBIT margin | `30%` | Apple's approximate operating margin |
| Tax rate | `15%` | Apple's effective rate (lower due to international structure) |
| Risk-free rate | `4.3%` | Approx 10-year US Treasury as of early 2025 |
| Equity risk premium | `5.5%` | Damodaran's current US ERP estimate |
| Terminal growth rate | `3%` | Long-run perpetuity growth |

---

## Output: Excel Workbook

The generated `AAPL_DCF.xlsx` contains three sheets:

**Sheet 1 — Model**
Full projection table: revenue → EBIT → FCF → discounted FCF → enterprise value → intrinsic price

**Sheet 2 — WACC Build**
Step-by-step WACC calculation showing cost of equity (CAPM), cost of debt, and blended rate

**Sheet 3 — Sensitivity Table**
Intrinsic price at every combination of:
- WACC: 8% → 13% (columns)
- Terminal growth rate: 1% → 4% (rows)

---

## How to Read the Sensitivity Table

The sensitivity table is the most important output. It shows you that a DCF is not a single number — it's a *range* driven by assumptions.

```
Example output (illustrative):

              WACC
              8%      9%      10%     11%     12%
g   1%       $168    $152    $138    $126    $115
    2%       $181    $163    $147    $133    $121
    3%       $198    $177    $159    $143    $130    ← base case
    4%       $221    $196    $174    $156    $141
```

If Apple's market price falls inside or below this range → potentially undervalued.
If market price is well above the entire range → market is pricing in assumptions more optimistic than yours.

---

## Learning Path

If you're building this to learn, do it in this order:

1. Run `dcf.py` end-to-end and look at the Excel output
2. Read `fetch_data.py` — understand what each financial line item means
3. Read `wacc.py` — trace through the CAPM calculation manually
4. Change the terminal growth rate from 3% to 1% and 4% — observe the price swing
5. Change WACC by ±2% — observe the price swing
6. Read about why Terminal Value drives 60–80% of total DCF value

The goal isn't a precise price target. The goal is to understand *which assumptions matter most* and by how much.

---

## Limitations (Important)

- **yfinance data is not always clean** — verify key numbers against SEC filings
- **DCF is highly sensitive to terminal value assumptions** — small changes in `g` or WACC cause large price swings
- **This model uses simplified FCF** — a professional model would adjust for stock-based compensation, lease obligations, and more
- **No mean reversion** — we apply a flat growth rate; real analysts use declining growth rates over the projection period
- **Survivorship bias in assumptions** — Apple's historical margins are exceptional; projecting them forward may be optimistic

---
