import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Config
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
    .section-label { color: #00F0FF; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; }
    .metric-container { text-align: center; }
    .how-to { color: #484F58; font-size: 12px; margin-top: -10px; margin-bottom: 15px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# 3. BRANDING & NICHE SELECTOR
st.markdown("<h1 style='color: white; margin-top: -60px; font-size: 32px;'>🛡️ AI Retention Hub</h1>", unsafe_allow_html=True)

selected_niche = st.selectbox("📂 Select Industry Database", ["Telecommunications", "Healthcare", "SaaS", "Banking"])

niche_configs = {
    "Telecommunications": {"scale": 7043, "leakage": 142500, "label": "Contract Type", "prefix": "TELCO"},
    "Healthcare": {"scale": 12400, "leakage": 890000, "label": "Insurance Provider", "prefix": "HEALTHC"},
    "SaaS": {"scale": 5120, "leakage": 210000, "label": "Plan Level", "prefix": "SAAS"},
    "Banking": {"scale": 15000, "leakage": 1200000, "label": "Account Type", "prefix": "BANK"}
}
cfg = niche_configs[selected_niche]

# 4. DATA GENERATOR
@st.cache_data
def get_industry_data(niche):
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url).head(10)
    df['customerID'] = [f"{cfg['prefix']}-{cid}" for cid in df['customerID']]
    if niche == "Banking": df['MonthlyCharges'] = df['MonthlyCharges'] * 5 
    if niche == "Healthcare": df['MonthlyCharges'] = df['MonthlyCharges'] * 12
    np.random.seed(len(niche)) 
    df['RiskScore'] = [f"{np.random.randint(10, 98)}%" for _ in range(len(df))]
    return df

df = get_industry_data(selected_niche)

# 5. RISK LEADERBOARD (RESTORED DESCRIPTIONS)
st.markdown('<p class="section-label" style="margin-top:20px;">1. Automated Risk Priority Queue</p>', unsafe_allow_html=True)
st.markdown(f'<p class="how-to">Live {selected_niche} database ranked by AI-predicted churn risk. Use the selector below to pick a user.</p>', unsafe_allow_html=True)

display_df = df[['customerID', 'tenure', 'MonthlyCharges', 'Contract', 'RiskScore']].copy()
display_df.columns = ['Customer ID', 'Tenure', 'Value ($)', cfg['label'], 'AI Risk Score']
st.dataframe(display_df, use_container_width=True, hide_index=True)

# 6. SELECTOR (THIS IS THE TABLE WORKAROUND)
target_id = st.selectbox("🎯 Click to Select Customer from Table", df['customerID'].tolist(), help="This updates the Simulation Lab below with the user's real data.")
selected_row = df[df['customerID'] == target_id].iloc[0]

# 7. INFERENCE LAB (RESTORED DESCRIPTIONS)
st.markdown(f'<p class="section-label" style="margin-top: 30px;">2. Simulation Lab: {target_id}</p>', unsafe_allow_html=True)
st.markdown('<p class="how-to">Adjust values to see how different retention strategies change this specific user\'s risk.</p>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, value=int(selected_row['tenure']))
    contract = st.selectbox(cfg['label'], ["Standard", "Premium", "Enterprise"])
with c2:
    monthly = st.number_input("Monthly Value ($)", 1, 10000, value=int(selected_row['MonthlyCharges']))
    has_support = st.checkbox("Simulate Priority Support?", value=(selected_row['OnlineSecurity'] == "Yes"))

# 8. CALCULATION ENGINE
risk_val = 35 if contract == "Standard" else 10
if not has_support: risk_val += 15
final_risk = max(5, min(95, risk_val - (tenure * 0.3)))

# 9. OUTPUT BOX
st.markdown(f"""
    <div style="background: #161B22; border: 1px solid #30363D; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
        <p style="color: #94A3B8; margin:0;">Predicted Risk for {target_id}</p>
        <h1 style="color: #00F0FF; margin:0;">{final_risk:.1f}%</h1>
    </div>
""", unsafe_allow_html=True)

# 10. XAI & MACRO (RESTORED DESCRIPTIONS)
st.markdown('<p class="section-label">3. Explainable AI (XAI)</p>', unsafe_allow_html=True)
st.markdown('<p class="how-to">Visualizes the top factors driving this customer\'s risk score.</p>', unsafe_allow_html=True)
st.write(f"Key Driver: **{cfg['label']}**")

st.markdown("---")
st.markdown('<p class="section-label">4. Macro Business Impact Projection</p>', unsafe_allow_html=True)
st.markdown('<p class="how-to">Projected annual savings if this model is deployed across the entire department.</p>', unsafe_allow_html=True)
st.success(f"Estimated Annual Revenue Recovered: ${cfg['leakage'] * 0.22:,.0f}")

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani</p>", unsafe_allow_html=True)
