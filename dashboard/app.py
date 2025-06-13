import streamlit as st
import pandas as pd
import numpy_financial as npf
import plotly.graph_objects as go
import os
import sys

# Add path to parent folder so 'scripts' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.data_loader import load_project_inputs
from scripts.wacc_calculator import calculate_wacc
from scripts.cashflow_model import calculate_cash_flows, calculate_npv, calculate_irr, calculate_payback_period

# ----- Page Config -----
st.set_page_config(page_title="Capital Budgeting | Futura Tech", layout="wide")

# ----- Header -----
st.markdown("<h1 style='text-align: center; color: navy;'>🏗️ Capital Budgeting Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Futura Tech Inc. - Factory Expansion Project in Singapore</h4>", unsafe_allow_html=True)
st.markdown("---")

# ----- File Upload -----
uploaded_file = st.file_uploader("📥 Upload 'Futura_Tech.xlsx'", type="xlsx")

if uploaded_file:
    df = load_project_inputs(uploaded_file)
    
    with st.expander("🔍 View Financial Driver Inputs"):
        st.dataframe(df)

    # Simulated data (you'll replace this with Excel-driven parsed values)
    equity = 5000000
    debt = 3000000
    cost_equity = 0.12
    cost_debt = 0.06
    tax_rate = 0.3
    initial_investment = 7000000

    revenues = [1e6, 1.2e6, 1.5e6, 1.8e6, 2e6]
    expenses = [0.6e6, 0.7e6, 0.8e6, 0.9e6, 1e6]
    depreciation = [500000] * 5
    wc_changes = [20000, 25000, 20000, 15000, 10000]

    # ----- Financial Calculations -----
    wacc = calculate_wacc(equity, debt, cost_equity, cost_debt, tax_rate)
    cash_flows = calculate_cash_flows(initial_investment, revenues, expenses, depreciation, tax_rate, wc_changes)
    npv = calculate_npv(cash_flows, wacc)
    irr = calculate_irr(cash_flows)
    payback = calculate_payback_period(cash_flows)

    # ----- KPI Cards -----
    st.markdown("### 📈 Key Financial Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("WACC", f"{wacc * 100:.2f}%", "Weighted Avg. Cost of Capital")
    col2.metric("NPV", f"${npv:,.2f}", "Net Present Value")
    col3.metric("IRR", f"{irr * 100:.2f}%", "Internal Rate of Return")
    col4.metric("Payback Period", f"{payback} years", "Breakeven Point")

    # ----- Tabs -----
    tab1, tab2 = st.tabs(["📊 Cash Flow Chart", "📃 Raw Cash Flow Table"])

    with tab1:
        years = list(range(1, len(cash_flows) + 1))
        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=cash_flows, marker_color='seagreen', name='Net Cash Flow'))
        fig.update_layout(
            title="📉 Annual Net Cash Flows",
            xaxis_title="Year",
            yaxis_title="Cash Flow ($)",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.dataframe(pd.DataFrame({
            "Year": list(range(1, len(cash_flows)+1)),
            "Cash Flow": cash_flows
        }))

    # ----- Final Recommendation -----
    st.markdown("---")
    if npv > 0 and irr > wacc:
        st.success("✅ Based on the financial metrics, the project is financially viable and should be pursued.")
    else:
        st.error("❌ The project does not meet investment thresholds. Recommend reassessment.")

else:
    st.info("📄 Please upload the 'Futura_Tech.xlsx' file to begin analysis.")
