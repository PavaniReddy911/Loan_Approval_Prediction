import streamlit as st
import random

st.set_page_config(
    page_title="Loan Approval Prediction System",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Loan Approval Prediction System")
st.markdown("### AI Powered Loan Risk Assessment")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 18, 100, 30)
    income = st.number_input("Annual Income", 0, 10000000, 50000)
    credit_score = st.number_input("Credit Score", 300, 900, 700)

with col2:
    loan_amount = st.number_input("Loan Amount", 1000, 10000000, 100000)
    interest_rate = st.number_input("Interest Rate (%)", 1.0, 30.0, 10.0)
    loan_term = st.number_input("Loan Term (Months)", 1, 360, 60)

if st.button("Predict"):

    # Demo Logic

    if credit_score > 700 and income > 50000:
        loan_status = "Approved"
        risk_level = "Low"
        risk_score = random.randint(10, 30)
        segment = "Premium Customer"

    elif credit_score > 600:
        loan_status = "Approved"
        risk_level = "Medium"
        risk_score = random.randint(31, 70)
        segment = "Regular Customer"

    else:
        loan_status = "Rejected"
        risk_level = "High"
        risk_score = random.randint(71, 95)
        segment = "High Risk Customer"

    st.success("Prediction Completed")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Loan Status", loan_status)
    c2.metric("Risk Score", f"{risk_score}%")
    c3.metric("Risk Level", risk_level)
    c4.metric("Customer Segment", segment)

    st.markdown("---")

    st.subheader("Prediction Summary")

    st.json({
        "loan_status": loan_status,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "customer_segment": segment
    })
