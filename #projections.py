#projections.py 

#projects FCF forward using a weighted average of historical growth.
#why weighted average over simple average
#a simple average treats 2018's 50% and 2024's 19% equally,
#but 2024 is far more relevant to what the business will do next year

#why we still cap/floor the rate:
#weighted average can still be distored by extreme outliers 
# a floor of -20 % and ceiling of 40% keeps projections in a realistic range for a mature business

#how weight work:
# Year 1 gets weight 1, year 2 gets weight 2, Most recent gets weight N

def compute_growth_rates(fcf_list: list) -> list:
    """Computes year over year FCF growth rates from a list of historical FCFS.
    Skips any where prior year FCF was 0 or negative (can't compute %)
    """

    rates = []

    for i in range(1, len(fcf_list)):
        prev = fcf_list[i-1]
        curr = fcf_list[i]
        if prev <= 0:
            continue
        rates.append((curr-prev)/ prev)
    return rates

def weighted_avg_growth(growth_rates: list) -> float:
    """Assigns linearly increasing weights to growth rates.
    Most recent rate gets the highest weight.

    e.g. 4 rates -> weights [1 , 2, 3, 4], sum = 10
    weighted avg = (1*r1 + 2*r2 + 3*r3 + 4*r4) / 10
    """
    n = len(growth_rates)
    if n == 0:
        return 0.08

    weights  = list(range(1, n+1))
    total_weight = sum(weights)
    weighted_sum = sum(r * w for r, w in zip(growth_rates, weights))
    return weighted_sum / total_weight

def project_fcf(
    fcf_history: list,
    years: int =5,
    floor: float = -0.20,
    ceiling: float = 0.40,
    override_rate: float = None
) -> dict:
    """
        Projects FCF forward N years using weighted historical growth.
        Returns a dict with:
            -projected_fcf : list of projected FCF values
            -growth_rate : the weighted average rate used
            -growth_history : year - over - year rates computed history
    """
    growth_rates = compute_growth_rates(fcf_history)

    if override_rate is not None:
        growth_rate = override_rate
    else:
        raw_rate = weighted_avg_growth(growth_rates)
        growth_rate = max(floor, min(ceiling, raw_rate))

    projections = []
    fcf = fcf_history[-1]
    for _ in range(years):
        fcf *= (1 + growth_rate)
        projections.append(fcf)
    return {
        "projected_fcf": projections,
        "growth_rate": growth_rate,
        "growth_history": growth_rates
    }