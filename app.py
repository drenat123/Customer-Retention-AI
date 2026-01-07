import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 THE "SCREENSHOT" HTML GENERATOR
# ==========================================
def custom_metric(label, value, color_type="green", help_text=""):
    # Define colors based on your screenshot
    colors = {
        "green": "#00FFAB",
        "orange": "#FF8C00",
        "red": "#FF4D4D",
        "blue": "#00F0FF",
        "gold": "#FFD700"
    }
    selected_color = colors.get(color_type, "#FFFFFF")
    
    # This raw HTML mimics the look of your 231930.png screenshot exactly
    html_code = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 10px;">
        <p style="color: #94A3B8; font-size: 13px; text-transform: uppercase; margin-bottom: -10px; letter-spacing: 1px;">
            {label}
        </p>
        <p style="color: {selected_color}; font-size: 52px; font-weight: 700; text-shadow: 0 0 20px {selected_color}66; margin: 0;">
            {value}
        </p>
    </div>
    """
    return st.markdown(html_code, unsafe_allow_html=True)

# CSS for the rest of the app
st.markdown("""
    <style>
    header, [data-testid="stHeader"] { display: none !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #0B0E14 !important; }
    .section-label { color: #00F0FF; font-size: 14px; font-weight: 600; text-transform: uppercase; margin-top: 30px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA
selected_niche = st.selectbox("📂 Select Industry Database", ["Telecommunications", "Healthcare", "SaaS", "Banking"])
n_cfg = {
    "Telecommunications": {"scale": 7043, "label": "Contract Type", "prefix": "TELCO"},
    "Healthcare": {"scale": 12400, "label": "Insurance Provider", "prefix": "HEALTHC"},
    "SaaS": {"scale": 5120, "label": "Plan Level", "prefix": "SAAS"},
    "Banking": {"scale": 15000, "label": "Account Type", "prefix": "BANK"}
}
cfg = n_cfg[selected_niche]

@st.cache_data
def load_data(prefix):
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url).head(15)
    df['customerID'] = [f"{prefix}-{cid}" for cid in df['customerID']]
    return df

base_df = load_data(cfg['prefix'])

if 'selected_id' not in st.session_state or not st.session_state.selected_id.startswith(cfg['prefix']):
    st.session_state.selected_id = base_df.iloc[0]['customerID']
if 'active_discount' not in st.session_state:
    st.session_state.active_discount = 0

# 3. QUEUE
st.markdown('<p class="section-label">1. Automated Risk Priority Queue</p>', unsafe_allow_html=True)
q_df = base_df[['customerID', 'tenure', 'MonthlyCharges', 'Contract']].copy()
q_df.insert(0, "Select", q_df['customerID'] == st.session_state.selected_id)
edited_df = st.data_editor(q_df, hide_index=True, use_container_width=True)

# 4. SIMULATION MATH
row = base_df[base_df['customerID'] == st.session_state.selected_id].iloc[0]
st.markdown(f'<p class="section-label">2. Simulation Lab: {st.session_state.selected_id}</p>', unsafe_allow_html=True)

# Offer Buttons
b1, b2, b3, b4 = st.columns(4)
with b1: st.button("No Offer", on_click=lambda: st.session_state.update({"active_discount": 0}))
with b2: st.button("10% Off", on_click=lambda: st.session_state.update({"active_discount": 10}))
with b3: st.button("25% Off", on_click=lambda: st.session_state.update({"active_discount": 25}))
with b4: st.button("50% VIP", on_click=lambda: st.session_state.update({"active_discount": 50}))

# Calculations
sim_risk = 17.3 + (st.session_state.active_discount * -0.2) # Sample logic
savings = 148.42 + (st.session_state.active_discount * 5)

# 5. THE RESULTS (Using the Custom Function)
st.markdown("---")
m1, m2 = st.columns(2)
with m1:
    # Logic for color
    c = "green" if sim_risk < 20 else "orange"
    custom_metric("🔵 SIMULATED RISK", f"{sim_risk:.1f}%", color_type=c)
with m2:
    custom_metric("🟢 REVENUE SAFEGUARDED", f"+${savings:,.2f}", color_type="green")

# 6. MACRO
st.markdown("---")
bi1, bi2, bi3 = st.columns(3)
with bi1: custom_metric("🟢 ANNUAL SAVINGS", "+$37,930", color_type="green")
with bi2: custom_metric("🔵 EFFICIENCY", "91%", color_type="blue")
with bi3: custom_metric("🟡 CONFIDENCE", "94.2%", color_type="gold")
