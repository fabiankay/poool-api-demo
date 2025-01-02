import streamlit as st
from requests import get
from src.helpers import poool_api
from src.helpers import open_api
from src.helpers import prism

st.write("# Let's set things up! 🚀")
st.caption("Please note that the API keys are stored in your browser's local storage and are not shared with the server. This also means that you will need to re-enter the API keys if you refresh the page.")
st.write("To get started, please provide the following information:")

# Input fields
st.write("### Poool Connection")
if "poool_api_key" in st.session_state:
    st.success("API key verified.")
else:
    poool_api_key = st.text_input("Poool API Key", type="password")
    if st.button("Verify API Key", key="poool"):
        poool_api.validate_api_key(poool_api_key)

st.write("### Open AI Connection")
if "openai_api_key" in st.session_state:
    st.success("API key verified.")
else:
    openai_key = st.text_input("Open AI Key", type="password")
    if st.button("Verify API Key", key="open-ai"):
        open_api.validate_api_key(openai_key)

st.write("### Prism Connection")
if "prism_username" and "prism_password" in st.session_state:
    st.success("Database credentials verified.")
else:
    db_username = st.text_input("Prism Username")
    db_password = st.text_input("Prism Password", type="password")
    if st.button("Verify database credentials", key="prism"):
        prism.validate_login(db_username, db_password)
