"""
wacc.py
-------
Calculates WACC from first principles.

WACC = (E/V) × Ke  +  (D/V) × Kd × (1 - Tax Rate)

Ke via CAPM:
    Ke = Rf + β × (Rm - Rf)

    Rf  = risk-free rate (10yr Treasury, ~4.3% as of early 2025)
    β   = beta (how much the stock moves relative to the market)
    ERP = equity risk premium (~5.5%, from Damodaran)

Debt gets a tax shield because interest expense is tax-deductible.
That's why cost of debt is multiplied by (1 - tax rate).
"""
def cost_of_equity(risk_free_rate: float, beta: float, erp: float) -> float:
    """CAPM. e.g. 0.043 + 1.2 * 0.05 = 0.109(10.9%)"""
    return risk_free_rate + beta * erp

def cost_of_debt(interest_expense: float, total_debt: float) -> float:
    """Pre tax-cost of debt  = interest expense/ total debt"""
    if total_debt == 0:
        return 0.03
    return abs(interest_expense)/ total_debt

def calculate_wacc(market_cap, total_debt, ke, kd, tax_rate) -> dict:
    V = market_cap + total_debt
    we = market_cap / V
    wd = total_debt / V
    kd_after_tax = kd * (1 - tax_rate)
    wacc = we * ke + wd * kd_after_tax

    return {
        "market_cap":      market_cap,
        "total_debt":      total_debt,
        "weight_equity":   we,
        "weight_debt":     wd,
        "cost_of_equity":  ke,
        "cost_of_debt_pretax":  kd,
        "cost_of_debt_aftertax": kd_after_tax,
        "wacc":            wacc,
    }