import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config - Clean & Clinical
st.set_page_config(page_title="Healthcare Revenue Integrity", layout="wide")

# 2. Professional Medical Styling
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #1e293b; }
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 8px;
        padding: 10px 20px;
    }
    h1, h2, h3 { color: #0f172a; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.title("🏥 Patient Retention & Revenue Integrity")
st.markdown("##### Genpact-Inspired Healthcare Analytics Solution")

tab1, tab2, tab3 = st.tabs(["📈 Portfolio Health", "👤 Patient Lookup", "🧬 Risk Predictor"])

# --- DATASET ---
patients = pd.DataFrame({
    'Patient_Name': ['John Smith', 'Maria Garcia', 'Robert Chen', 'Sarah Miller'],
    'Last_Visit': ['2 days ago', '15 days ago', '3 months ago', '6 months ago'],
    'Wait_Time_Avg': [45, 12, 85, 90], # Minutes
    'Billing_Issues': [1, 0, 3, 2],
    'Churn_Risk': [22, 5, 78, 91]
})

# --- TAB 1: EXECUTIVE OVERVIEW ---
with tab1:
    st.markdown("### Quarterly Patient Retention Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric("PATIENT LOYALTY", "94%", "+2.1%")
    m2.metric("PROJECTED REVENUE LOSS", "$210K", "-12%", delta_color="inverse")
    m3.metric("BILLING ACCURACY", "99.2%", "High")
    
    st.markdown("---")
    fig = px.bar(patients, x='Patient_Name', y='Churn_Risk', color='Churn_Risk',
                 title="Patient Attrition Risk Score", color_continuous_scale='Bluered')
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: PATIENT DEEP-DIVE ---
with tab2:
    st.markdown("### Individual Patient Audit")
    target = st.selectbox("Search Patient Records", patients['Patient_Name'])
    p_data = patients[patients['Patient_Name'] == target].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Patient:** {target}")
        st.write(f"**Last Visit:** {p_data['Last_Visit']}")
        st.write(f"**Average Wait Time:** {p_data['Wait_Time_Avg']} mins")
    with col2:
        risk = p_data['Churn_Risk']
        st.write(f"**Attrition Probability: {risk}%**")
        st.progress(risk / 100)
        if risk > 70:
            st.error("🚨 CRITICAL: High risk of switching providers. Recommend immediate follow-up.")

# --- TAB 3: GENPACT STRATEGY LAB ---
with tab3:
    st.markdown("### Patient Experience Simulator")
    st.write("Adjust service levels to see impact on patient retention.")
    wait = st.slider("Target Wait Time (Minutes)", 5, 120, 30)
    billing = st.radio("Automated Billing Efficiency", ["Low", "Medium", "High (Genpact Standard)"])
    
    # Logic: High billing efficiency and low wait times = low risk
    predicted_risk = (wait * 0.5) - (20 if billing == "High (Genpact Standard)" else 0)
    st.info(f"Predicted Attrition Rate for this Clinic: **{max(5, predicted_risk):.1f}%**")
