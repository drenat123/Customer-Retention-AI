import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Healthcare Revenue Integrity", layout="wide")

# 2. Corporate Styling (Genpact Standard Blue & Grey)
st.markdown("""
    <style>
    /* Main Background and Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; color: #1E293B; }
    
    /* Metric Card Styling */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #0F172A; }
    [data-testid="stMetricLabel"] { font-size: 0.9rem !important; text-transform: uppercase; letter-spacing: 1px; color: #64748B; }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Remove Emojis and standard headers */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 2px solid #E2E8F0; }
    .stTabs [data-baseweb="tab"] { color: #64748B; font-weight: 500; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { color: #2563EB !important; border-bottom: 2px solid #2563EB !important; }
    
    /* Error/Success messages custom look */
    .stAlert { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-left: 5px solid #2563EB; color: #1E293B; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATASET ---
patients = pd.DataFrame({
    'Patient_Identifier': ['P-1001', 'P-1002', 'P-1003', 'P-1004'],
    'Risk_Score': [22, 5, 78, 91],
    'Annual_Revenue': [5200, 12000, 3500, 9000],
    'Status': ['Stable', 'Optimal', 'At Risk', 'Critical']
})

# 3. Header
st.markdown("<h2 style='margin-bottom:0;'>Healthcare Revenue Integrity Platform</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748B; margin-top:0;'>Genpact Operational Excellence Framework</p>", unsafe_allow_html=True)

# 4. Navigation
tab_main, tab_search, tab_config = st.tabs(["Operations Overview", "Patient Record Search", "Risk Parameters"])

# --- OPERATIONS OVERVIEW ---
with tab_main:
    st.markdown("### Portfolio Performance")
    col1, col2, col3 = st.columns(3)
    col1.metric("Patient Retention Rate", "94.2%", "Target: 92%")
    col2.metric("Revenue Integrity Score", "98.8%", "Above Average")
    col3.metric("Projected Leakage", "$210,400", "-4.1% MoM")

    st.markdown("---")
    st.markdown("### Regional Attrition Distribution")
    fig = px.bar(patients, x='Patient_Identifier', y='Risk_Score', 
                 labels={'Risk_Score': 'Attrition Probability (%)'},
                 color='Risk_Score', color_continuous_scale='Blues')
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='#64748B', height=350)
    st.plotly_chart(fig, use_container_width=True)

# --- PATIENT SEARCH ---
with tab_search:
    st.markdown("### Clinical Record Audit")
    query = st.selectbox("Select Patient Identifier", patients['Patient_Identifier'])
    p_row = patients[patients['Patient_Identifier'] == query].iloc[0]
    
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"Summary for {query}\nCurrent Status: {p_row['Status']}\nAnnual Value: ${p_row['Annual_Revenue']}")
    with c2:
        st.write("Calculated Risk Level")
        st.progress(p_row['Risk_Score'] / 100)
        st.write(f"The statistical probability of this patient seeking an alternative provider is {p_row['Risk_Score']}%.")

# --- RISK PARAMETERS ---
with tab_config:
    st.markdown("### Predictive Modeling Variables")
    st.write("Adjust operational thresholds to calculate potential attrition.")
    billing_efficiency = st.select_slider("Billing Automation Level", options=["Manual", "Standard", "Advanced", "Elite"])
    wait_threshold = st.slider("Max Acceptable Wait Time (Minutes)", 15, 60, 30)
    
    potential_saving = 15 if billing_efficiency == "Elite" else 2
    st.success(f"Strategic Result: Implementing this configuration would improve retention by {potential_saving}%.")
