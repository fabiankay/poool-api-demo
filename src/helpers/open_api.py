from requests import get
import openai
import streamlit as st

def validate_api_key(api_key):
    client = openai.OpenAI(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ]
        )
    except openai.AuthenticationError:
        if "openai_api_key" in st.session_state:
            del st.session_state.openai_api_key
        st.error("Invalid API key.")
    
    st.session_state.openai_api_key = api_key
    st.rerun()


# Function to extract details using OpenAI
def extract_details(signature):
    client = openai.OpenAI(api_key=st.session_state.openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "developer", "content": f"You are a company secretary that only speaks JSON. Do not generate output that isn't in properly formated JSON. You will be given copies of unstructured E-Mail Signatures that contain information about the company and person sending the Mail. Please extract the company and person information in the following syntax to be handled by an API: name: <company_name> uid: <tax_id> management: <management> jurisdiction: <jurisdiction> commercial_register: <commercial_register> data_privacy_number: <data_privacy_number> addresses: [title: <title>, recipient_1: <recipient_1>, recipient_2: <recipient_2>, recipient_3: <recipient_3>, street_name: <street_name>, street_number: <street_number>, street_additional: <street_additional>, zip: <zip>, location: <location>, state: <state>] contacts: [title: phone-number|mail-adress|website, value: <value>]"},
            {"role": "user", "content": signature}
        ]
    )
    return response.choices[0].message.content