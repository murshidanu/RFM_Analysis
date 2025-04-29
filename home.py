import streamlit as st

st.set_page_config(
    page_title="FMCG Analytics Suite",
    page_icon="📊",
    layout="wide"
)

st.title("FMCG Analytics Dashboard")
st.write("""
Welcome to the FMCG Analytics Suite. Select an analysis from the sidebar to begin.
""")

st.sidebar.success("Select an analysis above.")