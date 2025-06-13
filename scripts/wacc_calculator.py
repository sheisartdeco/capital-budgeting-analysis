def calculate_wacc(equity, debt, cost_equity, cost_debt, tax_rate):
    v = equity + debt
    wacc = (equity / v) * cost_equity + (debt / v) * cost_debt * (1 - tax_rate)
    return round(wacc, 4)
