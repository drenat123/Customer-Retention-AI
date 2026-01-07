import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE SETUP
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# 2. THE FORCE-COLOR ENGINE (The exact code that kills white text)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    /* Hide Streamlit Garbage */
    header, [data-testid="stHeader"], [data-testid="stElementToolbar"] { display: none !important; }
    
    /* Background */
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #0B0E14 !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* THE TITLE SECTION */
    .hero-title {
        color: #FFFFFF !important;
        font-size: 36px !important;
        font-weight: 700 !important;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-top: -20px;
    }
    .hero-subtitle {
        color: #94A3B8 !important;
        font-size: 16px !important;
        margin-bottom: 30px !important;
    }

    /* THE NEON NUMBERS - THE "PIERCING" SELECTOR */
    /* This targets the deepest part of the metric to force the color */
    [data-testid="stMetricValue"] > div {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
    }

    /* GREEN 🟢 */
    div[data-testid="stMetric"]:has(label:contains("🟢")) [data-testid="stMetricValue"] > div {
        color: #00FFAB !important;
        text-shadow: 0 0 20px rgba(0, 255, 171, 0.8) !important;
        -webkit-text-fill-color: #00FFAB !important;
    }

    /* BLUE 🔵 */
    div[data-testid="stMetric"]:has(label:contains("🔵")) [data-testid="stMetricValue"] > div {
        color: #00F0FF !important;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.8) !important;
        -webkit-text-fill-color: #00F0FF !important;
    }

    /* ORANGE 🟠 */
    div[data-testid="stMetric"]:has(label:contains("🟠")) [data-testid="stMetricValue"] > div {
        color: #FF8C00 !important;
        text-shadow: 0 0 20px rgba(255, 140, 0, 0.8) !important;
        -webkit-text-fill-color: #FF8C00 !important;
    }

    /* Labels */
    [data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
        text-transform: uppercase !important;
        font-size: 13px !important;
        letter-spacing: 1.5px !important;
    }

    .section-label { 
        color: #00F0FF !important; 
        font-size: 14px !important; 
        font-weight: 600 !important; 
        text-transform: uppercase !important; 
        margin-top: 40px !important; 
        border-left: 3px solid #00F0FF !important;
        padding-left: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER RESTORATION
st.markdown('<div class="hero-title">🛡️ AI Retention Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Next-Gen Predictive Churn Intelligence</div>', unsafe_allow_html=True)

# 4. DATA 
df = pd.DataFrame({
    'customerID': [f'ID-{i}' for i in range(1001, 1006)],
    'Tenure': [12, 24, 5, 48, 10],
    'Value': [75.0, 110.5, 60.2, 150.0, 85.0],
    'Risk': ['15%', '42%', '88%', '10%', '65%']
})

# 5. UI SECTIONS
st.markdown('<p class="section-label">1. Priority Risk Queue</p>', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown('<p class="section-label">2. Real-Time Simulation</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.metric("🔵 SIMULATED RISK", "17.3%")
with col2:
    st.metric("🟢 REVENUE SAFEGUARDED", "+$148.42")

st.markdown("---")
st.markdown('<p class="section-label">3. Macro Business Impact</p>', unsafe_allow_html=True)
bi1, bi2, bi3 = st.columns(3)

with bi1: st.metric("🟢 ANNUAL SAVINGS", "+$37,930")
with bi2: st.metric("🔵 EFFICIENCY", "91%")
with bi3: st.metric("🟠 CONFIDENCE", "94.2%")

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani</p>", unsafe_allow_html=True)
