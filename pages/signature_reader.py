import streamlit as st
import openai
import requests

from src.helpers.open_api import extract_details

st.write("# Example 1: Get Contact from Mail Signature! ✏️")
st.write("This example demonstrates how to extract details from an email signature using OpenAI. Copy and paste an email signature in the text area below and click the 'Extract Details' button to get the extracted details.")

# Set your OpenAI API key
if "openai_api_key" not in st.session_state:
    # add a link to 1_🚀_Setup.py
    st.error("Please set your OpenAI API key first.")
    st.page_link("pages/setup.py", label="Setup", icon="🚀")
else:
    openai.api_key = st.session_state.openai_api_key

if "poool_api_key" not in st.session_state:
    # add a link to 1_🚀_Setup.py
    st.error("Please set your Poool API key first.")
    st.page_link("pages/setup.py", label="Setup", icon="🚀")

# Large text input for email signature
signature = st.text_area("Paste your email signature here:", height=200)

if st.button("Extract Details"):
    if signature:
        with st.spinner("Stay with me while I'm thinking..."):
            details = extract_details(signature)
        st.success("Thanks for your paitence!")

        st.write("### Extracted Details:")
        st.write(details)

        # company = st.text_input("Company", value=details.split('\n')[0])
        # person = st.text_input("Person", value=details.split('\n')[1])
        
        # if st.button("Send to API"):
        #     api_endpoint = "https://your-api-endpoint.com"
        #     data = {"company": company, "person": person}
        #     response = requests.post(api_endpoint, json=data)
        #     if response.status_code == 200:
        #         st.success("Details sent successfully!")
        #     else:
        #         st.error("Failed to send details.")
    else:
        st.error("Please paste an email signature.")