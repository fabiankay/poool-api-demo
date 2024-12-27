from requests import get
import streamlit as st

def validate_api_key(api_key):
    if api_key:
        # semd a request to the server to verify the API key
        # if the response is 200, then the API key is valid
        response = get("https://app.poool.cc/api/2/hello_its_me", headers={"Authorization": f"Bearer {api_key}"})
        if response.status_code == 200:
            # Save API key to session state
            st.session_state.poool_api_key = api_key
            st.rerun()
        else:
            if "poool_api_key" in st.session_state:
                del st.session_state.poool_api_key
            st.error("Invalid API key.")
