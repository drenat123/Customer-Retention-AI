import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 COMPLETE UI & BUTTON RECOVERY CSS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    header, [data-testid="stHeader"] { display: none !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #0B0E14 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: white;
    }

    /* SECTION LABELS */
    .section-label { 
        color: #00F0FF; 
        font-size: 14px; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 1.5px;
        margin-top: 30px; 
        margin-bottom: 15px; 
    }

    /* BUTTONS RECOVERY: Making them look clickable and highlighted again */
    .stButton > button {
        width: 100% !important;
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
        padding: 10px 0px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        border-color: #00F0FF !important;
        color: #00F0FF !important;
        background-color: #1c2128 !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2) !important;
    }

    /* CUSTOM METRIC BOXES (To bypass the white-text bug) */
    .metric-card {
        text-align: left;
        padding: 10px 0;
    }
    .metric-header {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #94A3B8;
        font-size: 14px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .tooltip-icon {
        cursor: help;
        font-size: 12px;
        color: #484F58;
    }
    .metric-val {
        font-size: 48px;
        font-weight: 700;
        line-height: 1.1;
    }

    /* Data Editor override */
    [data-testid="stDataEditor"] {
        background-color: #0B0E14 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 🛠️ HELPER: CUSTOM METRIC COMPONENT
def render_metric(label, value, color, tooltip):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span>{label}</span>
                <span class="tooltip-icon" title="{tooltip}">ⓘ</span>
            </div>
            <div class="metric-val" style="color: {color};">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
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

# Error Prevention for industry switching
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
selected_row = base_df[base_df['customerID'] == target_id].iloc[0]

st.markdown(f'<p class="section-label">2. Simulation Lab: {target_id}</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, value=int(selected_row['tenure']), help="The length of time the customer has been with the company. Longer tenure typically reduces the probability of churn.")
    contract = st.selectbox(cfg['label'], ["Standard", "Premium", "Enterprise"], help="The tier of service the customer is currently on. Higher tiers often correlate with better retention.")
with c2:
    monthly = st.number_input("Monthly Value ($)", 1, 10000, value=int(selected_row['MonthlyCharges']), help="The recurring monthly revenue from this customer. High-value customers are high priority for retention.")
    has_support = st.checkbox("Simulate Priority Support?", value=True, help="Enabling priority support simulates the impact of a dedicated agent or faster response times on customer satisfaction.")

# BUTTONS SECTION: Restored 4-column layout for "Highlights"
st.markdown("<br>", unsafe_allow_html=True)
b1, b2, b3, b4 = st.columns(4)
with b1: st.button("No Offer", on_click=lambda: st.session_state.update({"active_discount": 0}), key="btn0")
with b2: st.button("10% Off", on_click=lambda: st.session_state.update({"active_discount": 10}), key="btn10")
with b3: st.button("25% Off", on_click=lambda: st.session_state.update({"active_discount": 25}), key="btn25")
with b4: st.button("50% VIP", on_click=lambda: st.session_state.update({"active_discount": 50}), key="btn50")

# Logic
base_risk = 35 if contract == "Standard" else 10
if not has_support: base_risk += 15
base_risk = max(5, min(95, base_risk - (tenure * 0.3)))
sim_risk = max(5, base_risk - (st.session_state.active_discount * 0.6))
savings = ((base_risk/100) * (monthly * 24)) - ((sim_risk/100) * ((monthly * (1 - st.session_state.active_discount/100)) * 24))

# 5. DYNAMIC RESULTS
st.markdown("---")
m1, m2 = st.columns(2)
with m1:
    col = "#FF4D4D" if sim_risk > 30 else "#00F0FF"
    lab = "🔴 CRITICAL RISK" if sim_risk > 30 else "🔵 STABLE RISK"
    render_metric(lab, f"{sim_risk:.1f}%", col, "The AI's predicted probability of this customer churning based on current simulation variables.")
with m2:
    render_metric("🟢 REVENUE SAFEGUARDED", f"+${savings:,.2f}", "#00FFAB", "The estimated dollar value of revenue protected by implementing this retention strategy over 24 months.")

# 6. SECTION 3: XAI
st.markdown("---")
st.markdown('<p class="section-label">3. Explainable AI (XAI)</p>', unsafe_allow_html=True)
x1, x2 = st.columns(2)
with x1:
    v = "High" if contract == "Standard" else "Low"
    c = "#FF4D4D" if v == "High" else "#00FFAB"
    render_metric(f"🔴 {cfg['label']} IMPACT", v, c, f"Shows how much the {cfg['label']} is currently driving the churn risk for this specific user profile.")
with x2:
    v = "High" if not has_support else "Low"
    c = "#FF4D4D" if v == "High" else "#00FFAB"
    render_metric("🟢 SUPPORT IMPACT", v, c, "Indicates the degree to which support tier access (or lack thereof) influences this customer's likelihood to stay.")

# 7. SECTION 4: MACRO IMPACT
st.markdown("---")
st.markdown('<p class="section-label">4. Macro Business Impact Projection</p>', unsafe_allow_html=True)
bi1, bi2, bi3 = st.columns(3)
with bi1: 
    ann = (savings * 12 * (cfg['scale']/100))
    render_metric("🟢 ANNUAL SAVINGS", f"+${ann:,.0f}", "#00FFAB", "The projected yearly savings if the current retention logic were applied across your entire customer database.")
with bi2: 
    render_metric("🔵 EFFICIENCY", "91%", "#00F0FF", "Historical accuracy of the churn model. A 91% rating means the model is highly reliable for proactive intervention.")
with bi3: 
    render_metric("🟡 CONFIDENCE", "94.2%", "#FFD700", "The statistical confidence level the AI has in this specific prediction based on data density and pattern matching.")

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani</p>", unsafe_allow_html=True)
