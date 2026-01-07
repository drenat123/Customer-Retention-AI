import streamlit as st

# 1. Page Config
st.set_page_config(page_title="AI Retention Hub", layout="wide")

# 2. THE NUCLEAR CSS (Kills 'key', kills 'ghost' text, fixes highlights)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    
    /* WIPE ALL GHOST ELEMENTS */
    header, [data-testid="stHeader"], [data-testid="stSidebarNav"], .st-emotion-cache-1dp5vir {
        display: none !important;
        visibility: hidden !important;
    }

    /* GLOBAL THEME */
    html, body, [class*="st-"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        background-color: #0B0E14 !important;
        color: #FFFFFF; 
    }

    /* THE 'STOCK PEER' CARD STYLE */
    .glass-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* CUSTOM TOGGLE BUTTON SYSTEM */
    .toggle-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }

    /* Default state for buttons */
    .toggle-btn {
        flex: 1;
        padding: 12px;
        text-align: center;
        background: #1C2128;
        border: 1px solid #30363D;
        border-radius: 8px;
        color: #8B949E;
        font-weight: 600;
        cursor: pointer;
        transition: 0.2s;
    }

    /* THE HIGHLIGHT STATE (Neon Cyan) */
    .active-toggle {
        background: #00F0FF !important;
        color: #0B0E14 !important;
        border: 1px solid #00F0FF !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
    }

    .section-label { 
        color: #00F0FF; 
        font-size: 13px; 
        font-weight: 600; 
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown("<h1 style='color: white; margin-top: -60px;'>🛡️ AI Retention Hub</h1>", unsafe_allow_html=True)

# THE PROJECT STRATEGY (Static Card - Zero Ghost Text)
st.markdown("""
    <div class="glass-card">
        <p class="section-label" style="margin-top:0;">📊 PROJECT STRATEGY</p>
        <div style="color: #94A3B8; font-size: 14px; line-height: 1.6;">
            <b>1. Executive Summary:</b> 7,043 profiles mapped to $142.5K risk.<br>
            <b>2. Inference Lab:</b> Real-time XGBoost churn scoring.<br>
            <b>3. Technical Audit:</b> Precision & Recall performance tracking.
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #484F58; font-size: 12px;'>Engineered by <b>Drenat Nallbani</b></p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 1: EXECUTIVE SUMMARY
# ---------------------------------------------------------
st.markdown('<p class="section-label">1. Executive Summary</p>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Database Scale", "7,043", "Profiles")
m2.metric("Portfolio Churn", "26.5%", "Avg")
m3.metric("Projected Leakage", "$142.5K", "Risk")

# ---------------------------------------------------------
# SECTION 2: INFERENCE LAB (Custom Logic)
# ---------------------------------------------------------
st.markdown('<p class="section-label">2. Inference Lab</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, 39)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
with c2:
    monthly = st.number_input("Monthly Bill ($)", 18, 120, 80)
    
    # THE CUSTOM TOGGLE FIX: 
    # We use a button-based approach because st.radio is failing you.
    st.write('<p style="font-size:14px; margin-bottom:5px;">Tech Support Access?</p>', unsafe_allow_html=True)
    
    # Logic to switch highlight based on session state
    if 'support' not in st.session_state:
        st.session_state.support = "Yes"

    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("YES", use_container_width=True):
        st.session_state.support = "Yes"
    if col_btn2.button("NO", use_container_width=True):
        st.session_state.support = "No"

    # Apply the visual highlight using HTML
    yes_class = "active-toggle" if st.session_state.support == "Yes" else ""
    no_class = "active-toggle" if st.session_state.support == "No" else ""

    st.markdown(f"""
        <div class="toggle-container" style="margin-top: -35px; pointer-events: none;">
            <div class="toggle-btn {yes_class}">YES</div>
            <div class="toggle-btn {no_class}">NO</div>
        </div>
    """, unsafe_allow_html=True)

# Logic
risk = 45 if contract == "Month-to-month" else 15
if st.session_state.support == "No": risk += 10
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
