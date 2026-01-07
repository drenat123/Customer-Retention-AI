import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Advanced Page Configuration
st.set_page_config(page_title="Genpact | Clinical Integrity", layout="wide")

# 2. Hardened Enterprise CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #0F172A; color: #F8FAFC; }
    
    /* Executive Card Styling */
    .report-container {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Metrics Visibility */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    
    /* Professional Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 30px; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .stTabs [data-baseweb="tab"] { color: #94A3B8; font-weight: 600; padding: 12px 0px; }
    .stTabs [aria-selected="true"] { color: #6366F1 !important; border-bottom: 2px solid #6366F1 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BRANDING HEADER ---
st.markdown("""
    <div style='border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 30px;'>
        <h1 style='margin:0; font-weight:700; color:#6366F1;'>GENPACT <span style='color:white; font-weight:300;'>| Clinical Integrity Platform</span></h1>
        <p style='margin:0; color:#94A3B8; font-size:14px;'>Advanced Patient Retention & Revenue Protection Engine v2.4</p>
    </div>
    """, unsafe_allow_html=True)

# --- LOGIC: DATA ENGINE ---
def get_data():
    return pd.DataFrame({
        'Provider': ['Adria Dental Group', 'Metropolis Medical', 'St. Jude Specialty', 'Elite Ortho-Care', 'City General'],
        'Revenue_Risk': [45000, 12500, 88000, 52000, 15000],
        'Wait_Time_Score': [85, 20, 95, 40, 30], # 0-100 (Lower is better)
        'Billing_Accuracy': [92, 99, 84, 98, 95],
        'Patient_Volume': [1200, 800, 2400, 1100, 900],
        'Region': ['North', 'East', 'North', 'West', 'South']
    })

df = get_data()

# --- TABS ---
tab_exec, tab_audit, tab_lab = st.tabs(["📊 EXECUTIVE SUMMARY", "🔍 PATIENT FLOW AUDIT", "🧪 STRATEGIC SIMULATOR"])

# --- TAB 1: EXECUTIVE SUMMARY ---
with tab_exec:
    st.markdown("### 📈 Network Performance Overview")
    st.write("This dashboard monitors hospital performance to prevent 'Patient Churn'—when patients leave for a competitor.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Revenue at Risk", "$209,500", "-5.2%", help="Projected loss if retention issues are not addressed.")
    m2.metric("Avg Wait Time", "34m", "+4m", delta_color="inverse")
    m3.metric("Billing Integrity", "93.4%", "Stable")
    m4.metric("Retention Rate", "88.2%", "+1.4%")

    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("#### Revenue Risk by Clinical Provider")
        fig = px.bar(df, x='Provider', y='Revenue_Risk', color='Revenue_Risk',
                     color_continuous_scale='RdYlGn_r', template='plotly_dark')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.markdown("#### Risk Distribution")
        fig_pie = px.pie(df, values='Patient_Volume', names='Region', hole=.5,
                         color_discrete_sequence=px.colors.sequential.Indigo)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 2: AUDIT TOOL ---
with tab_audit:
    st.markdown("### 🔍 Individual Clinic Audit")
    provider = st.selectbox("Select a Hospital or Clinic to Inspect", df['Provider'])
    details = df[df['Provider'] == provider].iloc[0]
    
    st.markdown(f"""
    <div class='report-container'>
        <h2 style='margin:0;'>{provider} Audit Report</h2>
        <p style='color:#94A3B8;'>Operational Status: <b>Active Monitoring</b></p>
        <div style='display:flex; gap:40px; margin-top:20px;'>
            <div><small>MONTHLY REVENUE</small><br><b style='font-size:20px;'>${details['Revenue_Risk']*2:,}</b></div>
            <div><small>PATIENT VOLUME</small><br><b style='font-size:20px;'>{details['Patient_Volume']}</b></div>
            <div><small>BILLING SCORE</small><br><b style='font-size:20px;'>{details['Billing_Accuracy']}%</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Complex Analysis Text
    st.markdown("#### 🚩 AI Risk Assessment")
    risk_score = (details['Wait_Time_Score'] * 0.6) + ((100 - details['Billing_Accuracy']) * 0.4)
    
    if risk_score > 60:
        st.error(f"CRITICAL RISK ({risk_score:.1f}%): High wait times are causing patients to abandon this provider. Immediate intervention required.")
    else:
        st.success(f"STABLE ({risk_score:.1f}%): Patient satisfaction is high. Billing processes are meeting Genpact standards.")

# --- TAB 3: STRATEGY LAB ---
with tab_lab:
    st.markdown("### 🧪 Transformation ROI Simulator")
    st.write("Use this tool to show a hospital CEO how much money they save by using **Genpact's AI services.**")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 1. Current Operations")
        wait_time = st.slider("Average Wait Time (Minutes)", 10, 120, 45)
        billing_fix = st.checkbox("Apply Automated Billing Correction")
    
    with c2:
        st.markdown("#### 2. Financial Impact")
        # Simulator Logic
        improvement = 0
        if wait_time < 30: improvement += 15
        if billing_fix: improvement += 10
        
        savings = (209500 * (improvement / 100))
        st.markdown(f"""
        <div style='background:rgba(99, 102, 241, 0.1); border: 2px solid #6366F1; border-radius:15px; padding:30px; text-align:center;'>
            <h1 style='margin:0; color:#6366F1;'>{improvement}%</h1>
            <p style='margin:0;'>Projected Retention Improvement</p>
            <hr style='border:0.5px solid rgba(255,255,255,0.1);'>
            <h2 style='margin:0;'>${savings:,.0f}</h2>
            <p style='margin:0; opacity:0.6;'>Annual Revenue Recovered</p>
        </div>
        """, unsafe_allow_html=True)
