import os
import streamlit as st
from openai import OpenAI
import pandas as pd
import numpy as np
import datetime

# OpenAI Client
client = OpenAI(
    api_key=os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY"),
    base_url=os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL"),
)

# Page config
st.set_page_config(page_title="Inflation AI Agent", layout="wide")

# Title
st.title("📊 AI Inflation Forecast Agent")
st.markdown("Real-time CPI prediction using economic signals")

# Sidebar
st.sidebar.title("⚙️ Controls")
st.sidebar.write("Adjust inputs and explore features")

# Country Selector
country = st.selectbox("🌍 Select Country", ["India", "USA", "UK"])
st.write(f"📍 Selected Country: {country}")

# Inputs
price = st.slider("Price Increase (%)", 0, 20, 5)
sentiment = st.selectbox("Sentiment", ["Positive", "Neutral", "Negative"])
jobs = st.slider("Salary Growth (%)", 0, 20, 5)

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("📈 Price Change", f"{price}%")
col2.metric("💼 Salary Growth", f"{jobs}%")
col3.metric("🧠 Sentiment", sentiment)

st.markdown("---")

# Alert System
if price > 12 or sentiment == "Negative":
    st.error("🚨 High Inflation Alert!")
elif price > 7:
    st.warning("⚠️ Moderate Inflation Risk")
else:
    st.success("✅ Inflation Stable")

# Category Analysis
st.subheader("📊 Inflation by Category")
category_data = pd.DataFrame({
    "Inflation Rate (%)": [price + 2, price + 1, jobs, (price + jobs) / 2]
}, index=["Food", "Fuel", "Housing", "Core"])
st.bar_chart(category_data)

# Trend Graph
st.subheader("📉 Inflation Trend (Last 10 Days)")
trend = pd.DataFrame(
    np.random.randint(3, 7, size=10),
    columns=["Inflation (%)"]
)
st.line_chart(trend)

# Session History
if "history" not in st.session_state:
    st.session_state.history = []

# Predict Button
if st.button("Predict Inflation"):
    with st.spinner("Analyzing..."):
        prompt = f"""
        You are an AI inflation forecasting agent.

        Country: {country}
        Price increase: {price}%
        Sentiment: {sentiment}
        Salary growth: {jobs}%

        Give output in this format:

        CPI Prediction: __%
        Trend: Rising / Falling
        Top Drivers:
        1.
        2.
        3.
        Confidence: Low / Medium / High
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        st.subheader("📌 Prediction Result")
        st.write(result)

        # Save history
        st.session_state.history.append(result)

# History Display
st.subheader("📜 Prediction History")
for item in st.session_state.history:
    st.write(item)

# Scenario Simulation
st.subheader("🧪 Scenario Simulation")
scenario = st.selectbox("Choose Scenario", [
    "Normal Market",
    "High Inflation",
    "Economic Slowdown"
])

if scenario == "High Inflation":
    st.info("Simulating High Inflation Scenario")
elif scenario == "Economic Slowdown":
    st.info("Simulating Economic Slowdown")

# Download Report
report = f"""
Inflation Report
Country: {country}
Price Increase: {price}%
Salary Growth: {jobs}%
Sentiment: {sentiment}
"""

st.download_button("📥 Download Report", report, file_name="inflation_report.txt")

# Explanation Button
if st.button("💡 Explain Inflation"):
    st.write("Inflation is influenced by rising prices, wage growth, and consumer sentiment.")

# Real-time Clock
st.write("🕒 Time:", datetime.datetime.now())

# Footer
st.markdown("---")
st.markdown("🚀 Developed as an AI Inflation Forecasting Agent")
