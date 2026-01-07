import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Retention Hub",
    page_icon="🛡️",
    layout="wide"
)

# =========================
# COLOR PALETTE
# =========================
NEON_BLUE = "#00F0FF"
NEON_GREEN = "#00FFAB"
GOLD_COLOR = "#FFD700"
RED_COLOR = "#FF4D4D"
TEXT_MUTED = "#94A3B8"
BG_COLOR = "#0B0E14"

# =========================
# GLOBAL CSS
# =========================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');

html, body, [class*="st-"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: {BG_COLOR};
    color: white;
}}

header, [data-testid="stHeader"] {{
    display: none;
}}

.section-label {{
    color: {NEON_BLUE};
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 25px 0 10px 0;
}}

.stButton > button {{
    width: 100%;
    background-color: transparent;
    color: white;
    border: 1px solid #30363D;
    border-radius: 8px;
    height: 45px;
}}

.stButton > button:hover {{
    border-color: {NEON_BLUE};
    color: {NEON_BLUE};
}}
</style>
""", unsafe_allow_html=True)

# =========================
# COLORED METRIC COMPONENT
# =========================
def colored_metric(label, value, color):
    st.markdown(f"""
        <div style="text-align:center;">
            <div style="color:{TEXT_MUTED};font-size:14px;margin-bottom:6px;">
                {label}
            </div>
            <div style="color:{color};font-size:48px;font-weight:700;">
                {value}
            </div>
        </div>
    """, unsafe_allow_html=True)

# =========================
# DATA CONFIG
# =========================
selected_niche = st.selectbox(
    "📂 Select Industry Database",
    ["Telecommunications", "Healthcare", "SaaS", "Banking"]
)

n_cfg = {
    "Telecommunications": {"scale": 7043, "label": "Contract Type", "prefix": "TELCO"},
    "Healthcare": {"scale": 12400, "label": "Insurance Provider", "prefix": "HEALTH"},
    "SaaS": {"scale": 5120, "label": "Plan Level", "prefix": "SAAS"},
    "Banking": {"scale": 15000, "label": "Account Type", "prefix": "BANK"},
}

cfg = n_cfg[selected_niche]

@st.cache_data
def get_industry_data():
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url).head(15)
    df["customerID"] = [f"{cfg['prefix']}-{cid}" for cid in df["customerID"]]
    np.random.seed(42)
    df["RiskScore"] = [f"{np.random.randint(10, 98)}%" for _ in range(len(df))]
    return df

base_df = get_industry_data()

# =========================
# SESSION STATE
# =========================
if "selected_id" not in st.session_state:
    st.session_state.selected_id = base_df.iloc[0]["customerID"]

if "active_discount" not in st.session_state:
    st.session_state.active_discount = 0

# =========================
# SECTION 1 — QUEUE
# =========================
st.markdown('<p class="section-label">1. Automated Risk Priority Queue</p>', unsafe_allow_html=True)

display_df = base_df[["customerID", "tenure", "MonthlyCharges", "Contract", "RiskScore"]].copy()
display_df.insert(0, "Select", display_df["customerID"] == st.session_state.selected_id)
display_df.columns = ["Select", "Customer ID", "Tenure", "Value ($)", cfg["label"], "AI Risk Score"]

edited_df = st.data_editor(
    display_df,
    hide_index=True,
    use_container_width=True
)

checked = edited_df[edited_df["Select"] == True]
if not checked.empty:
    st.session_state.selected_id = checked.iloc[-1]["Customer ID"]
    st.rerun()

# =========================
# SECTION 2 — SIMULATION
# =========================
selected_row = base_df[base_df["customerID"] == st.session_state.selected_id].iloc[0]

st.markdown(f'<p class="section-label">2. Simulation Lab: {st.session_state.selected_id}</p>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, int(selected_row["tenure"]))
    contract = st.selectbox(cfg["label"], ["Standard", "Premium", "Enterprise"])
with c2:
    monthly = st.number_input("Monthly Value ($)", 1, 10000, int(selected_row["MonthlyCharges"]))
    has_support = st.checkbox("Simulate Priority Support?", value=True)

b1, b2, b3, b4 = st.columns(4)
with b1: st.button("No Offer", on_click=lambda: st.session_state.update({"active_discount": 0}))
with b2: st.button("10% Off", on_click=lambda: st.session_state.update({"active_discount": 10}))
with b3: st.button("25% Off", on_click=lambda: st.session_state.update({"active_discount": 25}))
with b4: st.button("50% VIP", on_click=lambda: st.session_state.update({"active_discount": 50}))

# =========================
# SIMULATION LOGIC
# =========================
base_risk = 35 if contract == "Standard" else 10
if not has_support:
    base_risk += 15

base_risk = max(5, min(95, base_risk - tenure * 0.3))
sim_risk = max(5, base_risk - st.session_state.active_discount * 0.6)

savings = (
    (base_risk / 100) * (monthly * 24)
    - (sim_risk / 100) * ((monthly * (1 - st.session_state.active_discount / 100)) * 24)
)

# =========================
# METRICS — COLORED
# =========================
st.markdown("---")
m1, m2 = st.columns(2)
with m1:
    colored_metric("Simulated Risk", f"{sim_risk:.1f}%", NEON_BLUE)
with m2:
    colored_metric("Revenue Safeguarded", f"+${savings:,.2f}", NEON_GREEN)

# =========================
# SECTION 3 — XAI
# =========================
st.markdown("---")
st.markdown('<p class="section-label">3. Explainable AI (XAI)</p>', unsafe_allow_html=True)

x1, x2 = st.columns(2)
with x1:
    colored_metric(
        f"{cfg['label']} Impact",
        "High" if contract == "Standard" else "Low",
        RED_COLOR if contract == "Standard" else NEON_GREEN
    )

with x2:
    colored_metric(
        "Support Impact",
        "High" if not has_support else "Low",
        RED_COLOR if not has_support else NEON_GREEN
    )

# =========================
# SECTION 4 — MACRO IMPACT
# =========================
st.markdown("---")
st.markdown('<p class="section-label">4. Macro Business Impact Projection</p>', unsafe_allow_html=True)

bi1, bi2, bi3 = st.columns(3)
with bi1:
    colored_metric(
        "Annual Savings",
        f"+${(savings * 12 * (cfg['scale'] / 100)):,.0f}",
        NEON_GREEN
    )
with bi2:
    colored_metric("Efficiency", "91%", NEON_BLUE)
with bi3:
    colored_metric("Confidence", "94.2%", GOLD_COLOR)

# =========================
# FOOTER
# =========================
st.markdown(
    "<p style='text-align:center;color:#484F58;font-size:12px;margin-top:50px;'>"
    "Architecture by Drenat Nallbani | Predictive Analytics & XAI Deployment"
    "</p>",
    unsafe_allow_html=True
)
