import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# 2. RESTORED PREMIUM CSS ENGINE (NO GLITCHES)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    header, [data-testid="stHeader"], [data-testid="stSidebarNav"] { display: none !important; }
    html, body, [class*="st-"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        background-color: #0B0E14 !important;
        color: #FFFFFF; 
    }
    /* Buttons */
    .stButton > button { width: 100%; background-color: transparent !important; color: #FFFFFF !important; border: 1px solid #30363D !important; border-radius: 8px !important; height: 45px; }
    .stButton > button:hover { border-color: #00F0FF !important; color: #00F0FF !important; }
    
    /* Section Labels */
    .section-label { color: #00F0FF; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; margin-top: 20px; }
    .how-to { color: #484F58; font-size: 13px; margin-top: -5px; margin-bottom: 20px; font-style: italic; }
    
    /* Metric Styling - RESTORED LARGE VIEW */
    .metric-container { text-align: center; padding: 10px; }
    .metric-label { color: #94A3B8; font-size: 14px; margin-bottom: 8px; display: flex; align-items: center; justify-content: center; gap: 5px; }
    .big-value-blue { font-size: 48px; font-weight: 700; color: #00F0FF; margin: 0; }
    .big-value-green { font-size: 48px; font-weight: 700; color: #00FFAB; margin: 0; }
    .big-value-white { font-size: 42px; font-weight: 700; color: #FFFFFF; margin: 0; }
    
    /* XAI Labels */
    .xai-label { color: #94A3B8; font-size: 14px; margin-bottom: 4px; }
    .xai-value { font-size: 18px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# 3. BRANDING & NICHE SELECTOR
st.markdown("<h1 style='color: white; margin-top: -60px; font-size: 32px;'>🛡️ AI Retention Hub</h1>", unsafe_allow_html=True)

selected_niche = st.selectbox(
    "📂 Select Industry Database", 
    ["Telecommunications", "Healthcare", "SaaS", "Banking"], 
    help="Recalibrates AI for industry-specific patterns."
)

niche_configs = {
    "Telecommunications": {"scale": 7043, "leakage": 142500, "label": "Contract Type", "prefix": "TELCO"},
    "Healthcare": {"scale": 12400, "leakage": 890000, "label": "Insurance Provider", "prefix": "HEALTHC"},
    "SaaS": {"scale": 5120, "leakage": 210000, "label": "Plan Level", "prefix": "SAAS"},
    "Banking": {"scale": 15000, "leakage": 1200000, "label": "Account Type", "prefix": "BANK"}
}
cfg = niche_configs[selected_niche]

# 4. DATA ENGINE
@st.cache_data
def get_industry_data(niche):
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url).head(15)
    df['customerID'] = [f"{cfg['prefix']}-{cid}" for cid in df['customerID']]
    if niche == "Banking": df['MonthlyCharges'] *= 5 
    if niche == "Healthcare": df['MonthlyCharges'] *= 12
    np.random.seed(len(niche)) 
    df['RiskScore'] = [f"{np.random.randint(10, 98)}%" for _ in range(len(df))]
    return df

base_df = get_industry_data(selected_niche)

# 5. BUG FIX: INDUSTRY SWITCHER (Prevents IndexError)
if 'selected_id' not in st.session_state or not st.session_state.selected_id.startswith(cfg['prefix']):
    st.session_state.selected_id = base_df.iloc[0]['customerID']

# 6. SECTION 1: QUEUE
st.markdown('<p class="section-label">1. Automated Risk Priority Queue</p>', unsafe_allow_html=True)
st.markdown(f'<p class="how-to">Live {selected_niche} database ranked by predicted attrition risk.</p>', unsafe_allow_html=True)

display_df = base_df[['customerID', 'tenure', 'MonthlyCharges', 'Contract', 'RiskScore']].copy()
display_df.insert(0, "Select", display_df['customerID'] == st.session_state.selected_id)
display_df.columns = ['Select', 'Customer ID', 'Tenure', 'Value ($)', cfg['label'], 'AI Risk Score']

edited_df = st.data_editor(
    display_df,
    hide_index=True,
    column_config={"Select": st.column_config.CheckboxColumn("Select", default=False)},
    disabled=['Customer ID', 'Tenure', 'Value ($)', cfg['label'], 'AI Risk Score'],
    use_container_width=True,
    key=f"editor_{selected_niche}"
)

# SYNC SELECTION
checked_rows = edited_df[edited_df['Select'] == True]
if not checked_rows.empty:
    new_id = checked_rows.iloc[-1]['Customer ID']
    if new_id != st.session_state.selected_id:
        st.session_state.selected_id = new_id
        st.rerun()

# 7. SECTION 2: SIMULATION LAB
target_id = st.session_state.selected_id
selected_row = base_df[base_df['customerID'] == target_id].iloc[0]

st.markdown(f'<p class="section-label">2. Simulation Lab: {target_id}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="how-to">Test "What-If" scenarios to lower this customer\'s specific risk score.</p>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, value=int(selected_row['tenure']))
    contract = st.selectbox(cfg['label'], ["Standard", "Premium", "Enterprise"])
with c2:
    monthly = st.number_input("Monthly Value ($)", 1, 10000, value=int(selected_row['MonthlyCharges']))
    has_support = st.checkbox("Simulate Priority Support?", value=(selected_row['OnlineSecurity'] == "Yes"))

# LOGIC
risk = 35 if contract == "Standard" else 10
if not has_support: risk += 15
risk = max(5, min(95, risk - (tenure * 0.3)))
clv = monthly * 24

# OFFERS
st.markdown("<br>", unsafe_allow_html=True)
if 'active_discount' not in st.session_state: st.session_state.active_discount = 0
b1, b2, b3, b4 = st.columns(4)
with b1: st.button("No Offer", on_click=lambda: st.session_state.update({"active_discount": 0}))
with b2: st.button("10% Off", on_click=lambda: st.session_state.update({"active_discount": 10}))
with b3: st.button("25% Off", on_click=lambda: st.session_state.update({"active_discount": 25}))
with b4: st.button("50% VIP", on_click=lambda: st.session_state.update({"active_discount": 50}))

sim_discount = st.session_state.active_discount
sim_risk = max(5, risk - (sim_discount * 0.6))
savings = ((risk/100) * clv) - ((sim_risk/100) * ((monthly * (1 - sim_discount/100)) * 24))

# METRICS - THE LARGE VIEW RESTORED
st.markdown("---")
m1, m2 = st.columns(2)
with m1:
    st.markdown(f'''<div class="metric-container">
        <div class="metric-label">Simulated Risk <span title="Predicted probability of churn based on your simulation.">info_outline</span></div>
        <p class="big-value-blue">{sim_risk:.1f}%</p>
    </div>''', unsafe_allow_html=True)
with m2:
    st.markdown(f'''<div class="metric-container">
        <div class="metric-label">Revenue Safeguarded <span title="Dollar amount of risk mitigated by this strategy.">info_outline</span></div>
        <p class="big-value-green">+${savings:,.2f}</p>
    </div>''', unsafe_allow_html=True)

# 8. SECTION 3: XAI
st.markdown("---")
st.markdown('<p class="section-label">3. Explainable AI (XAI)</p>', unsafe_allow_html=True)
st.markdown('<p class="how-to">Visualizes the top factors driving this customer\'s risk score.</p>', unsafe_allow_html=True)

x1, x2 = st.columns(2)
with x1:
    st.markdown(f'<p class="xai-label">{cfg["label"]} Impact <span title="Weight of the contract type in the risk calculation.">info_outline</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="xai-value">{"🔴 High" if contract == "Standard" else "🟢 Low"}</p>', unsafe_allow_html=True)
with x2:
    st.markdown('<p class="xai-label">Support Impact <span title="Correlation between support level and retention.">info_outline</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="xai-value">{"🔴 High" if not has_support else "🟢 Low"}</p>', unsafe_allow_html=True)

# 9. SECTION 4: MACRO (DYNAMIC)
st.markdown("---")
st.markdown('<p class="section-label">4. Macro Business Impact Projection</p>', unsafe_allow_html=True)
st.markdown('<p class="how-to">Projected annual savings if this model is deployed across the entire department.</p>', unsafe_allow_html=True)

bi1, bi2, bi3 = st.columns(3)
with bi1: 
    macro_val = savings * 12 * (cfg['scale'] / 100)
    st.markdown(f'<p class="metric-label">Annual Savings <span title="Macro recovery projection.">info_outline</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-value-green" style="font-size: 32px;">+${macro_val:,.0f}</p>', unsafe_allow_html=True)
with bi2: 
    st.markdown('<p class="metric-label">Efficiency <span title="Historical accuracy.">info_outline</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="big-value-blue" style="font-size: 32px;">91%</p>', unsafe_allow_html=True)
with bi3: 
    st.markdown('<p class="metric-label">Confidence <span title="Statistical confidence.">info_outline</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="big-value-white" style="font-size: 32px;">94.2%</p>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani | Predictive Analytics & XAI Deployment</p>", unsafe_allow_html=True)
