import streamlit as st

st.set_page_config(
    page_title="FMCG Analytics Portal",
    page_icon="📊",
    layout="centered"
)

st.title("Analytics Dashboard")
st.markdown("""
Select an analysis type to begin:
""")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1.rfmsaas.py", label="📈 RFM Analysis", icon="✨")
with col2:
    st.page_link("pages/2.rfmitem.py", label="⚠️ RFM Item Analysis", icon="🚨")
with col2:
    st.page_link("pages/3.churn.py", label="⚠️ Churn Analysis", icon="🚨")
st.sidebar.markdown("Navigate to your desired analysis")