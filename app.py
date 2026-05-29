import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Loan Approval Prediction System",
    page_icon="🏦",
    layout="wide"
)

# ==========================
# LOAD MODELS
# ==========================

@st.cache_resource
def load_models():
    logistic = joblib.load("logistic.pkl")
    rf = joblib.load("random_forest.pkl")
    scaler = joblib.load("scaler.pkl")
    pca = joblib.load("pca.pkl")
    kmeans = joblib.load("kmeans.pkl")

    return logistic, rf, scaler, pca, kmeans

logistic, rf, scaler, pca, kmeans = load_models()

# ==========================
# HEADER
# ==========================

st.title("🏦 AI Loan Approval Prediction System")
st.markdown("---")

# ==========================
# INPUTS
# ==========================

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    income = st.number_input(
        "Annual Income",
        min_value=0,
        value=50000
    )

    credit_score = st.number_input(
        "Credit Score",
        min_value=300,
        max_value=900,
        value=700
    )

with col2:
    loan_amount = st.number_input(
        "Loan Amount",
        min_value=1000,
        value=100000
    )

    interest_rate = st.number_input(
        "Interest Rate (%)",
        min_value=0.0,
        max_value=50.0,
        value=10.0
    )

    loan_term = st.number_input(
        "Loan Term (Months)",
        min_value=1,
        value=60
    )

# ==========================
# PREDICT BUTTON
# ==========================

if st.button("Predict Loan Status"):

    try:

        features = np.array([
            [
                age,
                income,
                credit_score,
                loan_amount,
                interest_rate,
                loan_term
            ]
        ])

        scaled = scaler.transform(features)
        reduced = pca.transform(scaled)

        approval_pred = logistic.predict(reduced)[0]

        risk_prob = rf.predict_proba(reduced)[0][1]
        risk_score = int(risk_prob * 100)

        cluster = kmeans.predict(scaled)[0]

        if approval_pred == 0:
            loan_status = "✅ Approved"
        else:
            loan_status = "❌ Rejected"

        if risk_score <= 30:
            risk_level = "Low Risk"
        elif risk_score <= 70:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"

        segment_map = {
            0: "Premium Customer",
            1: "Regular Customer",
            2: "High Risk Customer"
        }

        segment = segment_map.get(
            cluster,
            "Unknown"
        )

        st.success("Prediction Completed")

        st.markdown("## Results")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Loan Status",
            loan_status
        )

        c2.metric(
            "Risk Score",
            f"{risk_score}%"
        )

        c3.metric(
            "Risk Level",
            risk_level
        )

        c4.metric(
            "Customer Segment",
            segment
        )

        st.markdown("---")

        st.json({
            "loan_status": loan_status,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "customer_segment": segment
        })

    except Exception as e:
        st.error(str(e))
