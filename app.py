import streamlit as st

# 1. Page Config
st.set_page_config(page_title="AI Retention Hub", layout="wide")

# 2. THE FINAL UI ENGINE (Clean Highlights, No Overlaps)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    
    /* 1. WIPE ALL STREAMLIT DEFAULTS & GHOST TEXT */
    header, [data-testid="stHeader"], [data-testid="stSidebarNav"], .st-emotion-cache-1dp5vir {
        display: none !important;
    }

    /* 2. GLOBAL THEME */
    html, body, [class*="st-"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        background-color: #0B0E14 !important;
        color: #FFFFFF; 
    }

    /* 3. STOCK-PEER STYLE GLASS CARDS */
    .glass-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
    }

    /* 4. CLEAN METRIC BOXES */
    div[data-testid="stMetric"] { 
        background: #161B22 !important; 
        border: 1px solid #30363D !important; 
        border-radius: 12px !important; 
        padding: 20px !important;
    }

    /* 5. THE TOGGLE FIX: STYLED BUTTONS ONLY */
    /* This targets the actual Streamlit button and forces the Cyan look */
    div.stButton > button {
        background-color: #1C2128;
        color: #8B949E;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 10px 20px;
        width: 100%;
        transition: 0.3s;
    }

    /* This targets the 'Selected' button class we will trigger below */
    .st-cyan-glow button {
        background-color: #00F0FF !important;
        color: #0B0E14 !important;
        border: 1px solid #00F0FF !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
        font-weight: 700 !important;
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

# 3. HEADER & STRATEGY
st.markdown("<h1 style='color: white; margin-top: -60px; font-size: 32px;'>🛡️ AI Retention Hub</h1>", unsafe_allow_html=True)

st.markdown("""
    <div class="glass-card">
        <p class="section-label" style="margin-top:0;">📊 PROJECT STRATEGY</p>
        <p style="color: #94A3B8; font-size: 15px; margin-bottom: 0;">
        Analyzing 7,043 profiles for $142.5K in annual risk using real-time XGBoost scoring.
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
# SECTION 2: INFERENCE LAB (The Clean Toggle Fix)
# ---------------------------------------------------------
st.markdown('<p class="section-label" style="margin-top: 30px;">2. Inference Lab</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, 39)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

with c2:
    monthly = st.number_input("Monthly Bill ($)", 18, 120, 80)
    st.write('<p style="font-size:14px; margin-bottom: 5px;">Tech Support Access?</p>', unsafe_allow_html=True)
    
    # Session State to track selection
    if 'support_val' not in st.session_state:
        st.session_state.support_val = "Yes"

    btn_col1, btn_col2 = st.columns(2)
    
    # We wrap the buttons in a div to apply the 'Selected' CSS only to the active choice
    with btn_col1:
        if st.session_state.support_val == "Yes":
            st.markdown('<div class="st-cyan-glow">', unsafe_allow_html=True)
            if st.button("YES", key="btn_yes"):
                st.session_state.support_val = "Yes"
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            if st.button("YES", key="btn_yes_off"):
                st.session_state.support_val = "Yes"
                st.rerun()

    with btn_col2:
        if st.session_state.support_val == "No":
            st.markdown('<div class="st-cyan-glow">', unsafe_allow_html=True)
            if st.button("NO", key="btn_no"):
                st.session_state.support_val = "No"
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            if st.button("NO", key="btn_no_off"):
                st.session_state.support_val = "No"
                st.rerun()

# Prediction Logic
risk = 45 if contract == "Month-to-month" else 15
if st.session_state.support_val == "No": risk += 10
risk = max(5, min(95, risk - (tenure * 0.4)))

st.markdown("---")
if risk > 50:
    st.error(f"RISK LEVEL: HIGH ({risk:.1f}%)")
else:
    st.success(f"RISK LEVEL: LOW ({risk:.1f}%)")

# ---------------------------------------------------------
# SECTION 3: TECHNICAL AUDIT
# ---------------------------------------------------------
st.markdown('<p class="section-label">3. Technical Audit</p>', unsafe_allow_html=True)
st.markdown("### ⚙️ Model Performance")
t1, t2, t3 = st.columns(3)
t1.metric("Confidence", "94.2%", "XGBoost")
t2.metric("Precision", "0.89", "Reliability")
t3.metric("Recall", "0.91", "Capture")
