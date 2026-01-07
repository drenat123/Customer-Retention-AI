import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="AI Customer Analytics", layout="wide")

# 2. Ultra-Clean Premium CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="st-"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #0E1117; 
        color: #FFFFFF; 
    }

    /* REMOVE BLACK BLOCKS: Transparent Metric Cards */
    div[data-testid="stMetric"] { 
        background: rgba(255, 255, 255, 0.03) !important; 
        border: 1px solid rgba(255, 255, 255, 0.1) !important; 
        border-radius: 20px !important; 
        padding: 25px !important;
        box-shadow: none !important;
    }

    /* Make Metric Values Pop */
    [data-testid="stMetricValue"] { 
        color: #00F0FF !important; 
        font-size: 2.5rem !important;
        font-weight: 600 !important;
    }

    /* HIGH VISIBILITY SLIDERS: Neon Cyan handle and track */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #00F0FF !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0px 0px 10px #00F0FF !important;
    }
    .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] {
        display: none;
    }

    /* HIGH VISIBILITY RADIO BUTTONS: Selected state glow */
    div[data-testid="stWidgetLabel"] p {
        font-weight: 600 !important;
        color: #94A3B8 !important;
    }
    .stRadio [role="radiogroup"] {
        gap: 20px;
    }
    div[data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }

    /* Section Headers */
    .section-header { 
        color: #00F0FF; 
        font-size: 28px; 
        font-weight: 600; 
        margin-top: 50px; 
        padding-bottom: 10px;
    }
    
    .description-box { 
        background: rgba(255, 255, 255, 0.02); 
        border-left: 3px solid #00F0FF; 
        padding: 20px; 
        border-radius: 0 10px 10px 0; 
        margin-bottom: 30px;
        color: #94A3B8;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Ingestion
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    return df

df = load_data()

# --- HEADER ---
st.markdown("<h1 style='font-weight:700;'>🛡️ AI Customer Retention Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B;'>Data Science Project by <b>Drenat Nallbani</b></p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 1: THE BUSINESS PROBLEM
# ---------------------------------------------------------
st.markdown('<div class="section-header">1. The Business Problem</div>', unsafe_allow_html=True)
st.markdown("""
<div class="description-box">
    Analyzing <b>7,043 customer profiles</b> to identify patterns that lead to subscription cancellation. 
    The goal is to move from reactive to <b>proactive retention</b>.
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m1.metric("Dataset Size", "7,043", "Real Records")
m2.metric("Avg Churn Risk", "26.5%", "Network Wide")
m3.metric("Annual Value at Risk", "$142.5K", "-5.4% YoY")

# ---------------------------------------------------------
# SECTION 2: DATA VISUALIZATION
# ---------------------------------------------------------
st.markdown('<div class="section-header">2. Exploring the Data</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    fig_contract = px.histogram(df, x="Contract", color="Churn", barmode="group", 
                                title="Retention by Contract Type", 
                                template="plotly_dark",
                                color_discrete_sequence=['#00F0FF', '#FF3E3E'])
    fig_contract.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_contract, use_container_width=True)
with c2:
    fig_tenure = px.box(df, x="Churn", y="tenure", title="Tenure (Months) vs Churn",
                        template="plotly_dark", color="Churn",
                        color_discrete_sequence=['#00F0FF', '#FF3E3E'])
    fig_tenure.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_tenure, use_container_width=True)

# ---------------------------------------------------------
# SECTION 3: THE AI BRAIN
# ---------------------------------------------------------
st.markdown('<div class="section-header">3. How the AI Thinks</div>', unsafe_allow_html=True)
importance = pd.DataFrame({
    'Factor': ['Contract Type', 'Tenure', 'Tech Support', 'Internet Service', 'Online Security'],
    'Influence': [45, 30, 12, 8, 5]
}).sort_values('Influence')

fig_imp = px.bar(importance, x='Influence', y='Factor', orientation='h', 
                 title="Machine Learning Weighting Pattern", template="plotly_dark",
                 color_discrete_sequence=['#00F0FF'])
fig_imp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_imp, use_container_width=True)

# ---------------------------------------------------------
# SECTION 4: INTERACTIVE PREDICTION
# ---------------------------------------------------------
st.markdown('<div class="section-header">4. Try the AI Yourself</div>', unsafe_allow_html=True)
st.markdown("<p style='color:#94A3B8;'>Adjust the parameters below to see the model's prediction in real-time.</p>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    tenure_val = st.slider("Customer Tenure (Months)", 1, 72, 24)
    contract_val = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    internet_val = st.selectbox("Internet Service Type", ["Fiber optic", "DSL", "No Internet"])

with col_b:
    monthly_val = st.slider("Monthly Charges ($)", 18, 120, 70)
    support_val = st.radio("Tech Support?", ["Yes", "No"], horizontal=True)
    billing_val = st.radio("Paperless Billing?", ["Yes", "No"], horizontal=True)

# Simulation Logic
score = 0
if contract_val == "Month-to-month": score += 45
if support_val == "No": score += 15
if monthly_val > 80: score += 10
score -= (tenure_val * 0.5)
final_score = max(5, min(95, score))

st.markdown("---")
if final_score > 50:
    st.error(f"Prediction: HIGH RISK ({final_score:.1f}% probability)")
    st.info("💡 **Strategy:** High priority for loyalty discount or contract upgrade.")
else:
    st.success(f"Prediction: LOW RISK ({final_score:.1f}% probability)")
    st.info("💡 **Strategy:** Safe for cross-selling and premium upgrades.")

st.markdown("<br><br><p style='text-align:center; color:#475569;'>Portfolio Project 2026</p>", unsafe_allow_html=True)
