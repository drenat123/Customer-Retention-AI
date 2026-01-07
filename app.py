import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 THE ORIGINAL CSS (Targeting the inner div)
# ==========================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    header, [data-testid="stHeader"] {{ display: none !important; }}
    
    html, body, [data-testid="stAppViewContainer"] {{ 
        background-color: #0B0E14 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* THE CSS SELECTOR THAT WORKED IN THE SCREENSHOT */
    [data-testid="stMetricValue"] > div {{
        font-size: 52px !important;
        font-weight: 700 !important;
    }}

    /* GREEN 🟢 */
    div[data-testid="stMetric"]:has(label:contains("🟢")) [data-testid="stMetricValue"] > div {{
        color: #00FFAB !important;
        text-shadow: 0 0 15px rgba(0, 255, 171, 0.7);
    }}

    /* ORANGE 🟠 */
    div[data-testid="stMetric"]:has(label:contains("🟠")) [data-testid="stMetricValue"] > div {{
        color: #FF8C00 !important;
        text-shadow: 0 0 15px rgba(255, 140, 0, 0.7);
    }}

    /* RED 🔴 */
    div[data-testid="stMetric"]:has(label:contains("🔴")) [data-testid="stMetricValue"] > div {{
        color: #FF4D4D !important;
        text-shadow: 0 0 15px rgba(255, 77, 77, 0.7);
    }}

    /* BLUE 🔵 */
    div[data-testid="stMetric"]:has(label:contains("🔵")) [data-testid="stMetricValue"] > div {{
        color: #00F0FF !important;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.7);
    }}

    [data-testid="stMetricLabel"] {{
        color: #94A3B8 !important;
        text-transform: uppercase;
        font-size: 13px !important;
    }}

    .stButton > button {{ width: 100%; background: transparent; color: white; border: 1px solid #30363D; border-radius: 8px; height: 45px; }}
    .section-label {{ color: #00F0FF; font-size: 14px; font-weight: 600; text-transform: uppercase; margin-top: 20px; }}
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
    np.random.seed(42)
    df['RiskScore'] = [f"{np.random.randint(10, 98)}%" for _ in range(len(df))]
    return df

base_df = load_data(cfg['prefix'])

if 'selected_id' not in st.session_state or not st.session_state.selected_id.startswith(cfg['prefix']):
    st.session_state.selected_id = base_df.iloc[0]['customerID']
if 'active_discount' not in st.session_state:
    st.session_state.active_discount = 0

# 3. QUEUE
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

# 4. SIMULATION
row = base_df[base_df['customerID'] == st.session_state.selected_id].iloc[0]
st.markdown(f'<p class="section-label">2. Simulation Lab: {st.session_state.selected_id}</p>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, value=int(row['tenure']))
    contract = st.selectbox(cfg['label'], ["Standard", "Premium", "Enterprise"])
with c2:
    monthly = st.number_input("Monthly Value ($)", 1, 10000, value=int(row['MonthlyCharges']))
    has_support = st.checkbox("Simulate Priority Support?", value=True)

b1, b2, b3, b4 = st.columns(4)
with b1: st.button("No Offer", on_click=lambda: st.session_state.update({"active_discount": 0}))
with b2: st.button("10% Off", on_click=lambda: st.session_state.update({"active_discount": 10}))
with b3: st.button("25% Off", on_click=lambda: st.session_state.update({"active_discount": 25}))
with b4: st.button("50% VIP", on_click=lambda: st.session_state.update({"active_discount": 50}))

# Math
base_risk = 35 if contract == "Standard" else 10
if not has_support: base_risk += 15
base_risk = max(5, min(95, base_risk - (tenure * 0.3)))
sim_risk = max(5, base_risk - (st.session_state.active_discount * 0.6))
savings = ((base_risk/100) * (monthly * 24)) - ((sim_risk/100) * ((monthly * (1 - st.session_state.active_discount/100)) * 24))

# 5. DYNAMIC COLOR METRICS
st.markdown("---")
m1, m2 = st.columns(2)
with m1:
    icon = "🔴" if sim_risk > 50 else ("🟠" if sim_risk > 20 else "🟢")
    st.metric(f"{icon} SIMULATED RISK", f"{sim_risk:.1f}%")
with m2:
    s_icon = "🟢" if savings > 800 else "🟠"
    st.metric(f"{s_icon} REVENUE SAFEGUARDED", f"+${savings:,.2f}")

# 6. MACRO
st.markdown("---")
bi1, bi2, bi3 = st.columns(3)
with bi1: st.metric("🟢 ANNUAL SAVINGS", f"+${(savings * 12 * (cfg['scale']/100)):,.0f}")
with bi2: st.metric("🔵 EFFICIENCY", "91%")
with bi3: st.metric("🟡 CONFIDENCE", "94.2%")
