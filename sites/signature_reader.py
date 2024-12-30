import json
import streamlit as st
import openai

from src.helpers.open_api import extract_details
from src.helpers.poool_api import create_company, create_person, get_companies
from src.models.company import Company, Person

st.write("# Example 1: Get Contact from Mail Signature! ✏️")
st.write("This example demonstrates how to extract details from an email signature using OpenAI. Copy and paste an email signature in the text area below and click the 'Extract Details' button to get the extracted details.")

# Initialize session state data
if "data" not in st.session_state:
    st.session_state["data"] = {}

if "details_extracted" not in st.session_state:
    st.session_state.details_extracted = False

def callback():
    st.session_state.details_extracted = True

# Set your OpenAI API key
if "openai_api_key" not in st.session_state:
    # add a link to 1_🚀_Setup.py
    st.error("Please set your OpenAI API key first.")
else:
    openai.api_key = st.session_state.openai_api_key

if "poool_api_key" not in st.session_state:
    # add a link to 1_🚀_Setup.py
    st.error("Please set your Poool API key first.")

if "poool_api_key" not in st.session_state or "openai_api_key" not in st.session_state:
    st.page_link("sites/setup.py", label="Setup", icon="🚀")
    st.stop()

# Large text input for email signature
with st.form(key="email_signature"):
    signature = st.text_area("Paste your email signature here:", height=200)
    submit = st.form_submit_button("Extract Details")

# Extract details from email signature if form is submitted
if submit:
    with st.spinner("Extracting details..."):
        extracted_details = extract_details(signature)
        # convert str extracted details to json
        extracted_details = json.loads(extracted_details)
        # convert json extracted details to model
        st.session_state["data"]["company"] = Company.model_validate(extracted_details["company"])
        st.session_state["data"]["person"] = Person.model_validate(extracted_details["person"])
    st.success("Details extracted successfully.")
    
if "company" in st.session_state["data"]:
    expander = st.expander("Extracted Details")
    expander.write("#### Company")
    expander.write(st.session_state["data"]["company"].model_dump(exclude_none=True))
    expander.write("#### Person")
    expander.write(st.session_state["data"]["person"].model_dump(exclude_none=True))

    if st.button("Send Details to Poool"):
        # send company details to Poool
        json_data = {}
        json_data["data"] = st.session_state["data"]["company"].model_dump(exclude_none=True)
        response = create_company(st.session_state.poool_api_key, json_data)
        if response.status_code == 200:
            # save company id
            st.session_state["data"]["company"].company_id = response.json()["data"]["id"]
            st.session_state["data"]["person"].company_id = response.json()["data"]["id"]

            # send person details to Poool
            json_data = {}
            json_data["data"] = st.session_state["data"]["person"].model_dump(exclude_none=True)
            response = create_person(st.session_state.poool_api_key, json_data)
            if response.status_code == 200:
                st.success("Details sent to Poool successfully.")
            else:
                st.error("Error sending details to Poool.")
                st.write(response.json())
                st.write(response.request.__dict__)
        else:
            st.error("Error sending details to Poool.")
            st.write(response.json())
            st.write(response.request.__dict__)
