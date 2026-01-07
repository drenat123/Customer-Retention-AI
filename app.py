import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Executive Command Center", layout="wide", initial_sidebar_state="collapsed")

# 2. Ultra-Premium Styling (Custom CSS)
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Premium Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        transition: 0.3s;
    }
    [data-testid="stMetric"]:hover { border: 1px solid #00ff88; background: rgba(0, 255, 136, 0.02); }
    
    /* Buttons and Sliders */
    .stSlider > div > div > div > div { background-color: #00ff88; }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header & Navigation
st.markdown("<h1 style='text-align: center; color: #00ff88; margin-bottom: 0;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.6; margin-top: 0;'>AI-Powered Customer Intelligence Feed</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Market Health", "🔍 Customer Deep-Dive", "🧪 Strategy Sandbox"])

# DATA (Simulated)
data = pd.DataFrame({
    'Name': ['Tech Corp', 'Global Logistics', 'Retail Giant', 'Alpha Design'],
    'Risk': [88, 12, 45, 10],
    'Value': [5000, 12000, 3500, 9000]
})

# --- TAB 1: DASHBOARD ---
with tab1:
    st.markdown("### National Overview")
    m1, m2, m3 = st.columns(3)
    m1.metric("REVENUE AT RISK", "$142,500", "-5%")
    m2.metric("HEALTH INDEX", "92/100", "+2")
    m3.metric("SAVED REVENUE", "$45,200", "Live")
    
    st.markdown("---")
    fig = px.area(data, x='Name', y='Risk', title="Volatility Trend", 
                 color_discrete_sequence=['#00ff88'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                      font_color="white", height=300)
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: SEARCH ---
with tab2:
    target = st.selectbox("Select Client", data['Name'])
    client = data[data['Name'] == target].iloc[0]
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"## {target}")
        st.write(f"Monthly Value: **${client['Value']}**")
        st.write("Engagement Status: **Active**")
    with c2:
        # Progress bar for risk
        r_color = "red" if client['Risk'] > 50 else "green"
        st.markdown(f"<h3 style='color: {r_color}'>Risk Level: {client['Risk']}%</h3>", unsafe_allow_html=True)
        st.progress(client['Risk'] / 100)

# --- TAB 3: LAB ---
with tab3:
    st.markdown("### Risk Mitigation Simulator")
    promo = st.select_slider("Loyalty Program Tier", options=["Basic", "Silver", "Gold", "Platinum"])
    st.info(f"Applying **{promo}** tier incentives would likely reduce churn by **{20 if promo == 'Platinum' else 5}%**.")
