import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Genpact | Patient Intelligence", layout="wide")

# 2. Hardened CSS (Fixed Visibility)
st.markdown("""
    <style>
    /* Force high-contrast dark background */
    .stApp { background-color: #0B0E14 !important; color: #FFFFFF !important; }
    
    /* Executive Header Card */
    .header-box {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #6366F1;
        margin-bottom: 25px;
    }
    
    /* Metric Cards - Forcing Visibility */
    div[data-testid="stMetric"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; }
    
    /* Professional Typography */
    h1, h2, h3, p, span, li { color: #FFFFFF !important; }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161B22 !important;
        color: #94A3B8 !important;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { color: #6366F1 !important; border-bottom: 2px solid #6366F1 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Branded Header
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; font-size: 24px;'>PATIENT RETENTION INTELLIGENCE</h1>
        <p style='margin:0; opacity:0.7; font-size: 14px;'>GENPACT OPERATIONAL EXCELLENCE FRAMEWORK</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Dataset
data = pd.DataFrame({
    'ID': ['P-101', 'P-102', 'P-103', 'P-104'],
    'Name': ['Adria Dental', 'Metropolis', 'St. Jude', 'Elite Ortho'],
    'Risk': [88, 12, 45, 92],
    'Value': [45000, 12000, 21000, 52000]
})

# 5. Dashboard Tabs
tab1, tab2, tab3 = st.tabs(["📊 Performance", "🔍 Risk Audit", "🛠️ ROI Simulator"])

with tab1:
    st.markdown("### Quarterly Network Health")
    c1, c2, c3 = st.columns(3)
    c1.metric("Loyalty Index", "94.2%", "+2.1%")
    c2.metric("Revenue at Risk", "$142,500", "Critical")
    c3.metric("Retention Target", "96%", "In-Progress")
    
    st.markdown("---")
    # Professional Blue/Indigo Chart
    fig = px.bar(data, x='Name', y='Risk', color='Risk', 
                 color_continuous_scale=['#4F46E5', '#818CF8'],
                 labels={'Risk': 'Attrition Risk (%)'})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      font_color="white", margin=dict(t=20, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Patient Record Investigation")
    choice = st.selectbox("Search Identifier", data['Name'])
    p_info = data[data['Name'] == choice].iloc[0]
    
    st.markdown(f"""
        <div style='background:#161B22; padding:20px; border-radius:10px; border:1px solid #30363D;'>
            <h2 style='margin:0; color:#6366F1 !important;'>{choice}</h2>
            <p>Annual Contract Value: <b>${p_info['Value']:,}</b></p>
            <p>Calculated Probability of Attrition: <b>{p_info['Risk']}%</b></p>
        </div>
    """, unsafe_allow_html=True)
    st.progress(p_info['Risk'] / 100)

with tab3:
    st.markdown("### Genpact Transformation Lab")
    st.write("Simulate the impact of Genpact's AI Automation on this account.")
    automation = st.select_slider("AI Automation Tier", options=["Standard", "Advanced", "Genpact Elite"])
    
    impact = 25 if automation == "Genpact Elite" else 5
    st.success(f"Strategy Result: Moving to {automation} reduces risk by {impact}%.")
    st.write(f"Estimated Revenue Recovered: **${(142500 * (impact/100)):,.0f}**")
