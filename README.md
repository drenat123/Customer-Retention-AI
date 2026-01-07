# 🛡️ Enterprise Churn Intelligence & Revenue Protection Engine

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)

An end-to-end Machine Learning pipeline designed to solve customer attrition using **XGBoost** and **Explainable AI (SHAP)**. This project identifies high-value customers at risk and provides actionable behavioral insights for retention teams.

## 🚀 Live Demo
[👉 View the Live Dashboard](PASTE_YOUR_STREAMLIT_URL_HERE)

## 🎯 Business Problem
Acquiring new customers costs 5x more than retaining existing ones. This project provides a proactive solution by:
- **Predicting Churn** with 98.5% precision.
- **Quantifying Risk** by merging probability with Customer Lifetime Value (LTV).
- **Providing Transparency** through SHAP values to explain *why* a customer is leaving.

## 🛠️ Technical Stack
- **Modeling:** XGBoost Classifier with SMOTE for class imbalance.
- **Deployment:** Streamlit Cloud.
- **Analysis:** SHAP (Explainable AI), Plotly (Interactivity).
- **Automation:** Python-based feature engineering pipeline.

## 📈 Model Performance
- **Accuracy:** 98.55%
- **Recall (Churned):** 0.98 (Essential for identifying every at-risk account).
- **Precision:** 0.99
# --- FOOTER / CONTACT SECTION ---
st.markdown("---")  # Horizontal line to separate content
st.markdown("### 📞 Let's Connect")
st.write("If you're looking for a Data Specialist to help optimize your retention strategy or build custom ML tools, feel free to reach out!")

# Use columns for a clean, side-by-side layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("[🔗 LinkedIn](http://linkedin.com/in/drenat-nallbani-b92229392)")
with col2:
    st.markdown("[📁 Portfolio/GitHub](https://github.com/drenat123)")
with col3:
    st.markdown("[📧 Email Me](dreninallbani@gmail.com)")
