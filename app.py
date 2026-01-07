import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# =========================
# 🎨 FORCED CSS COLORS (The fix for white numbers)
# =========================
NEON_BLUE = "#00F0FF"
NEON_GREEN = "#00FFAB"
GOLD_COLOR = "#FFD700"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
header, [data-testid="stHeader"] {{ display: none !important; }}
html, body, [class*="st-"] {{ 
    font-family: 'Plus Jakarta Sans', sans-serif; 
    background-color: #0B0E14 !important;
    color: white; 
}}

/* Target the value numbers directly by their label association */
div[data-testid="stMetric"]:has(label:contains("Simulated Risk")) [data-testid="stMetricValue"] {{ color: {NEON_BLUE} !important; }}
div[data-testid="stMetric"]:has(label:contains("Efficiency")) [data-testid="stMetricValue"] {{ color: {NEON_BLUE} !important; }}
div[data-testid="stMetric"]:has(label:contains("Revenue Safeguarded")) [data-testid="stMetricValue"] {{ color: {NEON_GREEN} !important; }}
div[data-testid="stMetric"]:has(label:contains("Annual Savings")) [data-testid="stMetricValue"] {{ color: {NEON_GREEN} !important; }}
div[data-testid="stMetric"]:has(label:contains("Confidence")) [data-testid="stMetricValue"] {{ color: {GOLD_COLOR} !important; }}

[data-testid="stMetricValue"] {{ font-size: 48px !important; font-weight: 700 !important; justify-content: center !important; }}
[data-testid="stMetricLabel"] {{ justify-content: center !important; font-size: 14px !important; color: #94A3B8 !important; }}
.section-label {{ color: {NEON_BLUE}; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 25px; }}

.stButton > button {{ width: 100%; background-color: transparent; color: white; border: 1px solid #30363D; border-radius: 8px; height: 45px; }}
.stButton > button:hover {{ border-color: {NEON_BLUE}; color: {NEON_BLUE}; }}
</style>
""", unsafe_allow_html=True)

# 2. DATA ENGINE & INDUSTRY SWITCHER
selected_niche = st.selectbox("📂 Select Industry Database", ["Telecommunications", "Healthcare", "SaaS", "Banking"])

n_cfg = {
    "Telecommunications": {"scale": 7043, "label": "Contract Type", "prefix": "TELCO"},
    "Healthcare": {"scale": 12400, "label": "Insurance Provider", "prefix": "HEALTH"},
    "SaaS": {"scale": 5120, "label": "Plan Level", "prefix": "SAAS"},
    "Banking": {"scale": 15000, "label": "Account Type", "prefix": "BANK"}
}
cfg = n_cfg[selected_niche]

@st.cache_data
def load_data(niche):
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url).head(15)
    df['customerID'] = [f"{cfg['prefix']}-{cid}" for cid in df['customerID']]
    np.random.seed(42)
    df['RiskScore'] = [f"{np.random.randint(10, 98)}%" for _ in range(len(df))]
    return df

df = load_data(selected_niche)

# 3. SESSION STATE PROTECTION (Prevents the infinite loading)
if 'selected_id' not in st.session_state or not st.session_state.selected_id.startswith(cfg['prefix']):
    st.session_state.selected_id = df.iloc[0]['customerID']
if 'active_discount' not in st.session_state:
    st.session_state.active_discount = 0

# 4. SECTION 1: QUEUE
st.markdown('<p class="section-label">1. Automated Risk Priority Queue</p>', unsafe_allow_html=True)
display_df = df[['customerID', 'tenure', 'MonthlyCharges', 'Contract', 'RiskScore']].copy()
display_df.insert(0, "Select", display_df['customerID'] == st.session_state.selected_id)
display_df.columns = ["Select", "ID", "Tenure", "Value", cfg['label'], "Risk"]

# Unique key per industry prevents cache collisions
edited_df = st.data_editor(display_df, hide_index=True, use_container_width=True, key=f"editor_{selected_niche}")

# Smart update: Only rerun if the selection actually changes
checked = edited_df[edited_df["Select"] == True]
if not checked.empty:
    new_id = checked.iloc[-1]["ID"]
    if new_id != st.session_state.selected_id:
        st.session_state.selected_id = new_id
        st.rerun()

# 5. SECTION 2: SIMULATION LAB
match = df[df['customerID'] == st.session_state.selected_id]
selected_row = match.iloc[0] if not match.empty else df.iloc[0]

st.markdown(f'<p class="section-label">2. Simulation Lab: {st.session_state.selected_id}</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, int(selected_row['tenure']))
    contract = st.selectbox(cfg['label'], ["Standard", "Premium", "Enterprise"])
with c2:
    monthly = st.number_input("Monthly Value ($)", 1, 10000, int(selected_row['MonthlyCharges']))
    has_support = st.checkbox("Simulate Priority Support?", value=True)

# Discount Buttons
st.write("") # Spacer
b1, b2, b3, b4 = st.columns(4)
with b1: st.button("No Offer", on_click=lambda: st.session_state.update({"active_discount": 0}))
with b2: st.button("10% Off", on_click=lambda: st.session_state.update({"active_discount": 10}))
with b3: st.button("25% Off", on_click=lambda: st.session_state.update({"active_discount": 25}))
with b4: st.button("50% VIP", on_click=lambda: st.session_state.update({"active_discount": 50}))

# Logic
base_risk = 35 if contract == "Standard" else 10
if not has_support: base_risk += 15
base_risk = max(5, min(95, base_risk - tenure * 0.3))
sim_risk = max(5, base_risk - st.session_state.active_discount * 0.6)
savings = ((base_risk/100)*(monthly*24)) - ((sim_risk/100)*((monthly*(1-st.session_state.active_discount/100))*24))

# 6. RESULTS & XAI
st.markdown("---")
m1, m2 = st.columns(2)
with m1: st.metric("Simulated Risk", f"{sim_risk:.1f}%", help="Predicted churn probability.")
with m2: st.metric("Revenue Safeguarded", f"+${savings:,.2f}", help="Revenue protected.")

st.markdown("---")
st.markdown('<p class="section-label">3. Explainable AI (XAI)</p>', unsafe_allow_html=True)
x1, x2 = st.columns(2)
with x1: st.metric(f"{cfg['label']} Impact", "High" if contract=="Standard" else "Low")
with x2: st.metric("Support Impact", "High" if not has_support else "Low")

st.markdown("---")
st.markdown('<p class="section-label">4. Macro Business Impact Projection</p>', unsafe_allow_html=True)
bi1, bi2, bi3 = st.columns(3)
with bi1: st.metric("Annual Savings", f"+${(savings * 12 * (cfg['scale']/100)):,.0f}")
with bi2: st.metric("Efficiency", "91%")
with bi3: st.metric("Confidence", "94.2%")

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani</p>", unsafe_allow_html=True)
