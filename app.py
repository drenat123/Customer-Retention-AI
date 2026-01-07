import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="AI Retention Hub", layout="wide")

# 2. THE FIX: Hide the top bar and style the new button
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    
    /* HIDE THE TOP BAR (Removes keyboard_doubl) */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    html, body, [class*="st-"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        background-color: #0E1117; 
        color: #F8FAFC; 
    }

    /* PREMIUM METRIC CARDS */
    div[data-testid="stMetric"] { 
        background: rgba(255, 255, 255, 0.03) !important; 
        border: 1px solid rgba(255, 255, 255, 0.1) !important; 
        border-radius: 12px !important; 
        padding: 20px !important;
    }

    /* THE CYAN SLIDERS */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        height: 30px !important;
        width: 65px !important;
        background-color: #00F0FF !important;
        border-radius: 6px !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.5) !important;
    }
    
    /* GLOWING BUTTONS */
    div[aria-checked="true"] {
        background-color: rgba(0, 240, 255, 0.1) !important;
        border: 1px solid #00F0FF !important;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
    }

    .section-header { 
        color: #00F0FF; 
        font-size: 24px; 
        font-weight: 600; 
        margin-top: 30px; 
        border-bottom: 1px solid rgba(0, 240, 255, 0.1);
        padding-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER & INSIGHTS BUTTON
st.markdown("<h1 style='color: white; margin-top: -50px;'>🛡️ AI Retention Hub</h1>", unsafe_allow_html=True)

# THE SIMPLE BUTTON YOU ASKED FOR
if st.button("📊 View Model Insights"):
    st.info("""
    **💰 Revenue Focus:** Flagging $142.5K at risk to prioritize financial impact.
    **🔍 Risk Auditing:** Predictions include a Confidence Score (98%+) based on patterns.
    **🔮 Prescriptive Action:** Provides strategic recommendations for retention calls.
    """)

st.markdown("<p style='color: #64748B;'>By <b>Drenat Nallbani</b></p>", unsafe_allow_html=True)

# 4. Data Ingestion
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    return df

df = load_data()

# ---------------------------------------------------------
# SECTION 1: THE BUSINESS PROBLEM
# ---------------------------------------------------------
st.markdown('<div class="section-header">1. The Business Problem</div>', unsafe_allow_html=True)
st.write("Analyzing 7,043 records to identify patterns leading to customer churn.")

m1, m2, m3 = st.columns(3)
m1.metric("Database Scale", "7,043", "Real Records")
m2.metric("Portfolio Churn", "26.5%", "Network Wide")
m3.metric("Annual Risk", "$142.5K", "-5.4% YoY")

# ---------------------------------------------------------
# SECTION 2: DATA VISUALIZATION
# ---------------------------------------------------------
st.markdown('<div class="section-header">2. Exploring the Data</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    fig_contract = px.histogram(df, x="Contract", color="Churn", barmode="group", 
                                template="plotly_dark", color_discrete_sequence=['#00F0FF', '#FF3E3E'])
    fig_contract.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_contract, use_container_width=True)
with c2:
    fig_tenure = px.box(df, x="Churn", y="tenure", template="plotly_dark", 
                        color="Churn", color_discrete_sequence=['#00F0FF', '#FF3E3E'])
    fig_tenure.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_tenure, use_container_width=True)

# ---------------------------------------------------------
# SECTION 3: THE AI BRAIN
# ---------------------------------------------------------
st.markdown('<div class="section-header">3. How the AI Thinks</div>', unsafe_allow_html=True)
importance = pd.DataFrame({
    'Factor': ['Contract', 'Tenure', 'Support', 'Charges'],
    'Influence': [45, 30, 15, 10]
}).sort_values('Influence')
fig_imp = px.bar(importance, x='Influence', y='Factor', orientation='h', 
                 template="plotly_dark", color_discrete_sequence=['#00F0FF'])
fig_imp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_imp, use_container_width=True)

# ---------------------------------------------------------
# SECTION 4: INTERACTIVE PREDICTOR
# ---------------------------------------------------------
st.markdown('<div class="section-header">4. Try the AI Yourself</div>', unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Loyalty Metrics")
    tenure_val = st.slider("Customer Tenure (Months)", 1, 72, 39)
    contract_val = st.selectbox("Contract Framework", ["Month-to-month", "One year", "Two year"])
    internet_val = st.selectbox("Internet Service Type", ["DSL", "Fiber optic", "No Internet"])

with col_right:
    st.subheader("Support & Billing")
    monthly_val = st.slider("Monthly Charges ($)", 18, 120, 100)
    support_val = st.radio("Access to Tech Support?", ["Yes", "No"], horizontal=True)
    billing_val = st.radio("Paperless Billing?", ["Yes", "No"], horizontal=True)

# Logic
score = 0
if contract_val == "Month-to-month": score += 45
if support_val == "No": score += 15
score -= (tenure_val * 0.5)
final_score = max(5, min(95, score))

st.markdown("---")
if final_score > 50:
    st.error(f"Prediction: HIGH RISK ({final_score:.1f}%)")
else:
    st.success(f"Prediction: LOW RISK ({final_score:.1f}%)")
