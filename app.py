import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Setup
st.set_page_config(page_title="Customer Health Monitor", layout="wide")

# 2. Sidebar with simple explanation
with st.sidebar:
    st.title("What is this?")
    st.write("""
    This tool helps a business owner see which customers are 
    happy and which ones are about to stop buying from you.
    """)
    st.write("**Goal:** Save customers before they leave.")

# 3. Simple Header
st.title("🛡️ Customer Health & Safety Dashboard")
st.markdown("### Helping you keep your customers happy and loyal.")
st.markdown("---")

# 4. The "Big Three" Numbers (Simple Language)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Model Trust Score", "98%", help="How accurate our predictions are.")
with col2:
    st.metric("Money at Risk", "$142,500", help="The total value of customers who are unhappy right now.")
with col3:
    st.metric("Loyalty Rate", "88%", help="The percentage of customers staying with us.")

st.markdown("---")

# 5. The "What-If" Simulator
st.markdown("### 🧪 Customer Happiness Simulator")
st.write("Move the sliders below to see how a customer's behavior changes their risk level.")

c1, c2 = st.columns([1, 1])
with c1:
    usage = st.slider("How much less are they using the product? (%)", 0, 100, 20)
    complaints = st.slider("How many complaints have they made?", 0, 10, 1)
    
    # Simple logic
    risk_score = (usage * 0.7) + (complaints * 10)

with c2:
    if risk_score > 70:
        st.error(f"⚠️ HIGH RISK ({risk_score:.0f}%)")
        st.write("This customer is very unhappy. They need a phone call immediately!")
    elif risk_score > 30:
        st.warning(f"🟡 CAUTION ({risk_score:.0f}%)")
        st.write("This customer is losing interest. Send them a discount or an email.")
    else:
        st.success(f"✅ HEALTHY ({risk_score:.0f}%)")
        st.write("This customer is happy! Keep doing what you are doing.")

st.markdown("---")

# 6. Why do customers leave?
st.markdown("### ❓ Why do our customers leave?")
st.write("This chart shows the biggest reasons people stop buying from us.")

reasons = pd.DataFrame({
    'Reason': ['Too Many Problems', 'Stopped Using It', 'Price too High', 'Better Competitor'],
    'Impact': [45, 30, 15, 10]
})

fig = px.pie(reasons, values='Impact', names='Reason', hole=0.4, 
             color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig, use_container_width=True)

# 7. List of Unhappy Customers
st.markdown("### 📋 Action List: Customers to Save")
st.write("Here are the top customers you should contact today.")

action_list = pd.DataFrame({
    'Customer Name': ['Tech Corp', 'Global Logistics', 'Retail Giant'],
    'Risk Status': ['🚨 Critical', '⚠️ Warning', '⚠️ Warning'],
    'Reason': ['High Complaints', 'Stopped Using App', 'Using App Less'],
    'Potential Loss': ['$5,000', '$2,100', '$1,500']
})
st.table(action_list)
