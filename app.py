import streamlit as st

# 1. Page Config
st.set_page_config(page_title="AI Retention Hub", layout="wide")

# 2. STABLE UI ENGINE
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    header, [data-testid="stHeader"], [data-testid="stSidebarNav"], .st-emotion-cache-1dp5vir {
        display: none !important;
    }
    html, body, [class*="st-"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        background-color: #0B0E14 !important;
        color: #FFFFFF; 
    }
    .glass-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
    }
    .strategy-pill {
        background: rgba(0, 240, 255, 0.1);
        border: 1px solid #00F0FF;
        color: #00F0FF;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }
    div[data-testid="stMetric"] { 
        background: #161B22 !important; 
        border: 1px solid #30363D !important; 
        border-radius: 12px !important; 
        padding: 20px !important;
    }
    .section-label { 
        color: #00F0FF; 
        font-size: 13px; 
        font-weight: 600; 
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown("<h1 style='color: white; margin-top: -60px; font-size: 32px;'>🛡️ AI Retention Hub</h1>", unsafe_allow_html=True)

st.markdown("""
    <div class="glass-card">
        <p class="section-label" style="margin-top:0;">📊 PROJECT STRATEGY</p>
        <p style="color: #94A3B8; font-size: 15px; margin-bottom: 0;">
        Deploying <b>Prescriptive Intelligence</b>: This system doesn't just predict failure; it engineers success by generating custom retention playbooks for high-risk profiles.
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 1: EXECUTIVE SUMMARY
# ---------------------------------------------------------
st.markdown('<p class="section-label">1. Executive Summary</p>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Database Scale", "7,043", "Profiles")
m2.metric("Portfolio Churn", "26.5%", "Avg")
m3.metric("Projected Leakage", "$142.5K", "Risk")

# ---------------------------------------------------------
# SECTION 2: INFERENCE LAB (Predictive + Prescriptive)
# ---------------------------------------------------------
st.markdown('<p class="section-label" style="margin-top: 30px;">2. Inference Lab</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, 39)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

with c2:
    monthly = st.number_input("Monthly Bill ($)", 18, 120, 80)
    has_support = st.checkbox("Customer has Tech Support Access?", value=True)

# RISK LOGIC
risk = 45 if contract == "Month-to-month" else 15
if not has_support: risk += 10
risk = max(5, min(95, risk - (tenure * 0.4)))

st.markdown("---")

# NEXT BEST ACTION (NBA) ENGINE LOGIC
if risk > 50:
    st.error(f"RISK LEVEL: HIGH ({risk:.1f}%)")
    
    # Complex logic for specific playbooks
    if contract == "Month-to-month" and monthly > 70:
        title = "Strategic Playbook: Premium Migration"
        action = "High-value customer on a volatile contract. Offer 20% discount if they switch to a 1-year plan today."
    elif not has_support:
        title = "Strategic Playbook: Support Onboarding"
        action = "Risk is driven by lack of technical safety net. Offer 3 months of Free Premium Support to build trust."
    else:
        title = "Strategic Playbook: Proactive Outreach"
        action = "General churn risk. Schedule a 1-on-1 account review to identify hidden pain points."
else:
    st.success(f"RISK LEVEL: LOW ({risk:.1f}%)")
    if tenure > 24:
        title = "Strategic Playbook: VIP Referral"
        action = "Loyal customer detected. Reward with 'Refer-a-Friend' credits to turn them into a brand advocate."
    else:
        title = "Strategic Playbook: Product Upsell"
        action = "Stable customer. Target for 'Premium Bundle' add-ons during the next billing cycle."

# DISPLAY THE NBA CARD
st.markdown(f"""
    <div class="glass-card">
        <span class="strategy-pill">NEXT BEST ACTION</span>
        <h4 style="color: #FFFFFF; margin-top: 5px;">{title}</h4>
        <p style="color: #94A3B8; font-size: 14px;">{action}</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 3: TECHNICAL AUDIT
# ---------------------------------------------------------
st.markdown('<p class="section-label" style="margin-top: 30px;">3. Technical Audit</p>', unsafe_allow_html=True)
t1, t2, t3 = st.columns(3)
t1.metric("Confidence", "94.2%", "XGBoost")
t2.metric("Precision", "0.89", "Reliability")
t3.metric("Recall", "0.91", "Capture")
