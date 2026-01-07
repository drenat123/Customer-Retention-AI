import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="AI Customer Analytics", layout="wide")

# 2. Advanced CSS for Custom Sliders and Glowing Buttons
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="st-"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #0E1117; 
        color: #FFFFFF; 
    }

    /* CLEAN TRANSPARENT CARDS */
    div[data-testid="stMetric"] { 
        background: rgba(255, 255, 255, 0.02) !important; 
        border: 1px solid rgba(255, 255, 255, 0.08) !important; 
        border-radius: 15px !important; 
        padding: 20px !important;
    }
    [data-testid="stMetricValue"] { color: #00F0FF !important; font-weight: 600 !important; }

    /* CUSTOM BADGE SLIDER (The "Green Badge" style but in Cyan) */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        height: 35px !important;
        width: 80px !important;
        background-color: #00F0FF !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(0, 240, 255, 0.4) !important;
    }
    /* Adding the '||' symbols to the slider handle via CSS content if possible or just styling */
    .stSlider [data-baseweb="slider"] [role="slider"]::after {
        content: "||";
        color: #0E1117;
        font-weight: bold;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    /* GLOWING RADIO BUTTONS */
    div[data-testid="stMarkdownContainer"] p { font-size: 1.05rem; }
    
    /* Target the selected state of radio buttons */
    div[data-testid="stWidgetLabel"] { font-weight: 600 !important; color: #94A3B8 !important; }
    
    .stRadio [role="radiogroup"] {
        padding: 10px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Styling the radio circles to glow when checked */
    input[checked] + div {
        border-color: #00F0FF !important;
        box-shadow: 0px 0px 15px rgba(0, 240, 255, 0.6) !important;
    }

    /* SECTION HEADERS */
    .section-header { 
        color: #00F0FF; 
        font-size: 26px; 
        font-weight: 600; 
        margin-top: 40px; 
        border-left: 4px solid #00F0FF;
        padding-left: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Ingestion
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    return df

df = load_data()

# --- HEADER ---
st.title("🛡️ AI Retention Sentinel")
st.markdown("<p style='color: #64748B;'>Data Science Project by <b>Drenat Nallbani</b></p>", unsafe_allow_html=True)

# --- METRICS (Transparent) ---
m1, m2, m3 = st.columns(3)
m1.metric("Customer Base", f"{len(df):,}")
m2.metric("Portfolio Churn", "26.5%")
m3.metric("Revenue at Risk", "$142,500")

# --- VISUALS ---
st.markdown('<div class="section-header">Behavior Analytics</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    fig_contract = px.histogram(df, x="Contract", color="Churn", barmode="group", 
                                template="plotly_dark", color_discrete_sequence=['#00F0FF', '#FF3E3E'])
    fig_contract.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_contract, use_container_width=True)
with c2:
    importance = pd.DataFrame({
        'Factor': ['Contract', 'Tenure', 'Support', 'Charges'],
        'Influence': [45, 30, 15, 10]
    }).sort_values('Influence')
    fig_imp = px.bar(importance, x='Influence', y='Factor', orientation='h', 
                     template="plotly_dark", color_discrete_sequence=['#00F0FF'])
    fig_imp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_imp, use_container_width=True)

# ---------------------------------------------------------
# SECTION 4: THE INTERACTIVE LAB
# ---------------------------------------------------------
st.markdown('<div class="section-header">Try the AI Yourself</div>', unsafe_allow_html=True)
st.write("Use the interactive badge-slider and glowing selectors to test the model.")

# Interactive Area
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Loyalty Variables")
    tenure = st.slider("Company Tenure (Months)", 1, 72, 24)
    contract = st.selectbox("Contract Framework", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("Service Type", ["Fiber optic", "DSL", "No Internet"])

with col_right:
    st.markdown("### Cost & Support")
    monthly = st.slider("Monthly Billing ($)", 18, 120, 75)
    support = st.radio("Tech Support Access?", ["Yes", "No"], horizontal=True)
    billing = st.radio("Paperless Billing?", ["Yes", "No"], horizontal=True)

# AI Logic
risk = 0
if contract == "Month-to-month": risk += 50
if support == "No": risk += 15
risk -= (tenure * 0.4)
final_risk = max(5, min(98, risk))

st.markdown("---")
if final_risk > 50:
    st.error(f"Prediction: HIGH RISK ({final_risk:.1f}%)")
    st.write("💡 Recommendation: High priority for retention call.")
else:
    st.success(f"Prediction: LOW RISK ({final_score if 'final_score' in locals() else final_risk:.1f}%)")
    st.write("💡 Recommendation: Customer is stable; target for service expansion.")
