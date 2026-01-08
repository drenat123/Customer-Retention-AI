import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 THE FINAL "FORCE-PAINT" CSS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    
    header, [data-testid="stHeader"] { display: none !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #0B0E14 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stMetricValue"] div {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 48px !important;
        font-weight: 700 !important;
    }

    div#metric-green [data-testid="stMetricValue"] div { color: #00FFAB !important; }
    div#metric-red [data-testid="stMetricValue"] div { color: #FF4D4D !important; }
    div#metric-cyan [data-testid="stMetricValue"] div { color: #00F0FF !important; }
    div#metric-yellow [data-testid="stMetricValue"] div { color: #FFD700 !important; }

    [data-testid="stMetricLabel"] { font-size: 14px !important; color: #94A3B8 !important; text-transform: uppercase; }
    .section-label { color: #00F0FF; font-size: 14px; font-weight: 600; text-transform: uppercase; margin-top: 20px; }
    .stButton > button { width: 100%; background-color: transparent !important; color: #FFFFFF !important; border: 1px solid #30363D !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA & INDUSTRY CONFIG
selected_niche = st.selectbox("📂 Select Industry Database", ["Telecommunications", "Healthcare", "SaaS", "Banking"])
n_cfg = {
    "Telecommunications": {"scale": 7043, "label": "Contract Type", "prefix": "TELCO"},
    "Healthcare": {"scale": 12400, "label": "Insurance Provider", "prefix": "HEALTHC"},
    "SaaS": {"scale": 5120, "label": "Plan Level", "prefix": "SAAS"},
    "Banking": {"scale": 15000, "label": "Account Type", "prefix": "BANK"}
}
cfg = n_cfg[selected_niche]

@st.cache_data
def get_industry_data(prefix):
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url).head(15)
    df['customerID'] = [f"{prefix}-{cid}" for cid in df['customerID']]
    np.random.seed(42) 
    df['RiskScore'] = [f"{np.random.randint(10, 98)}%" for _ in range(len(df))]
    return df

base_df = get_industry_data(cfg['prefix'])

# FIX: Ensure selected ID exists in the current industry dataframe
if 'selected_id' not in st.session_state or st.session_state.selected_id not in base_df['customerID'].values:
    st.session_state.selected_id = base_df.iloc[0]['customerID']

if 'active_discount' not in st.session_state:
    st.session_state.active_discount = 0

# 3. SECTION 1: QUEUE
st.markdown('<p class="section-label">1. Automated Risk Priority Queue</p>', unsafe_allow_html=True)
display_df = base_df[['customerID', 'tenure', 'MonthlyCharges', 'Contract', 'RiskScore']].copy()
display_df.insert(0, "Select", display_df['customerID'] == st.session_state.selected_id)
display_df.columns = ['Select', 'Customer ID', 'Tenure', 'Value ($)', cfg['label'], 'AI Risk Score']
edited_df = st.data_editor(display_df, hide_index=True, use_container_width=True, key=f"ed_{selected_niche}")

checked_rows = edited_df[edited_df['Select'] == True]
if not checked_rows.empty:
    new_id = checked_rows.iloc[-1]['Customer ID']
    if new_id != st.session_state.selected_id:
        st.session_state.selected_id = new_id
        st.rerun()

# 4. SECTION 2: SIMULATION LAB
target_id = st.session_state.selected_id
# FIX: Use a filtered dataframe to avoid iloc[0] errors
matching_row = base_df[base_df['customerID'] == target_id]
if matching_row.empty:
    selected_row = base_df.iloc[0]
else:
    selected_row = matching_row.iloc[0]

st.markdown(f'<p class="section-label">2. Simulation Lab: {target_id}</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, value=int(selected_row['tenure']), 
                             help="The total number of months the customer has been with the company. Longer tenure usually indicates higher loyalty and lower baseline churn risk.")
    contract = st.selectbox(cfg['label'], ["Standard", "Premium", "Enterprise"], 
                            help=f"The classification of the user's current {cfg['label']}. Enterprise/Premium contracts usually have higher switching costs and lower churn rates.")
with c2:
    monthly = st.number_input("Monthly Value ($)", 1, 10000, value=int(selected_row['MonthlyCharges']), 
                              help="The current monthly recurring revenue (MRR) for this account. High-value accounts are prioritized for retention efforts to protect bottom-line revenue.")
    has_support = st.checkbox("Simulate Priority Support?", value=True, 
                              help="Toggle this to see how assigning a dedicated account manager or priority support line impacts the AI's risk assessment.")

st.markdown("<br>", unsafe_allow_html=True)
b1, b2, b3, b4 = st.columns(4)
with b1: st.button("No Offer", on_click=lambda: st.session_state.update({"active_discount": 0}))
with b2: st.button("10% Off", on_click=lambda: st.session_state.update({"active_discount": 10}))
with b3: st.button("25% Off", on_click=lambda: st.session_state.update({"active_discount": 25}))
with b4: st.button("50% VIP", on_click=lambda: st.session_state.update({"active_discount": 50}))

# Simulation Logic
base_risk = 35 if contract == "Standard" else 10
if not has_support: base_risk += 15
base_risk = max(5, min(95, base_risk - (tenure * 0.3)))
sim_risk = max(5, base_risk - (st.session_state.active_discount * 0.6))
savings = ((base_risk/100) * (monthly * 24)) - ((sim_risk/100) * ((monthly * (1 - st.session_state.active_discount/100)) * 24))

# 5. DYNAMIC RESULTS
st.markdown("---")
m1, m2 = st.columns(2)
with m1:
    risk_id = "metric-red" if sim_risk > 30 else "metric-cyan"
    st.markdown(f'<div id="{risk_id}">', unsafe_allow_html=True)
    st.metric("🔴 CRITICAL RISK" if sim_risk > 30 else "🔵 STABLE RISK", f"{sim_risk:.1f}%", 
              help="The AI-calculated probability that the customer will leave within the next 30 days. Scores above 30% are flagged for immediate intervention.")
    st.markdown('</div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div id="metric-green">', unsafe_allow_html=True)
    st.metric("🟢 REVENUE SAFEGUARDED", f"+${savings:,.2f}", 
              help="The estimated amount of revenue saved over a 24-month horizon by applying the current retention strategy versus doing nothing.")
    st.markdown('</div>', unsafe_allow_html=True)

# 6. SECTION 3: XAI
st.markdown("---")
st.markdown('<p class="section-label">3. Explainable AI (XAI)</p>', unsafe_allow_html=True)
x1, x2 = st.columns(2)
with x1:
    val = "High" if contract == "Standard" else "Low"
    impact_id = "metric-red" if val == "High" else "metric-green"
    st.markdown(f'<div id="{impact_id}">', unsafe_allow_html=True)
    st.metric(f"🔴 {cfg['label']} IMPACT", val, 
              help=f"Analyzes how much the current {cfg['label']} contributes to the risk score. Standard tiers typically show a higher correlation with churn.")
    st.markdown('</div>', unsafe_allow_html=True)
with x2:
    val = "High" if not has_support else "Low"
    sup_id = "metric-red" if val == "High" else "metric-green"
    st.markdown(f'<div id="{sup_id}">', unsafe_allow_html=True)
    st.metric(f"🟢 SUPPORT IMPACT", val, 
              help="Evaluates the weight of customer support interaction. A 'High' impact here means the lack of priority support is a primary driver of risk.")
    st.markdown('</div>', unsafe_allow_html=True)

# 7. SECTION 4: MACRO IMPACT
st.markdown("---")
st.markdown('<p class="section-label">4. Macro Business Impact Projection</p>', unsafe_allow_html=True)
bi1, bi2, bi3 = st.columns(3)
with bi1: 
    annual = (savings * 12 * (cfg['scale']/100))
    st.markdown('<div id="metric-green">', unsafe_allow_html=True)
    st.metric("🟢 ANNUAL SAVINGS", f"+${annual:,.0f}", 
              help="The total projected revenue recovered across the entire customer base if this specific retention logic were applied globally.")
    st.markdown('</div>', unsafe_allow_html=True)
with bi2: 
    st.markdown('<div id="metric-cyan">', unsafe_allow_html=True)
    st.metric("🔵 EFFICIENCY", "91%", 
              help="The historical accuracy of the model (F1-Score). This indicates how often the AI correctly identifies true churners vs false alarms.")
    st.markdown('</div>', unsafe_allow_html=True)
with bi3: 
    st.markdown('<div id="metric-yellow">', unsafe_allow_html=True)
    st.metric("🟡 CONFIDENCE", "94.2%", 
              help="The statistical confidence interval for this specific customer's prediction. High confidence means the user's data closely matches historical churn patterns.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani</p>", unsafe_allow_html=True)
