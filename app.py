import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Config
st.set_page_config(page_title="Genpact | Patient Intelligence", layout="wide", initial_sidebar_state="collapsed")

# 2. Advanced CSS for a "SaaS Product" Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Public Sans', sans-serif; background-color: #F1F5F9; }
    
    /* Executive Header */
    .header-container { background: linear-gradient(90deg, #0F172A 0%, #1E293B 100%); padding: 2rem; border-radius: 0 0 20px 20px; color: white; margin-bottom: 2rem; }
    
    /* Modern Card UI */
    div[data-testid="stMetric"] {
        background: white !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Data Container Branding */
    .report-card { background: white; padding: 25px; border-radius: 16px; border: 1px solid #E2E8F0; margin-bottom: 20px; }
    
    /* Clean Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid #CBD5E1; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre; background-color: transparent; border: none; color: #64748B; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: #4F46E5 !important; border-bottom: 3px solid #4F46E5 !important; }
    
    /* Professional Sliders */
    .stSlider [data-baseweb="slider"] { margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Branding Header
st.markdown("""
    <div class="header-container">
        <h1 style='margin:0; font-weight:700; letter-spacing:-1px;'>Patient Retention Intelligence</h1>
        <p style='margin:0; opacity:0.8; font-weight:300;'>Operational Excellence Framework | Healthcare Vertical</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Initialization
data = pd.DataFrame({
    'ID': ['P-8821', 'P-9902', 'P-4410', 'P-1205', 'P-3391'],
    'Patient': ['Adria Dental Group', 'Metropolis Clinic', 'St. Jude Center', 'Elite Ortho', 'City Dental'],
    'Score': [88, 12, 56, 94, 21],
    'Value': [45000, 12000, 21000, 52000, 9500],
    'Risk_Level': ['Critical', 'Stable', 'Monitoring', 'Critical', 'Stable'],
    'Last_Audit': ['24h ago', '12d ago', '3d ago', '6h ago', '20d ago']
})

# 5. Reorganized Tab Navigation
tab_summary, tab_intelligence, tab_simulator = st.tabs(["📊 Executive Summary", "🔍 Risk Audit", "🛠️ Transformation Lab"])

# --- TAB 1: EXECUTIVE SUMMARY ---
with tab_summary:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Network Health", "84.2%", "Optimal")
    col2.metric("Revenue at Attrition Risk", "$142.5K", "-5.4% YoY")
    col3.metric("Retention Target", "96.0%", "In Progress")
    col4.metric("Avg Wait Time", "18m", "-2m Improvement")
    
    st.markdown("---")
    
    c_left, c_right = st.columns([2, 1])
    with c_left:
        st.markdown("#### Attrition Distribution by Provider")
        fig = px.bar(data, x='Patient', y='Score', color='Score', 
                     color_continuous_scale='RdYlGn_r', template='plotly_white')
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=350)
        st.plotly_chart(fig, use_container_width=True)
    with c_right:
        st.markdown("#### Clinical Risk Profile")
        fig_pie = px.pie(data, values='Value', names='Risk_Level', 
                         hole=0.6, color_discrete_sequence=['#4F46E5', '#EF4444', '#F59E0B'])
        fig_pie.update_layout(showlegend=False, height=350, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 2: RISK AUDIT ---
with tab_intelligence:
    st.markdown("### Deep-Dive Audit Tool")
    target = st.selectbox("Select Provider/Patient Identifier", data['ID'] + " - " + data['Patient'])
    selected_id = target.split(" - ")[0]
    p_info = data[data['ID'] == selected_id].iloc[0]
    
    st.markdown(f"""
    <div class="report-card">
        <h2 style='margin-top:0;'>{p_info['Patient']}</h2>
        <p style='color:#64748B;'>Patient ID: {p_info['ID']} | Last Operational Audit: {p_info['Last_Audit']}</p>
        <hr style='border: 0.5px solid #E2E8F0;'>
        <div style='display: flex; gap: 50px;'>
            <div><p style='margin:0; font-size:0.8rem; color:#64748B;'>CONTRACT VALUE</p><b>${p_info['Value']:,}</b></div>
            <div><p style='margin:0; font-size:0.8rem; color:#64748B;'>RISK CATEGORY</p><b>{p_info['Risk_Level']}</b></div>
            <div><p style='margin:0; font-size:0.8rem; color:#64748B;'>MODEL CONFIDENCE</p><b>98.4%</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("**Calculated Probability of Attrition**")
    st.progress(p_info['Score'] / 100)
    st.write(f"The patient provider currently shows a **{p_info['Score']}%** probability of leaving the network.")

# --- TAB 3: TRANSFORMATION LAB ---
with tab_simulator:
    st.markdown("### Process Transformation Simulator")
    st.write("Adjust operational parameters to simulate Genpact transformation impact.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        efficiency = st.select_slider("AI Billing Integration Level", options=["Baseline", "Optimized", "Predictive", "Genpact-Elite"])
        wait_time = st.slider("Target Service Delivery (Minutes)", 5, 60, 25)
    
    with col_b:
        # Business Logic Simulation
        saving_pct = 22 if efficiency == "Genpact-Elite" else 5
        st.markdown(f"""
        <div style='background-color:#EEF2FF; padding:30px; border-radius:12px; border:1px solid #C7D2FE;'>
            <h4 style='margin-top:0; color:#3730A3;'>ROI Projection</h4>
            <p style='color:#312E81;'>Implementing <b>{efficiency}</b> workflows and maintaining a <b>{wait_time}m</b> wait time reduces attrition risk by <b>{saving_pct}%</b>.</p>
            <h3 style='color:#4F46E5; margin-bottom:0;'>Potential Recovery: ${142500 * (saving_pct/100):,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)
