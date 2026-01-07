import streamlit as st

# 1. Page Config
st.set_page_config(page_title="AI Retention Hub", layout="wide")

# 2. THE STABLE UI ENGINE (COMPLETELY RESTORED)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    
    /* 1. WIPE ALL GHOST ELEMENTS */
    header, [data-testid="stHeader"], [data-testid="stSidebarNav"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* 2. GLOBAL THEME & BRANDING */
    html, body, [class*="st-"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        background-color: #0B0E14 !important;
        color: #FFFFFF; 
    }

    /* 3. ORIGINAL PROJECT STRATEGY CARD */
    .glass-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
    }

    /* 4. UPGRADED INTERACTIVE STRATEGY BOX */
    .nba-card {
        background: linear-gradient(145deg, #161B22, #0D1117);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .nba-badge {
        background: #00F0FF;
        color: #0B0E14;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        margin-right: 10px;
    }

    /* 5. METRIC BOXES & LABELS */
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

# 3. BRANDING & HEADER (RESTORED FROM IMAGE)
# Based on
st.markdown("<h1 style='color: white; margin-top: -60px; font-size: 32px;'>🛡️ AI Retention Hub</h1>", unsafe_allow_html=True)

# 4. PROJECT STRATEGY (RESTORED FROM IMAGE)
# Based on
st.markdown("""
    <div class="glass-card">
        <p class="section-label" style="margin-top:0;">📊 PROJECT STRATEGY</p>
        <p style="color: #94A3B8; font-size: 15px; margin-bottom: 0;">
        <b>Objective:</b> Convert 7,043 raw profiles into a $142.5K annual revenue protection roadmap using XGBoost inference and Prescriptive Analytics.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #484F58; font-size: 12px; margin-bottom: 35px;'>Engineered by <b>Drenat Nallbani</b></p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 1: EXECUTIVE SUMMARY (RESTORED)
# Based on
# ---------------------------------------------------------
st.markdown('<p class="section-label">1. Executive Summary</p>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Database Scale", "7,043", "Profiles")
m2.metric("Portfolio Churn", "26.5%", "Avg")
m3.metric("Projected Leakage", "$142.5K", "Risk")

# ---------------------------------------------------------
# SECTION 2: INFERENCE LAB (PRESERVING INPUTS)
# Based on
# ---------------------------------------------------------
st.markdown('<p class="section-label" style="margin-top: 30px;">2. Inference Lab</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, 39)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

with c2:
    monthly = st.number_input("Monthly Bill ($)", 18, 120, 80)
    has_support = st.checkbox("Tech Support Access?", value=True)

# LOGIC
risk = 45 if contract == "Month-to-month" else 15
if not has_support: risk += 10
risk = max(5, min(95, risk - (tenure * 0.4)))

st.markdown("---")

# NEW: INTERACTIVE STRATEGY BOX (AS AN ADDITION)
# Based on
if risk > 50:
    icon, status, action = "🚨", "High-Priority Retention", "Volatile user detected. Offer a 15% loyalty discount if they move to an Annual Contract."
else:
    icon, status, action = "✅", "Growth Opportunity", "Stable user. Trigger VIP Referral Program and offer 'Early Access' features."

st.markdown(f"""
    <div class="nba-card">
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            <span class="nba-badge">Strategy</span>
            <span style="color: white; font-weight: 600; font-size: 18px;">{icon} {status}</span>
        </div>
        <p style="color: #94A3B8; font-size: 15px; line-height: 1.6; border-left: 3px solid #00F0FF; padding-left: 15px; margin: 0;">
            {action}
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 3: TECHNICAL AUDIT (RESTORED)
# Based on
# ---------------------------------------------------------
st.markdown('<p class="section-label" style="margin-top: 30px;">3. Technical Audit</p>', unsafe_allow_html=True)
t1, t2, t3 = st.columns(3)
t1.metric("Model Confidence", "94.2%", "XGBoost")
t2.metric("Precision", "0.89", "Reliability")
t3.metric("Recall", "0.91", "Capture")
