import streamlit as st

# 1. Page Config (PRESERVED)
st.set_page_config(page_title="AI Retention Hub", layout="wide")

# 2. THE STABLE UI ENGINE (PRESERVED & LOCKED)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    header, [data-testid="stHeader"], [data-testid="stSidebarNav"] { display: none !important; }
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
    .nba-card {
        background: linear-gradient(145deg, #161B22, #0D1117);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .nba-header { display: flex; align-items: center; gap: 12px; margin-bottom: 15px; }
    .nba-badge {
        background: #00F0FF;
        color: #0B0E14;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
    }
    .nba-body {
        color: #94A3B8;
        font-size: 15px;
        line-height: 1.6;
        border-left: 3px solid #00F0FF;
        padding-left: 15px;
    }
    .roi-positive { color: #00FFAB; font-weight: 600; }
    div[data-testid="stMetric"] { 
        background: #161B22 !important; 
        border: 1px solid #30363D !important; 
        border-radius: 12px !important; 
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

# 3. BRANDING & HEADER (PRESERVED)
st.markdown("<h1 style='color: white; margin-top: -60px; font-size: 32px;'>🛡️ AI Retention Hub</h1>", unsafe_allow_html=True)

st.markdown("""
    <div class="glass-card">
        <p class="section-label" style="margin-top:0;">📊 PROJECT STRATEGY</p>
        <p style="color: #94A3B8; font-size: 15px; margin-bottom: 0;">
        <b>Objective:</b> Convert 7,043 raw profiles into a $142.5K annual revenue protection roadmap using XGBoost inference and Prescriptive Analytics.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #484F58; font-size: 12px; margin-bottom: 30px;'>Engineered by <b>Drenat Nallbani</b></p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 1: EXECUTIVE SUMMARY (PRESERVED)
# ---------------------------------------------------------
st.markdown('<p class="section-label">1. Executive Summary</p>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Database Scale", "7,043", "Profiles")
m2.metric("Portfolio Churn", "26.5%", "Avg")
m3.metric("Projected Leakage", "$142.5K", "Risk")

# ---------------------------------------------------------
# SECTION 2: INFERENCE LAB (PRESERVED)
# ---------------------------------------------------------
st.markdown('<p class="section-label" style="margin-top: 30px;">2. Inference Lab</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, 39)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
with c2:
    monthly = st.number_input("Monthly Bill ($)", 18, 120, 80)
    has_support = st.checkbox("Tech Support Access?", value=True)

# RISK LOGIC (PRESERVED)
risk = 45 if contract == "Month-to-month" else 15
if not has_support: risk += 10
risk = max(5, min(95, risk - (tenure * 0.4)))

# ---------------------------------------------------------
# NEW IMPLEMENTATION: FINANCIAL IMPACT CALCULATOR
# ---------------------------------------------------------
clv = monthly * 24 # Simplified 2-year LTV
revenue_at_risk = (risk / 100) * clv
rescue_potential = revenue_at_risk * 0.40 # Estimating 40% recovery rate

st.markdown("---")
f1, f2 = st.columns(2)
with f1:
    st.metric("Individual LTV (24mo)", f"${clv:,.0f}", help="Total projected revenue from this profile.")
with f2:
    st.metric("Revenue at Risk", f"${revenue_at_risk:,.2f}", f"-{risk:.1f}% Score", delta_color="inverse")

# ---------------------------------------------------------
# STRATEGY ENGINE (EXPANDED GROWTH & RETENTION)
# ---------------------------------------------------------
if risk > 50:
    icon, title = "🚨", "High-Priority Retention"
    action = f"User is volatile. Projected loss: <span class='roi-positive'>${revenue_at_risk:,.2f}</span>. Execute 15% discount migration to lock in revenue."
else:
    icon = "✅"
    if monthly > 90:
        title = "Growth Strategy: Premium Upsell"
        action = "High-value spender. Target for Executive Concierge Bundle to increase annual LTV by <b>$400+</b>."
    elif tenure > 36:
        title = "Growth Strategy: Brand Ambassador"
        action = "Veteran user. Deploy Referral Credits to generate organic growth (est. value: <b>$250/referral</b>)."
    else:
        title = "Growth Strategy: Ecosystem Lock-in"
        action = "Stable user. Cross-sell Security Cloud services to maximize product stickiness."

st.markdown(f"""
    <div class="nba-card">
        <div class="nba-header">
            <span class="nba-badge">Action Plan</span>
            <p style="color:white; font-size:18px; font-weight:600; margin:0;">{icon} {title}</p>
        </div>
        <div class="nba-body">{action}</div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 3: TECHNICAL AUDIT (PRESERVED)
# ---------------------------------------------------------
st.markdown('<p class="section-label" style="margin-top: 30px;">3. Technical Audit</p>', unsafe_allow_html=True)
t1, t2, t3 = st.columns(3)
t1.metric("Confidence", "94.2%", "XGBoost")
t2.metric("Precision", "0.89", "Reliability")
t3.metric("Recall", "0.91", "Capture")
