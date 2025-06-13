import numpy_financial as npf

def calculate_cash_flows(initial_investment, revenues, expenses, depreciation, tax_rate, working_capital_changes):
    cash_flows = []
    for i in range(len(revenues)):
        ebit = revenues[i] - expenses[i] - depreciation[i]
        tax = ebit * tax_rate
        net_income = ebit - tax
        cash_flow = net_income + depreciation[i] - working_capital_changes[i]
        cash_flows.append(cash_flow)
    cash_flows[0] -= initial_investment
    return cash_flows

def calculate_npv(cash_flows, discount_rate):
    return round(npf.npv(discount_rate, cash_flows), 2)

def calculate_irr(cash_flows):
    return round(npf.irr(cash_flows), 4)

def calculate_payback_period(cash_flows):
    cumulative = 0
    for i, cf in enumerate(cash_flows):
        cumulative += cf
        if cumulative >= 0:
            return i
    return None
