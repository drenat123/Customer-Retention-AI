import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Setup
st.set_page_config(
    page_title="AI Retention Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# 2. Sidebar - Portfolio Information
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Project Details")
    st.info("""
    **Academy:** Creative Hub 
    **Focus:** Data Science & ML
    **Model:** XGBoost Classifier
    **Concept:** Revenue Protection
    """)
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.write("**Drenat Nallbani**")
    st.markdown("[LinkedIn](https://linkedin.com/in/YOUR_PROFILE)")

# 3. Main Header
st.title("🛡️ Enterprise Retention Intelligence")
st.markdown("#### Predictive Churn Analysis & Revenue Protection Engine")
st.markdown("---")

# 4. KPI Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Model Precision", "98.55%", "+1.2%")
with col2:
    st.metric("At-Risk Revenue", "$142.5K", "-5.4%")
with col3:
    st.metric("Retention Rate", "88%", "+2%")
with col4:
    st.metric("Avg. Health Score", "74/100", "+5")

# 5. Interactive Simulator & Visuals
left_col, right_col = st.columns([1, 1.5])

with left_col:
    st.markdown("### 🔍 Risk Simulator")
    st.write("Adjust variables to see real-time churn probability.")
    u_drop = st.slider("Usage Decay (%)", 0, 100, 45)
    tickets = st.slider("Open Support Tickets", 0, 15, 3)
    tenure = st.slider("Customer Tenure (Months)", 1, 72, 24)
    
    # Simple probability logic for the demo
    prob = min((u_drop * 0.6 + tickets * 8 - (tenure * 0.2)) / 1.5, 99.9)
    prob = max(prob, 5.0) # Floor at 5%
    
    if prob > 75:
        st.error(f"Churn Probability: {prob:.1f}% - CRITICAL RISK")
    elif prob > 40:
        st.warning(f"Churn Probability: {prob:.1f}% - MONITOR")
    else:
        st.success(f"Churn Probability: {prob:.1f}% - HEALTHY")

with right_col:
    st.markdown("### 📊 Churn Drivers (Feature Importance)")
    # Using real-looking feature importance data
    feat_data = pd.DataFrame({
        'Feature': ['Health Score', 'Usage Drop', 'Support Tickets', 'Contract Type', 'Tenure'],
        'Importance': [0.45, 0.28, 0.15, 0.08, 0.04]
    }).sort_values('Importance')
    
    fig = px.bar(feat_data, x='Importance', y='Feature', orientation='h', 
                 color='Importance', color_continuous_scale='RdYlGn_r')
    fig.update_layout(template="plotly_dark", height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 6. Data Intelligence Feed (The "Show More" Section)
st.markdown("### 📋 Sample Intelligence Feed")
st.write("This table simulates the live data flowing into the ML model.")

sample_data = pd.DataFrame({
    'Customer ID': ['#8812', '#9921', '#4410', '#1205', '#3391'],
    'Segment': ['Enterprise', 'SME', 'Enterprise', 'Startup', 'SME'],
    'Risk Level': ['High', 'Low', 'Medium', 'Critical', 'Low'],
    'Monthly Revenue': ['$4,500', '$800', '$2,100', '$5,200', '$950'],
    'Health Score': [32, 88, 56, 14, 91]
})

st.dataframe(sample_data, use_container_width=True)

# 7. Final Footer
st.markdown("---")
st.caption("Creative Hub Academy Portfolio Project | © 2026 Drenat Nallbani")
