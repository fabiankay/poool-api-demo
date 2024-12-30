import streamlit as st
import openai

from src.helpers.open_api import extract_details
from src.helpers.poool_api import create_company, create_person, get_companies, find_similar_companies
from src.models.company import Company, Person
from src.components.company_selectbox import company_selectbox

st.write("# Example 1: Get Contact from Mail Signature! ✏️")
st.write("This example demonstrates how to extract details from an email signature using OpenAI. Copy and paste an email signature in the text area below and click the 'Extract Details' button to get the extracted details.")

# Initialize session state data
if "data" not in st.session_state:
    st.session_state["data"] = {}

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

# @todo: Check if needed or good place
if "companies" not in st.session_state["data"] or len(st.session_state["data"]["companies"]) == 0:
    companies = get_companies(st.session_state.poool_api_key)

# Large text input for email signature
with st.form(key="email_signature"):
    signature = st.text_area("Paste your email signature here:", height=200)
    submit = st.form_submit_button("Extract Details")

# Extract details from email signature if form is submitted
if submit:
    with st.spinner("Extracting details..."):
        company, person = extract_details(signature)
        st.session_state["data"]["company"] = company
        st.session_state["data"]["person"] = person
    st.success("Details extracted successfully.")
    
if "company" in st.session_state["data"]:
    # two columns for company and person details
    col1, col2 = st.columns(2)

    with col1:
        expander = st.expander("Extracted Details")
        expander.write("#### Company")
        expander.write(st.session_state["data"]["company"].model_dump(exclude_none=True))
        expander.write("#### Person")
        expander.write(st.session_state["data"]["person"].model_dump(exclude_none=True))

        if st.button("Send Details to Poool", key="send_details"):
            # send company details to Poool
            response = create_company(st.session_state["data"]["company"], st.session_state.poool_api_key)
            if response.status_code == 200:
                # save company id
                st.session_state["data"]["company"].id = response.json()["data"]["id"]
                st.session_state["data"]["person"].company_id = response.json()["data"]["id"]

                # send person details to Poool
                response = create_person(st.session_state["data"]["person"], st.session_state.poool_api_key)
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

    with col2:
        # look for similar companies in Poool
        similar_companies = find_similar_companies(st.session_state["data"]["companies"], st.session_state["data"]["company"].name)
        company_dict = {company.name: company.id for company in similar_companies if company.name and company.id}

        if len(similar_companies) > 0:
            st.write("#### We found similar companies in Poool")
            st.write("If you think this is the same company, you can send the details to Poool.")
            # show similar companies in selectbox
            company_id = company_selectbox(similar_companies)
        
            if st.button("Add person to selected company", key="send_similar_details"):
                st.session_state["data"]["company"].id = company_id
                st.session_state["data"]["person"].company_id = company_id
                response = create_person(st.session_state["data"]["person"], st.session_state.poool_api_key)
                
                if response.status_code == 200:
                    st.success("Details sent to Poool successfully.")
                else:
                    st.error("Error sending details to Poool.")
                    st.write(response.json())
                    st.write(response.request.__dict__)
