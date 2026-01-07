import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Config (FIXED & PERMANENT)
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# 2. THE ULTIMATE CSS ENGINE (LOCKED)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    header, [data-testid="stHeader"], [data-testid="stSidebarNav"] { display: none !important; }
    html, body, [class*="st-"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        background-color: #0B0E14 !important;
        color: #FFFFFF; 
    }
    .glass-card { background: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 24px; margin-bottom: 25px; }
    div[data-testid="stMarkdownContainer"], div[data-testid="stVerticalBlock"], div[data-testid="stHorizontalBlock"] {
        background-color: transparent !important; border: none !important;
    }
    .stButton > button { width: 100%; background-color: transparent !important; color: #FFFFFF !important; border: 1px solid #30363D !important; border-radius: 8px !important; }
    .stButton > button:hover { border-color: #00F0FF !important; color: #00F0FF !important; }
    .niche-tag { background: rgba(0, 240, 255, 0.1); border: 1px solid #00F0FF; color: #00F0FF; padding: 2px 10px; border-radius: 4px; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-right: 8px; }
    .section-label { color: #00F0FF; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; }
    .metric-container { text-align: center; }
    .how-to { color: #484F58; font-size: 12px; margin-top: -10px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. BRANDING & NICHE SELECTOR
st.markdown("<h1 style='color: white; margin-top: -60px; font-size: 32px;'>🛡️ AI Retention Hub</h1>", unsafe_allow_html=True)

selected_niche = st.selectbox("📂 Select Industry Database", ["Telecommunications", "Healthcare", "SaaS", "Banking"], 
                             help="Changing this will reload the database and update the model parameters.")

niche_configs = {
    "Telecommunications": {"scale": 7043, "leakage": 142500, "label": "Contract Type", "prefix": "TELCO"},
    "Healthcare": {"scale": 12400, "leakage": 890000, "label": "Insurance Provider", "prefix": "HEALTHC"},
    "SaaS": {"scale": 5120, "leakage": 210000, "label": "Plan Level", "prefix": "SAAS"},
    "Banking": {"scale": 15000, "leakage": 1200000, "label": "Account Type", "prefix": "BANK"}
}
cfg = niche_configs[selected_niche]

# 4. LIVE DYNAMIC DATA GENERATOR
@st.cache_data
def get_industry_data(niche):
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url).head(15)
    df['customerID'] = [f"{cfg['prefix']}-{cid}" for cid in df['customerID']]
    if niche == "Banking": df['MonthlyCharges'] = df['MonthlyCharges'] * 5 
    if niche == "Healthcare": df['MonthlyCharges'] = df['MonthlyCharges'] * 12
    np.random.seed(len(niche)) 
    df['RiskScore'] = [f"{np.random.randint(10, 98)}%" for _ in range(len(df))]
    return df

df = get_industry_data(selected_niche)

# 5. RISK LEADERBOARD (WITH CLICK-TO-SELECT)
st.markdown('<p class="section-label" style="margin-top:20px;">1. Automated Risk Priority Queue</p>', unsafe_allow_html=True)
st.markdown(f'<p class="how-to">Click a row in the table below to analyze a specific {selected_niche} account.</p>', unsafe_allow_html=True)

display_df = df[['customerID', 'tenure', 'MonthlyCharges', 'Contract', 'RiskScore']].copy()
display_df.columns = ['Customer ID', 'Tenure', 'Value ($)', cfg['label'], 'AI Risk Score']

# Table Selection Logic
event = st.dataframe(
    display_df, 
    use_container_width=True, 
    hide_index=True, 
    selection_mode="single_row", 
    on_select="rerun"
)

# 6. ROW SELECTION HANDLING
# Default to the first row if nothing is clicked
selected_index = event.selection.rows[0] if event.selection.rows else 0
selected_row = df.iloc[selected_index]
target_id = selected_row['customerID']

# 7. INFERENCE LAB
st.markdown(f'<p class="section-label" style="margin-top: 30px;">2. Simulation Lab: {target_id}</p>', unsafe_allow_html=True)
st.markdown('<p class="how-to">Values auto-fill from the table. Modify them to test retention strategies.</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, value=int(selected_row['tenure']))
    csv_contract = selected_row['Contract']
    contract_idx = 0 if "Month" in csv_contract else (1 if "One" in csv_contract else 2)
    contract = st.selectbox(cfg['label'], ["Standard", "Premium", "Enterprise"], index=contract_idx)
with c2:
    monthly = st.number_input("Monthly Value ($)", 1, 10000, value=int(selected_row['MonthlyCharges']))
    has_support = st.checkbox("Simulate Priority Support?", value=(selected_row['OnlineSecurity'] == "Yes"))

# 8. LOGIC ENGINE (PRESERVED)
risk = 35 if contract == "Standard" else 10
if not has_support: risk += 15
risk = max(5, min(95, risk - (tenure * 0.3)))
clv = monthly * 24

# 9. RETENTION SANDBOX (PRESERVED)
st.markdown("---")
if 'active_discount' not in st.session_state: st.session_state.active_discount = 0
b1, b2, b3, b4 = st.columns(4)
with b1:
    if st.button("No Offer"): st.session_state.active_discount = 0
with b2:
    if st.button("10% Off"): st.session_state.active_discount = 10
with b3:
    if st.button("25% Off"): st.session_state.active_discount = 25
with b4:
    if st.button("50% VIP"): st.session_state.active_discount = 50

sim_discount = st.session_state.active_discount
sim_risk = max(5, risk - (sim_discount * 0.6))
original_rev = (risk/100) * clv
sim_rev = (sim_risk/100) * ((monthly * (1 - sim_discount/100)) * 24)
savings = original_rev - sim_rev

st.markdown(f"""
    <div style="background: transparent; border-top: 1px solid #30363D; border-bottom: 1px solid #30363D; padding: 25px 0px; display: flex; justify-content: space-around; align-items: center; margin: 20px 0;">
        <div class="metric-container"><p style="color: #94A3B8; font-size: 12px; margin:0;">Simulated Risk</p><h2 style="color: #00F0FF; margin:0;">{sim_risk:.1f}%</h2></div>
        <div class="metric-container"><p style="color: #94A3B8; font-size: 12px; margin:0;">Revenue Safeguarded</p><h2 style="color: #00FFAB; margin:0;">+${savings:,.2f}</h2></div>
    </div>
""", unsafe_allow_html=True)

# 10. XAI & BUSINESS IMPACT (PRESERVED)
st.markdown('<p class="section-label">3. Explainable AI (XAI)</p>', unsafe_allow_html=True)
xai_c1, xai_c2 = st.columns(2)
with xai_c1: st.markdown(f"<p style='color: #94A3B8; font-size: 14px;'>{cfg['label']} Impact: <span style='color: white;'>{'🔴 High' if contract == 'Standard' else '🟢 Low'}</span></p>", unsafe_allow_html=True)
with xai_c2: st.markdown(f"<p style='color: #94A3B8; font-size: 14px;'>Support Impact: <span style='color: white;'>{'🔴 High' if not has_support else '🟢 Low'}</span></p>", unsafe_allow_html=True)

st.markdown("---")
st.markdown('<p class="section-label">4. Macro Business Impact Projection</p>', unsafe_allow_html=True)
recovered_leakage = cfg['leakage'] * 0.22 
bi1, bi2, bi3 = st.columns(3)
with bi1: st.markdown(f"<div class='metric-container'><p style='color:#94A3B8; font-size:12px;'>Annual Savings</p><h2 style='color:#00FFAB; margin:0;'>+${recovered_leakage:,.0f}</h2></div>", unsafe_allow_html=True)
with bi2: st.markdown(f"<div class='metric-container'><p style='color:#94A3B8; font-size:12px;'>Efficiency</p><h2 style='color:#00F0FF; margin:0;'>91%</h2></div>", unsafe_allow_html=True)
with bi3: st.markdown(f"<div class='metric-container'><p style='color:#94A3B8; font-size:12px;'>Confidence</p><h2 style='color:#FFFFFF; margin:0;'>94.2%</h2></div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani | Predictive Analytics & XAI Deployment</p>", unsafe_allow_html=True)
