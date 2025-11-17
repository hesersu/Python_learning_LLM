import os
import streamlit as st
from dotenv import load_dotenv
from main import query_capital, setup_phoenix_tracing

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Capital City Finder",
    page_icon="🌍",
    layout="centered"
)

# Initialize session state for Phoenix tracing
if "phoenix_setup" not in st.session_state:
    setup_phoenix_tracing()
    st.session_state.phoenix_setup = True

# Title and description
st.title("🌍 Capital City Finder")
st.markdown("Ask me about the capital of any country using Google Gemini!")

# Check for API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error(
        "Missing GEMINI_API_KEY environment variable. "
        "Please set it in your .env file and restart the app."
    )
    st.stop()

# Input field
country_name = st.text_input(
    "Enter a country name:",
    placeholder="e.g., France, Japan, Brazil",
    help="Type any country name and press Enter"
)

# Query button and response
if country_name:
    st.markdown("---")
    st.subheader(f"Capital of {country_name}")

    # Create a placeholder for streaming output
    response_placeholder = st.empty()
    full_response = ""

    try:
        # Stream the response
        with st.spinner("Thinking..."):
            for chunk in query_capital(country_name, api_key):
                full_response += chunk
                response_placeholder.markdown(full_response)

        st.success("Response complete!")

    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini Flash with Phoenix tracing")
