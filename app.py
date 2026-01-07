import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Advanced Page Config
st.set_page_config(page_title="Genpact | Sentinel AI", layout="wide")

# 2. Premium "Glass" UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;700&display=swap');
    
    /* Background Gradient */
    .stApp {
        background: radial-gradient(circle at top right, #1E293B, #0F172A);
        color: #F8FAFC;
        font-family: 'Public Sans', sans-serif;
    }
    
    /* High-End Card Design */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 15px;
    }
    
    /* Fix Visibility of Standard Elements */
    div[data-testid="stMetric"] { background: transparent !important; border: none !important; }
    [data-testid="stMetricValue"] { color: #818CF8 !important; font-size: 2rem !important; }
    
    /* Custom Sidebar/Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent !important;
        border: none !important;
        color: #94A3B8 !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] { color: #6366F1 !important; border-bottom: 3px solid #6366F1 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_hospital_data():
    return pd.DataFrame({
        'Clinic': ['Adria Dental', 'Metropolis Med', 'St. Jude Specialty', 'Elite Ortho', 'City General'],
        'Risk_Score': [82, 14, 91, 44, 28],
        'Revenue_at_Stake': [125000, 45000, 210000, 95000, 32000],
        'Wait_Time_Min': [55, 12, 88, 32, 22],
        'Staff_Ratio': [0.4, 0.9, 0.3, 0.7, 0.8], # Percentage of staff availability
        'Billing_Leakage': [12, 2, 18, 5, 4] # % of revenue lost to errors
    })

df = load_hospital_data()

# --- HEADER ---
st.markdown("""
    <div style='padding: 20px 0px;'>
        <h1 style='color: white; margin-bottom: 0px;'>GENPACT <span style='color: #6366F1;'>SENTINEL</span></h1>
        <p style='color: #94A3B8; font-size: 16px; margin-top: 5px;'>Predictive Revenue Integrity & Patient Retention Engine</p>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🏛️ NETWORK OVERVIEW", "🔍 CLINICAL DEEP-DIVE", "📈 ROI SIMULATOR"])

# --- TAB 1: EXECUTIVE VIEW ---
with tab1:
    st.markdown("### Portfolio Key Performance Indicators")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Retention Rate", "91.4%", "+2.3%")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Revenue Leakage", "$507K", "-12%", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Wait Score", "38m", "+4m", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Operational Health", "88%", "Stable")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### Patient Retention Risk by Facility")
    fig = px.bar(df, x='Clinic', y='Risk_Score', color='Risk_Score',
                 color_continuous_scale='Purples', template='plotly_dark')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: AUDIT VIEW ---
with tab_audit := tab2:
    st.markdown("### Facility Integrity Audit")
    selected_clinic = st.selectbox("Select Clinic for Analysis", df['Clinic'])
    row = df[df['Clinic'] == selected_clinic].iloc[0]
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <h2 style='margin-top:0; color:#818CF8;'>{selected_clinic}</h2>
            <p style='color:#94A3B8;'>Patient Attrition Risk: <b style='color:white;'>{row['Risk_Score']}%</b></p>
            <p style='color:#94A3B8;'>Revenue at Stake: <b style='color:white;'>${row['Revenue_at_Stake']:,}</b></p>
            <hr style='opacity:0.1'>
            <p style='font-size:14px;'><b>Genpact Analysis:</b> This facility shows a high correlation between wait times ({row['Wait_Time_Min']}m) 
            and patient exit intent. Staffing levels are currently at {row['Staff_Ratio']*100}% of optimal capacity.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("#### Operational Vulnerabilities")
        # Fixed the error here by using a more stable color scale
        radar_data = pd.DataFrame(dict(
            r=[row['Wait_Time_Min'], (1-row['Staff_Ratio'])*100, row['Billing_Leakage']*5],
            theta=['Wait Time', 'Understaffing', 'Billing Errors']))
        fig_radar = px.line_polar(radar_data, r='r', theta='theta', line_close=True, template='plotly_dark')
        fig_radar.update_traces(fill='toself', line_color='#6366F1')
        fig_radar.update_layout(paper_bgcolor='rgba(0,0,0,0)', polar=dict(bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig_radar, use_container_width=True)

# --- TAB 3: SIMULATOR ---
with tab3:
    st.markdown("### Transformation ROI Lab")
    st.write("Calculate the fiscal impact of Genpact's AI-driven billing and scheduling automation.")
    
    sl1, sl2 = st.columns(2)
    with sl1:
        auto_level = st.select_slider("Automation Implementation", options=["Manual", "Hybrid", "Genpact AI-Elite"])
        reduction = st.slider("Target Wait Time Reduction (%)", 0, 100, 25)
    
    with sl2:
        # Business Logic
        recovery_base = 507000 # Total Leakage
        multiplier = 0.8 if auto_level == "Genpact AI-Elite" else 0.3
        total_recovery = (recovery_base * multiplier) + (reduction * 1000)
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); padding:40px; border-radius:20px; text-align:center;'>
            <p style='margin:0; text-transform:uppercase; font-size:12px; letter-spacing:2px;'>Projected Annual Recovery</p>
            <h1 style='margin:0; font-size:48px;'>${total_recovery:,.0f}</h1>
            <p style='margin-bottom:0; opacity:0.8;'>Based on {auto_level} Workflows</p>
        </div>
        """, unsafe_allow_html=True)
