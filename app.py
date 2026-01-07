import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Premium Page Config
st.set_page_config(page_title="Executive Insights", layout="wide")

# Custom CSS for a "Premium" feel (Clean fonts and spacing)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Navigation
st.sidebar.title("💎 Luxury Retail AI")
menu = st.sidebar.radio("Navigate", ["Company Overview", "Customer Search", "Strategy Lab"])

# --- DATASET (Simulated for your academy project) ---
data = pd.DataFrame({
    'Name': ['Tech Corp', 'Global Logistics', 'Retail Giant', 'Alpha Design', 'Omega Inc'],
    'Status': ['🚨 Critical', '✅ Healthy', '⚠️ Warning', '✅ Healthy', '🚨 Critical'],
    'Health_Score': [14, 92, 45, 88, 12],
    'Revenue': [5000, 12000, 3500, 9000, 4200],
    'Last_Contact': ['2 days ago', '1 month ago', '5 days ago', '2 weeks ago', 'Yesterday']
})

# ---------------------------------------------------------
# TAB 1: COMPANY OVERVIEW
# ---------------------------------------------------------
if menu == "Company Overview":
    st.title("Company Health Overview")
    st.markdown("A bird's-eye view of your business stability.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue at Risk", "$9,200", "🚨")
    col2.metric("Overall Loyalty", "84%", "+2%")
    col3.metric("Active Saving Campaigns", "3", "Active")

    st.markdown("---")
    st.markdown("### Why are customers leaving?")
    fig = px.bar(data, x='Name', y='Health_Score', color='Health_Score', 
                 color_continuous_scale='RdYlGn', title="Individual Customer Health Scores")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: CUSTOMER SEARCH (The Specific Look-up)
# ---------------------------------------------------------
elif menu == "Customer Search":
    st.title("Customer Intelligence Lookup")
    
    search_query = st.selectbox("Select a specific customer to inspect:", data['Name'])
    
    # Get specific customer data
    user_data = data[data['Name'] == search_query].iloc[0]
    
    st.markdown(f"## Report for: {search_query}")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("**Current Status**")
        st.subheader(user_data['Status'])
    with c2:
        st.write("**Customer Value**")
        st.subheader(f"${user_data['Revenue']}")
    with c3:
        st.write("**Last Interaction**")
        st.subheader(user_data['Last_Contact'])

    st.markdown("---")
    
    # Visual Health Gauge
    score = user_data['Health_Score']
    st.write(f"**Health Rating: {score}/100**")
    st.progress(score / 100)
    
    if score < 30:
        st.error("🛑 ACTION REQUIRED: This customer is highly likely to leave. Schedule a meeting today.")
    elif score < 60:
        st.warning("⚠️ PROACTIVE OUTREACH: Send a loyalty bonus or check-in email.")
    else:
        st.success("✨ ALL CLEAR: Customer is satisfied and engaged.")

# ---------------------------------------------------------
# TAB 3: STRATEGY LAB
# ---------------------------------------------------------
else:
    st.title("Strategy Simulation Lab")
    st.write("Test how changes in your service affect customer loyalty.")
    
    # Simple Slider Logic
    service_quality = st.select_slider("Improve Support Speed", options=["Slow", "Average", "Fast", "Instant"])
    price_change = st.slider("Price Discount (%)", 0, 50, 0)
    
    st.info(f"By choosing **{service_quality}** support and a **{price_change}%** discount, you could save an estimated **12%** more customers next month.")
