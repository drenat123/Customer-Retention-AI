import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 THE CHATGPT-OPTIMIZED NEON ENGINE
# ==========================================
def neon_metric(label, value, color="#00FFAB"):
    # Convert hex to rgba for text-shadow (Fixes the white text issue)
    def hex_to_rgba(hex_color, alpha=0.6):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"
    
    glow = hex_to_rgba(color, 0.6)
    
    html_code = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 10px;">
        <p style="color: #94A3B8; font-size: 13px; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 1.5px; font-family: 'Plus Jakarta Sans', sans-serif;">
            {label}
        </p>
        <p style="color: {color}; font-size: 52px; font-weight: 700; text-shadow: 0 0 20px {glow}; margin: 0; font-family: 'Plus Jakarta Sans', sans-serif;">
            {value}
        </p>
    </div>
    """
    return st.markdown(html_code, unsafe_allow_html=True)

# Global Style Imports & UI Tweaks
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    header, [data-testid="stHeader"] { display: none !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #0B0E14 !important; 
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .section-label { 
        color: #00F0FF; 
        font-size: 14px; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 2px;
        margin-top: 40px; 
        margin-bottom: 20px;
        border-left: 3px solid #00F0FF;
        padding-left: 15px;
    }
    
    /* Clean up data editor */
    [data-testid="stElementToolbar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url).head(15)
    np.random.seed(42)
    df['RiskScore'] = [np.random.randint(10, 95) for _ in range(len(df))]
    return df

df = load_data()

if 'active_discount' not in st.session_state:
    st.session_state.active_discount = 0

# 3. QUEUE
st.markdown('<p class="section-label">1. Automated Risk Priority Queue</p>', unsafe_allow_html=True)
st.data_editor(
    df[['customerID', 'tenure', 'MonthlyCharges', 'Contract', 'RiskScore']], 
    hide_index=True, 
    use_container_width=True,
    column_config={"RiskScore": st.column_config.ProgressColumn("Risk Level", format="%d%%", min_value=0, max_value=100)}
)

# 4. SIMULATION LAB
st.markdown(f'<p class="section-label">2. Real-Time Retention Simulation</p>', unsafe_allow_html=True)

# Offer Buttons
st.write("Apply Retention Strategy:")
b1, b2, b3, b4 = st.columns(4)
with b1: 
    if st.button("No Offer"): st.session_state.active_discount = 0
with b2: 
    if st.button("10% Discount"): st.session_state.active_discount = 10
with b3: 
    if st.button("25% Discount"): st.session_state.active_discount = 25
with b4: 
    if st.button("50% VIP"): st.session_state.active_discount = 50

# Logic for results (Example values from your screenshot)
sim_risk = 17.3 - (st.session_state.active_discount * 0.1)
savings = 148.42 + (st.session_state.active_discount * 4.5)

# 5. THE RESULTS (The Glow Zone)
st.markdown("---")
m1, m2 = st.columns(2)
with m1:
    # Logic: Orange for simulation values, Blue for lower
    risk_color = "#FF8C00" if sim_risk > 15 else "#00F0FF"
    neon_metric("🔵 SIMULATED RISK", f"{sim_risk:.1f}%", color=risk_color)
with m2:
    neon_metric("🟢 REVENUE SAFEGUARDED", f"+${savings:,.2f}", color="#00FFAB")

# 6. MACRO IMPACT
st.markdown("---")
st.markdown('<p class="section-label">3. Macro Business Impact</p>', unsafe_allow_html=True)
bi1, bi2, bi3 = st.columns(3)
with bi1:
    neon_metric("🟢 ANNUAL SAVINGS", "+$37,930", color="#00FFAB")
with bi2:
    neon_metric("🔵 EFFICIENCY", "91%", color="#00F0FF")
with bi3:
    neon_metric("🟡 CONFIDENCE", "94.2%", color="#FFD700")

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani</p>", unsafe_allow_html=True)
