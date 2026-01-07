import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 THE ONLY WAY TO FORCE COLOR (Custom HTML)
# ==========================================
def neon_metric(label, value, color="#00FFAB"):
    # Convert hex to rgba for the glow
    hex_color = color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    glow = f"rgba({r},{g},{b},0.5)"
    
    # We use a unique ID for each metric to prevent CSS bleeding
    html_code = f"""
    <div style="
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        padding: 20px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
    ">
        <span style="
            color: #94A3B8 !important; 
            font-size: 13px !important; 
            text-transform: uppercase !important; 
            letter-spacing: 1.5px !important; 
            margin-bottom: 8px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        ">{label}</span>
        <span style="
            color: {color} !important; 
            font-size: 52px !important; 
            font-weight: 700 !important; 
            text-shadow: 0 0 20px {glow} !important; 
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            line-height: 1 !important;
        ">{value}</span>
    </div>
    """
    st.write(html_code, unsafe_allow_html=True)

# 2. GLOBAL STYLES
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    [data-testid="stHeader"] { display: none !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #0B0E14 !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .main-title {
        color: #FFFFFF !important;
        font-size: 36px !important;
        font-weight: 700 !important;
        margin-bottom: 0px !important;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .subtitle {
        color: #94A3B8 !important;
        font-size: 16px !important;
        margin-bottom: 40px !important;
        opacity: 0.8;
    }

    .section-label { 
        color: #00F0FF !important; 
        font-size: 14px !important; 
        font-weight: 600 !important; 
        text-transform: uppercase !important; 
        letter-spacing: 2px !important;
        margin-top: 40px !important; 
        margin-bottom: 20px !important;
        border-left: 3px solid #00F0FF !important;
        padding-left: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🛡️ RESTORED HEADER
# ==========================================
st.markdown('<div class="main-title">🛡️ AI Retention Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Next-Gen Predictive Churn Intelligence</div>', unsafe_allow_html=True)

# 3. DATA
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url).head(10)
    df['Risk'] = [np.random.randint(15, 90) for _ in range(len(df))]
    return df

df = load_data()

# 4. QUEUE SECTION
st.markdown('<p class="section-label">1. Risk Priority Queue</p>', unsafe_allow_html=True)
st.dataframe(df[['customerID', 'tenure', 'MonthlyCharges', 'Contract', 'Risk']], use_container_width=True, hide_index=True)

# 5. RESULTS SECTION (SIMULATION)
st.markdown('<p class="section-label">2. Real-Time Impact Simulation</p>', unsafe_allow_html=True)

m1, m2 = st.columns(2)
with m1:
    neon_metric("🔵 SIMULATED RISK", "17.3%", color="#00F0FF")
with m2:
    neon_metric("🟢 REVENUE SAFEGUARDED", "+$148.42", color="#00FFAB")

# 6. MACRO SECTION
st.markdown('<p class="section-label">3. Macro Business Impact</p>', unsafe_allow_html=True)
bi1, bi2, bi3 = st.columns(3)
with bi1:
    neon_metric("🟢 ANNUAL SAVINGS", "+$37,930", color="#00FFAB")
with bi2:
    neon_metric("🔵 EFFICIENCY", "91%", color="#00F0FF")
with bi3:
    neon_metric("🟠 CONFIDENCE", "94.2%", color="#FF8C00")

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani</p>", unsafe_allow_html=True)
