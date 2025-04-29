import streamlit as st
import sys

# Only set page config if this script is run directly (not imported)
if __name__ == "__main__":
    st.set_page_config(
        page_title="RFM Analysis",
        page_icon="📊",
        layout="wide"
    )

# Rest of your imports
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
    run_script("rfmsaas")

elif st.session_state.current_page == "RFM_Item":
    run_script("rfmitem")

elif st.session_state.current_page == "Churn":
    run_script("churn")