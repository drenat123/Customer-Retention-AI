import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Retention Hub", page_icon="🛡️", layout="wide")

# ==========================================
# 🎨 THE GLOW ENGINE (Custom HTML Metrics)
# ==========================================
def neon_metric(label, value, color="#00FFAB"):
    """
    Replicates the exact screenshot look by bypassing st.metric.
    Colors: Green (#00FFAB), Blue (#00F0FF), Orange (#FF8C00), Red (#FF4D4D)
    """
    html_code = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 10px;">
        <p style="color: #94A3B8; font-size: 13px; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 1.5px; font-family: 'Source Sans Pro', sans-serif;">
            {label}
        </p>
        <p style="color: {color}; font-size: 52px; font-weight: 700; text-shadow: 0 0 20px {color}80; margin: 0; font-family: 'Source Sans Pro', sans-serif;">
            {value}
        </p>
    </div>
    """
    return st.markdown(html_code, unsafe_allow_html=True)

# CSS for Global Background and Sidebar
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    header, [data-testid="stHeader"] { display: none !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #0B0E14 !important; 
    }
    
    .section-label { 
        color: #00F0FF; 
        font-size: 14px; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 1.5px;
        margin-top: 30px; 
        margin-bottom: 15px; 
    }
    
    /* Style Data Editor */
    [data-testid="stElementToolbar"] { display: none; }
    .st-emotion-cache-1kyx606 { background-color: #161B22 !important; border: 1px solid #30363D !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url).head(15)
    # Adding Risk Logic
    np.random.seed(42)
    df['RiskScore'] = [np.random.randint(10, 95) for _ in range(len(df))]
    return df

base_df = load_data()

if 'active_discount' not in st.session_state:
    st.session_state.active_discount = 0
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = 0

# 3. QUEUE
st.markdown('<p class="section-label">1. Automated Risk Priority Queue</p>', unsafe_allow_html=True)
q_df = base_df[['customerID', 'tenure', 'MonthlyCharges', 'Contract', 'RiskScore']].copy()
q_df.insert(0, "Select", False)
q_df.iloc[st.session_state.selected_index, 0] = True

edited_df = st.data_editor(
    q_df, 
    hide_index=True, 
    use_container_width=True, 
    column_config={"RiskScore": st.column_config.ProgressColumn("Risk Level", format="%d%%", min_value=0, max_value=100)}
)

# 4. SIMULATION LAB
row = base_df.iloc[st.session_state.selected_index]
st.markdown(f'<p class="section-label">2. Simulation Lab: {row["customerID"]}</p>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    tenure = st.number_input("Tenure (Months)", 1, 72, value=int(row['tenure']))
with c2:
    monthly = st.number_input("Monthly Value ($)", 1, 5000, value=int(row['MonthlyCharges']))

# Offer Buttons
st.write("Apply Retention Strategy:")
b1, b2, b3, b4 = st.columns(4)
with b1: 
    if st.button("No Offer"): st.session_state.active_discount = 0
with b2: 
    if st.button("10% Discount"): st.session_state.active_discount = 10
with b3: 
    if st.button("25% Discount"): st.session_state.active_discount = 25
with b4: 
    if st.button("50% VIP"): st.session_state.active_discount = 50

# Logic for results
sim_risk = max(5, row['RiskScore'] - (st.session_state.active_discount * 0.8))
savings = (row['MonthlyCharges'] * 24) * (st.session_state.active_discount / 100)

# 5. THE SCREENSHOT REPLICA RESULTS
st.markdown("---")
m1, m2 = st.columns(2)
with m1:
    # Logic: Orange for high simulation values, Blue for lower
    risk_color = "#FF8C00" if sim_risk > 20 else "#00F0FF"
    neon_metric("🔵 SIMULATED RISK", f"{sim_risk:.1f}%", color=risk_color)
with m2:
    neon_metric("🟢 REVENUE SAFEGUARDED", f"+${savings:,.2f}", color="#00FFAB")

# 6. MACRO IMPACT
st.markdown("---")
st.markdown('<p class="section-label">3. Macro Business Impact Projection</p>', unsafe_allow_html=True)
bi1, bi2, bi3 = st.columns(3)
with bi1:
    neon_metric("🟢 ANNUAL SAVINGS", "+$37,930", color="#00FFAB")
with bi2:
    neon_metric("🔵 EFFICIENCY", "91%", color="#00F0FF")
with bi3:
    neon_metric("🟠 CONFIDENCE", "94.2%", color="#FF8C00")

st.markdown("<p style='text-align: center; color: #484F58; font-size: 12px; margin-top: 50px;'>Architecture by Drenat Nallbani</p>", unsafe_allow_html=True)
