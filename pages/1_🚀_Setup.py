import streamlit as st
from requests import get
from src.components import sidebar
from src.helpers import poool_api

st.set_page_config(
    page_title="Poool API - Setup",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded",
)

sidebar.show_sidebar()

st.write("# Let's set things up! 🚀")

# Function to validate API keys and login data
def validate_data(poool_api_key, openai_key, db_username, db_password):
    # Add your validation logic here
    if not poool_api_key or not openai_key or not db_username or not db_password:
        return False
    # Example validation: check if keys are of a certain length
    if len(poool_api_key) < 10 or len(openai_key) < 10:
        return False
    return True

# Streamlit app
st.title("Setup Page")

# Input fields
poool_api_key = st.text_input("Poool API Key")
openai_key = st.text_input("Open AI Key")
db_username = st.text_input("Postgres Database Username")
db_password = st.text_input("Postgres Database Password", type="password")

# Validate and store data in session state
if st.button("Submit"):
    if validate_data(poool_api_key, openai_key, db_username, db_password):
        st.session_state['poool_api_key'] = poool_api_key
        st.session_state['openai_key'] = openai_key
        st.session_state['db_username'] = db_username
        st.session_state['db_password'] = db_password
        st.success("Data validated and stored successfully!")
    else:
        st.error("Invalid data. Please check your inputs.")