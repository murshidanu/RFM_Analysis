import streamlit as st
import importlib
import sys

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Navigation sidebar
st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.session_state.current_page = "Home"
if st.sidebar.button("RFM Analysis"):
    st.session_state.current_page = "RFM"
if st.sidebar.button("RFM Item Analysis"):
    st.session_state.current_page = "RFM_Item"
if st.sidebar.button("Churn Analysis"):
    st.session_state.current_page = "Churn"


# Function to run a script without a main() function
def run_script(script_name):
    try:
        # Clear any existing modules with this name
        if script_name in sys.modules:
            del sys.modules[script_name]

        # Import the module (this executes the script)
        importlib.import_module(script_name)
    except Exception as e:
        st.error(f"Error loading {script_name}: {e}")
        st.exception(e)


# Render the selected page
if st.session_state.current_page == "Home":
    # Home page content directly here
    st.title("Home")
    st.write("Welcome to the RFM Analysis Tool")
    # ... other home page content

elif st.session_state.current_page == "RFM":
    run_script("1_rfmsaas")

elif st.session_state.current_page == "RFM_Item":
    run_script("2_rfmitem")

elif st.session_state.current_page == "Churn":
    run_script("3_churn")