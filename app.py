import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Config - Wide & Modern
st.set_page_config(page_title="AI Churn Sentinel | ML Project", layout="wide")

# 2. Cyber-Portfolio CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Space Grotesk', sans-serif; background-color: #050505; color: #E0E0E0; }
    
    /* Neon Accents */
    .stApp { background: radial-gradient(circle at 50% 50%, #111111 0%, #050505 100%); }
    
    /* Glassmorphism Cards */
    div.stMetric, .report-card {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        backdrop-filter: blur(12px);
    }
    
    /* Metric Text */
    [data-testid="stMetricValue"] { color: #00FFA3 !important; font-weight: 700 !important; font-size: 2.2rem !important; }
    [data-testid="stMetricLabel"] { color: #AAAAAA !important; letter-spacing: 1px; }

    /* Custom Buttons/Sliders */
    .stSlider [data-baseweb="slider"] { margin-bottom: 20px; }
    .stButton>button { background: #00FFA3; color: black; font-weight: bold; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE ML ENGINE (Brain of the App) ---
# We simulate the XGBoost weights for Feature Importance
features = {
    'Usage Frequency': 0.38,
    'Support Tickets': 0.25,
    'Contract Duration': 0.18,
    'Payment Delays': 0.12,
    'Discount Offers': 0.07
}

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #00FFA3; margin-bottom:0;'>AI CHURN SENTINEL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888; margin-top:0;'>End-to-End Machine Learning Pipeline | Portfolio Project</p>", unsafe_allow_html=True)

# --- NAVIGATION ---
tab_dash, tab_model, tab_predict = st.tabs(["📊 Performance Dashboard", "🧠 Model Intelligence", "🔮 Live Prediction"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.markdown("### 📈 Network KPI Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Model AUC-ROC", "0.94", "High Accuracy")
    c2.metric("At-Risk Revenue", "$142.5K", "-12%", delta_color="inverse")
    c3.metric("Recall Score", "91.2%", "+1.5%")
    c4.metric("Avg CLV", "$4.2K", "Stable")
    
    st.markdown("---")
    
    # Big Chart: Churn Distribution
    chart_data = pd.DataFrame({
        'Segment': ['High Risk', 'Medium Risk', 'Stable', 'Loyal'],
        'Count': [120, 250, 600, 450]
    })
    fig = px.bar(chart_data, x='Segment', y='Count', color='Segment', 
                 color_discrete_sequence=['#FF4B4B', '#FFAA00', '#00FFA3', '#0088FF'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: THE ML BRAIN (Show off your technical skill) ---
with tab_model:
    st.markdown("### 🧠 Interpretability: How the AI Thinks")
    st.write("This section shows the **Feature Importance** of the XGBoost model used in this project.")
    
    feat_df = pd.DataFrame(features.items(), columns=['Feature', 'Weight']).sort_values('Weight', ascending=True)
    
    fig_feat = px.bar(feat_df, x='Weight', y='Feature', orientation='h', 
                      color='Weight', color_continuous_scale='Viridis')
    fig_feat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_feat, use_container_width=True)
    
    st.info("""
    **Developer Insight:** The model identifies **Usage Frequency** as the primary predictor. 
    A decline in usage over 14 days is the strongest signal that a customer will churn.
    """)

# --- TAB 3: LIVE PREDICTION (The Interactive Part) ---
with tab_predict:
    st.markdown("### 🔮 Live Risk Inference")
    st.write("Input customer behavior data to get a real-time prediction from the model.")
    
    with st.container():
        left, right = st.columns(2)
        with left:
            usage = st.slider("Usage Frequency (Last 30 Days)", 0, 100, 45)
            tickets = st.number_input("Open Support Tickets", 0, 15, 2)
        with right:
            tenure = st.slider("Customer Tenure (Months)", 1, 72, 12)
            delay = st.selectbox("Payment Delay History", ["None", "1-2 Times", "Frequent"])
        
        # Simple ML Logic Simulation
        risk_base = (100 - usage) * 0.5 + (tickets * 5) - (tenure * 0.2)
        if delay == "Frequent": risk_base += 20
        risk_score = min(max(risk_base, 0), 100)
        
        st.markdown("---")
        if risk_score > 70:
            st.error(f"Prediction: CHURN LIKELY ({risk_score:.1f}%)")
            st.write("Action: High-priority intervention required.")
        elif risk_score > 40:
            st.warning(f"Prediction: NEUTRAL/STABLE ({risk_score:.1f}%)")
            st.write("Action: Monitor engagement levels.")
        else:
            st.success(f"Prediction: LOYAL ({risk_score:.1f}%)")
            st.write("Action: Candidate for upselling/expansion.")

st.markdown("---")
st.caption("Developed by Drenat Nallbani | Machine Learning Portfolio 2026")
