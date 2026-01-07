import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="AI Retention Intelligence", layout="wide")

# 2. Header Section
st.title("🛡️ Enterprise Retention Intelligence")
st.subheader("Predictive Churn Analysis & Revenue Protection Engine")
st.markdown("---")

# 3. KPI Cards (Top Row)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Model Precision", "98.55%", "+1.2%")
with col2:
    st.metric("At-Risk Revenue", "$142.5K", "-5.4%")
with col3:
    st.metric("Retention Rate", "88%", "+2%")

# 4. Interactive Simulator (Left Column) and Visuals (Right Column)
left_col, right_col = st.columns([1, 2])

with left_col:
    st.markdown("### 🔍 Risk Simulator")
    u_drop = st.slider("Usage Decay (%)", 0, 100, 45)
    tickets = st.slider("Open Support Tickets", 0, 15, 3)
    
    # Simple probability logic for the demo
    prob = min((u_drop * 0.7 + tickets * 10) / 2, 99.9)
    
    if prob > 70:
        st.error(f"Churn Probability: {prob:.1f}% - HIGH RISK")
    else:
        st.success(f"Churn Probability: {prob:.1f}% - HEALTHY")

with right_col:
    st.markdown("### 📊 Global Churn Drivers")
    features = ['Health Score', 'Tenure', 'Support Tickets', 'Usage Drop']
    importance = [3.8, 2.4, 1.7, 0.4]
    fig = px.bar(x=importance, y=features, orientation='h', color=importance)
    fig.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig, use_container_width=True)

# 5. Footer / Contact Section
st.markdown("---")
st.markdown("### 📞 Let's Connect")
c1, c2 = st.columns(2)
with c1:
    st.write("Developed by **[Drenat Nallbani]**")
    st.write("Master ML & AI | Data Strategy")
with c2:
    st.markdown("[🔗 LinkedIn](http://linkedin.com/in/drenat-nallbani-b92229392)")
    st.markdown("[📁 GitHub Portfolio](https://github.com/drenat123)")
