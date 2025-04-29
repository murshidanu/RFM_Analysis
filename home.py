import streamlit as st

st.set_page_config(
    page_title="FMCG Analytics",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"


def home_page():
    st.title("FMCG Analytics Dashboard")
    st.write("Select an analysis type to begin:")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📈 RFM Analysis", use_container_width=True):
            st.session_state.current_page = "RFM"
            st.rerun()
    with col2:
        if st.button("📈 RFM_Item Analysis", use_container_width=True):
            st.session_state.current_page = "RFM_Item"
            st.rerun()
    with col3:
        if st.button("⚠️ Churn Analysis", use_container_width=True):
            st.session_state.current_page = "Churn"
            st.rerun()


# Page router
if st.session_state.current_page == "Home":
    home_page()
elif st.session_state.current_page == "RFM":
    st.switch_page("pages/1.rfmsaas.py")
elif st.session_state.current_page == "RFM_Item":
    st.switch_page("pages/2.rfmitem.py")
elif st.session_state.current_page == "Churn":
    st.switch_page("pages/3.churn.py")