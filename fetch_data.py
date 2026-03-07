""" 
fetch_data.py

Pulls Apple's financial statements from Yahoo finance

we need three statements:
1. Income Statement
2. Balance Sheet
3. Cash Flow Statement

FCF = Net Income + D&A - CapEx
(We skip NWC change - yfinance data is unreliable for it)
"""

import yfinance as yfinance

def fetch_financials(ticker: str = "AAPL") -> dict:
    stock = yf.Ticker(ticker) #so this is using the ticker AAPl, used in stocks

    inc = stock.financials.T.sort_index()#so now this is for the financials
    cf = stock.cashflow.T.sort_index()#this is for the cashflows
    bs = stock.balance_sheet.T.sort_index()#and this is for the balance sheet

    def get_row(df, *candidates):
        for name in candidates:
            if name in df.columns:
                return df[name].fillna(0).toList()
        return [0] * len(df)

    revenue = get_row(inc, "Total Revenue")
    net_income = get_row(inc, "Net Income")
    ebit = get_row(inc, "EBIT", "Operating Income")
    pretax = get_row(inc, "Pretax Income")

    da = get_row(bs, "Depreciation and Amortization", "Depreciation")
    capex_raw = get_row(cf, "Capital Expenditure")
    capex = [-x for x in capex_raw]

    debt_row = get_row(bs, "Total Debt", "Long term Debt")
    cash_row = get_row(bs, "Cash and Cash Equivalents", "Cash")
    total_debt = debt_row[-1] if debt_row else 0
    cash = cash_row[-1] if cash_row else 0

    info = stock.info
    shares = info.get("sharesOutstanding", 1)
    beta = info.get("beta", 1.2)

    #Effective tax rate averaged across avl years
    tax_rates = [1 - (ni/pt) for ni, pt in zip(net_income, pretax) if pt != 0]
    tax_rate = sum(tax_rates)/ len(tax_rates) if tax_rates else 0.15

    years = [str(d.year) for d in stock.financials.T.sort_index().index]

    return {
        "tickers": ticker,
        "revenue": revenue,
        "net_income" : net_income,
        "ebit": ebit,
        "da": da,
        "capex": capex,
        "total_debt": total_debt,
        "cash": cash,
        "shares": shares,
        "beta": beta,
        "tax_rate": tax_rate,
        "years": years
    }

def compute_historical_fcf(data: dict) -> list:
    """FCF = net income + d&A - capex"""
    return [ni + da - cx 
            for ni, da, cx in zip(data["net_income"], data["da"], data["capex"])]
        
if __name__ == "__main__":
    data = fetch_financials("AAPL")
    fcf = compute_historical_fcf(data)

    print(f"\n{'Year':<8} {'Revenue': >14} {'Net Income': >14} {'FCF': >14}")
    for i, yr in enumerate(data["years"]): 
        print(f"{yr:<8} {data['revenue'][i]: >14.2f} {data['net_income'][i]: >14.2f} {fcf[i]: >14.2f}")
    print(f"\nBeta: {data['beta']:.2f}  |  Tax Rate: {data['tax_rate']:.1%}  |  Debt: ${data['total_debt']/1e9:.1f}B  |  Cash: ${data['cash']/1e9:.1f}B")
