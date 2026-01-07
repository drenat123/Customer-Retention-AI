import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 THE ORIGINAL CSS SELECTOR (The "Secret" One)
# ==========================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    header, [data-testid="stHeader"] {{ display: none !important; }}
    
    html, body, [data-testid="stAppViewContainer"] {{ 
        background-color: #0B0E14 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* THIS IS THE EXACT SELECTOR FROM THE EARLIER WORKING CODE */
    /* It targets the inner-most div that Streamlit uses for the number */
    [data-testid="stMetricValue"] > div:first-child {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* NEON GREEN 🟢 - Target: Safeguarded/Savings */
    div[data-testid="stMetric"]:has(label:contains("🟢")) [data-testid="stMetricValue"] > div:first-child {{
        color: #00FFAB !important;
        text-shadow: 0 0 20px rgba(0, 255, 171, 0.8) !important;
    }}

    /* NEON ORANGE 🟠 - Target: Warning/Risk */
    div[data-testid="stMetric"]:has(label:contains("🟠")) [data-testid="stMetricValue"] > div:first-child {{
        color: #FF8C00 !important;
        text-shadow: 0 0 20px rgba(255, 140, 0, 0.8) !important;
    }}

    /* NEON RED 🔴 - Target: Critical */
    div[data-testid="stMetric"]:has(label:contains("🔴")) [data-testid="stMetricValue"] > div:first-child {{
        color: #FF4D4D !important;
        text-shadow: 0 0 20px rgba(255, 77, 77, 0.8) !important;
    }}

    /* NEON BLUE 🔵 - Target: Efficiency/Stable */
    div[data-testid="stMetric"]:has(label:contains("🔵")) [data-testid="stMetricValue"] > div:first-child {{
        color: #00F0FF !important;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.8) !important;
    }}

    /* Target the Labels */
    [data-testid="stMetricLabel"] {{
        color: #94A3B8 !important;
        text-transform: uppercase;
        font-size: 13px !important;
        letter-spacing: 1px;
    }}

    .stButton > button {{ width: 100%; background: transparent; color: white; border: 1px solid #30363D; border-radius: 8px; height: 45px; }}
    .section-label {{ color: #00F0FF; font-size: 14px; font-weight: 600; text-transform: uppercase; margin-top: 20px; }}
    </style>
    """, unsafe_allow_html=True)

# 2. DATA 
selected_niche = st.selectbox("📂 Select Industry Database", ["Telecommunications", "Healthcare", "SaaS", "Banking"])
if 'active_discount' not in st.session_state:
    st.session_state.active_discount = 0

# Calculations (Match the screenshot values)
sim_risk = 17.3 if st.session_state.active_discount == 0 else 12.1
savings = 148.42 if st.session_state.active_discount == 0 else 210.50

# 3. RESULTS
st.markdown('<p class="section-label">2. Simulation Lab Results</p>', unsafe_allow_html=True)
m1, m2 = st.columns(2)
with m1:
    # Use ORANGE 🟠 if risk is above a certain point, BLUE 🔵 if low
    r_icon = "🟠" if sim_risk > 15 else "🔵"
    st.metric(f"{r_icon} SIMULATED RISK", f"{sim_risk:.1f}%")

with m2:
    st.metric("🟢 REVENUE SAFEGUARDED", f"+${savings:,.2f}")

# 4. MACRO
st.markdown("---")
bi1, bi2, bi3 = st.columns(3)
with bi1: st.metric("🟢 ANNUAL SAVINGS", "+$37,930")
with bi2: st.metric("🔵 EFFICIENCY", "91%")
with bi3: st.metric("🟡 CONFIDENCE", "94.2%")

# Buttons
st.markdown("---")
b1, b2 = st.columns(2)
with b1: st.button("No Offer", on_click=lambda: st.session_state.update({"active_discount": 0}))
with b2: st.button("25% Off", on_click=lambda: st.session_state.update({"active_discount": 25}))
