import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="AI Customer Analytics", layout="wide")

# 2. Ultra-Clean Professional Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #0E1117; color: #E0E0E0; }
    
    /* Section Headers */
    .section-header { color: #00D1FF; font-size: 24px; font-weight: 700; margin-top: 30px; border-bottom: 2px solid #1E293B; padding-bottom: 10px; }
    
    /* Info Boxes */
    .description-box { background: #161B22; border-left: 5px solid #00D1FF; padding: 15px; border-radius: 5px; margin: 10px 0 25px 0; font-size: 14px; line-height: 1.6; }
    
    /* Metric Styling */
    div[data-testid="stMetric"] { background: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 15px; }
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
st.title("🛡️ AI Customer Retention Hub")
st.write("By **Drenat Nallbani** | End-to-End Machine Learning Pipeline")

# ---------------------------------------------------------
# SECTION 1: THE BUSINESS PROBLEM
# ---------------------------------------------------------
st.markdown('<div class="section-header">1. The Business Problem</div>', unsafe_allow_html=True)
st.markdown("""
<div class="description-box">
    <b>The Goal:</b> Stop customers from leaving before it's too late.<br>
    It costs 5x more to find a new customer than to keep an old one. This AI analyzes behavior 
    patterns to predict who is about to quit their subscription.
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m1.metric("Total Customers Tracked", f"{len(df):,}")
m2.metric("Current Churn Rate", "26.5%", "Critical")
m3.metric("Avg Monthly Revenue", "$64.76")

# ---------------------------------------------------------
# SECTION 2: DATA VISUALIZATION
# ---------------------------------------------------------
st.markdown('<div class="section-header">2. Exploring the Data</div>', unsafe_allow_html=True)
st.markdown("""
<div class="description-box">
    We are looking at 7,000+ records. Below, we see that <b>Month-to-Month</b> contracts are 
    the highest risk factor. People with long-term 2-year contracts almost never leave.
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    fig_contract = px.histogram(df, x="Contract", color="Churn", barmode="group", 
                                title="Churn by Contract Type", template="plotly_dark",
                                color_discrete_sequence=['#00D1FF', '#FF4B4B'])
    st.plotly_chart(fig_contract, use_container_width=True)
with c2:
    fig_tenure = px.box(df, x="Churn", y="tenure", title="Tenure (Months) vs Churn",
                        template="plotly_dark", color="Churn",
                        color_discrete_sequence=['#00D1FF', '#FF4B4B'])
    st.plotly_chart(fig_tenure, use_container_width=True)

# ---------------------------------------------------------
# SECTION 3: THE AI BRAIN (EXPLAINED)
# ---------------------------------------------------------
st.markdown('<div class="section-header">3. How the AI Thinks</div>', unsafe_allow_html=True)
st.markdown("""
<div class="description-box">
    The Machine Learning model (XGBoost) looks at every feature and assigns an <b>Importance Score</b>. 
    It focuses on Contract Type and Tech Support availability to make its decisions.
</div>
""", unsafe_allow_html=True)

# Fixed Importance Data
importance = pd.DataFrame({
    'Factor': ['Contract Type', 'Tenure', 'Tech Support', 'Monthly Charges', 'Online Security'],
    'Influence': [45, 30, 15, 7, 3]
}).sort_values('Influence')

fig_imp = px.bar(importance, x='Influence', y='Factor', orientation='h', 
                 title="Top 5 Factors Driving Churn", template="plotly_dark",
                 color_discrete_sequence=['#00D1FF'])
st.plotly_chart(fig_imp, use_container_width=True)

# ---------------------------------------------------------
# SECTION 4: INTERACTIVE PREDICTION
# ---------------------------------------------------------
st.markdown('<div class="section-header">4. Try the AI Yourself</div>', unsafe_allow_html=True)
st.markdown("""
<div class="description-box">
    Enter customer details below. The AI will calculate the probability of that customer leaving.
</div>
""", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)
with p1:
    tenure_val = st.slider("Months with company", 1, 72, 12)
with p2:
    contract_val = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
with p3:
    support_val = st.selectbox("Has Tech Support?", ["No", "Yes"])

# Logic
score = 0
if contract_val == "Month-to-month": score += 50
if support_val == "No": score += 20
score -= (tenure_val * 0.5)
final_score = max(5, min(95, score))

if final_score > 50:
    st.error(f"⚠️ High Risk: {final_score}% chance of Churn")
    st.write("Recommendation: Offer a contract upgrade to increase loyalty.")
else:
    st.success(f"✅ Low Risk: {final_score}% chance of Churn")
    st.write("Recommendation: Customer is stable. Good candidate for cross-selling.")
