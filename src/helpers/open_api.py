import json
from requests import get
import openai
import streamlit as st

from src.models.company import Company, Person

def validate_api_key(api_key: str) -> None:
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
def extract_details(signature: str) -> tuple[Company, Person]:
    client = openai.OpenAI(api_key=st.session_state.openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "developer", "content": f"You are a company secretary that only speaks JSON. Do not generate output that isn't in properly formated JSON. You will be given copies of unstructured E-Mail Signatures that contain information about the company and person sending the Mail."},
            {"role": "developer", "content": f"Please extract the company in the following syntax to be handled by an API: {Company.model_json_schema()}"},
            {"role": "developer", "content": f"Please extract the person in the following syntax to be handled by an API: {Person.model_json_schema()}"},
            {"role": "developer", "content": f"Ignore any other information in the signature - only extract the company and person details." },
            {"role": "developer", "content": f"You must adhere to all specifications from the pydantic model description. For the final output only keep the initial label and the value property for every property. Skip the first level if called 'properties'. If not given explicitly - use default values." },
            {"role": "developer", "content": "Return the extracted details in the following format: {company: Company Details, person: Person Details}" },
            {"role": "user", "content": signature}
        ]
    )

    result = json.loads(response.choices[0].message.content)
    company = Company.model_validate(result["company"])
    person = Person.model_validate(result["person"])
    return company, person