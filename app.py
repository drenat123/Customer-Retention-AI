import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 DYNAMIC COLOR LOGIC
# ==========================================
# This CSS targets the metric values but we will use logic below to "tag" them
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    header, [data-testid="stHeader"] { display: none !important; }
    html, body, [class*="st-"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        background-color: #0B0E14 !important;
        color: #FFFFFF; 
    }

    /* Target by Label to force specific Neon Colors */
    div[data-testid="stMetric"]:has(label:contains("SAFEGUARDED")) [data-testid="stMetricValue"],
    div[data-testid="stMetric"]:has(label:contains("SAVINGS")) [data-testid="stMetricValue"] { color: #00FFAB !important; }
    
    div[data-testid="stMetric"]:has(label:contains("CONFIDENCE")) [data-testid="stMetricValue"] { color: #FFD700 !important; }
    
    /* REACTIVE CLASSES */
    div[data-testid="stMetric"]:has(label:contains("CRITICAL")) [data-testid="stMetricValue"] { color: #FF4D4D !important; }
    div[data-testid="stMetric"]:has(label:contains("STABLE")) [data-testid="stMetricValue"] { color: #00F0FF !important; }

    [data-testid="stMetricValue"] { font-size: 48px !important; font-weight: 700 !important; justify-content: center !important; }
    [data-testid="stMetricLabel"] { justify-content: center !important; font-size: 14px !important; color: #94A3B8 !important; }
    
    .stButton > button { width: 100%; background-color: transparent !important; color: #FFFFFF !important; border: 1px solid #30363D !important; border-radius: 8px !important; height: 45px; }
    .stButton > button:hover { border-color: #00F0FF !important; color: #00F0FF !important; }
    .section-label { color: #00F0FF; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; margin-top: 20px; }
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

# Session State Sync
if 'selected_id' not in st.session_state or not st.session_state.selected_id.startswith(cfg['prefix']):
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
selected_row = base_df[base_df['customerID'] == target_id].iloc[0]

st.markdown(f'<p class="section-label">2. Simulation Lab: {target_id}</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, value=int(selected_row['tenure']), help="Adjust loyalty duration to see how tenure reduces churn risk.")
    contract = st.selectbox(cfg['label'], ["Standard", "Premium", "Enterprise"], help="Simulate tier upgrades to protect high-value accounts.")
with c2:
    monthly = st.number_input("Monthly Value ($)", 1, 10000, value=int(selected_row['MonthlyCharges']), help="Simulate revenue impact based on monthly spend.")
    has_support = st.checkbox("Simulate Priority Support?", value=True, help="Toggle the impact of dedicated agent support.")

# Buttons
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
    status_label = "🔴 CRITICAL RISK" if sim_risk > 30 else "🔵 STABLE RISK"
    st.metric(status_label, f"{sim_risk:.1f}%", help="The AI's predicted churn probability for this scenario.")
with m2:
    st.metric("🟢 REVENUE SAFEGUARDED", f"+${savings:,.2f}", help="Total dollar amount protected from loss.")

# 6. SECTION 3: XAI (EMOJI REACTIVITY UPDATED)
st.markdown("---")
st.markdown('<p class="section-label">3. Explainable AI (XAI)</p>', unsafe_allow_html=True)
x1, x2 = st.columns(2)
with x1:
    # REACTIVE: Red if Standard (High risk), Green if others
    impact_emoji = "🔴" if contract == "Standard" else "🟢"
    st.metric(f"{impact_emoji} {cfg['label']} IMPACT", "High" if contract == "Standard" else "Low")
with x2:
    # REACTIVE: Red if no support (High risk), Green if supported
    sup_emoji = "🔴" if not has_support else "🟢"
    st.metric(f"{sup_emoji} SUPPORT IMPACT", "High" if not has_support else "Low")

# 7. SECTION 4: MACRO IMPACT (EMOJI REACTIVITY UPDATED)
st.markdown("---")
st.markdown('<p class="section-label">4. Macro Business Impact Projection</p>', unsafe_allow_html=True)
bi1, bi2, bi3 = st.columns(3)
with bi1: 
    # REACTIVE: Red if negative/low, Green if positive
    savings_emoji = "🟢" if savings > 0 else "🔴"
    st.metric(f"{savings_emoji} ANNUAL SAVINGS", f"+${(savings * 12 * (cfg['scale']/100)):,.0f}")
with bi2: 
    st.metric("🔵 EFFICIENCY", "91%")
with bi3: 
    # REACTIVE: Red if risk too high, Yellow if stable
    conf_emoji = "🔴" if sim_risk > 60 else "🟡"
    st.metric(f"{conf_emoji} CONFIDENCE", "94.2%")

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani</p>", unsafe_allow_html=True)
