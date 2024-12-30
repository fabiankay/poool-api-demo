from typing import List
from difflib import get_close_matches
from requests import get, post, Response
import streamlit as st

from src.models.company import Company, Person

def validate_api_key(api_key: str) -> None:
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
    

def create_company(company_data: Company, api_key: str) -> Response:
    api_endpoint = "https://app.poool.cc/api/2/companies"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    json_data = {}
    json_data["data"] = company_data.model_dump(exclude_none=True)
    try:
        response = post(api_endpoint, headers=headers, json=json_data)
        return response
    except Exception as e:
        st.error("Error creating company in Poool.")
        st.error(e)
        return response
    

def create_person(person_data: Person, api_key: str) -> Response:
    api_endpoint = "https://app.poool.cc/api/2/persons"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    json_data = {}
    json_data["data"] = person_data.model_dump(exclude_none=True)
    try:
        response = post(api_endpoint, headers=headers, json=json_data)
        return response
    except Exception as e:
        st.error("Error creating person in Poool.")
        st.error(e)
        return response
    

@st.cache_data
def get_companies(api_key: str) -> List[Company]:
    api_endpoint = "https://app.poool.cc/api/2/companies"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    # get companies from Poool over multiple pages
    companies = []
    try:
        response = get(api_endpoint, headers=headers)
        if response.status_code == 200:
            companies.extend(response.json()["data"])
            while response.json()["links"]["next"]:
                response = get(response.json()["links"]["next"], headers=headers)
                companies.extend(response.json()["data"])
        return [Company.model_validate(company) for company in companies]
    except Exception as e:
        st.error("Error getting companies from Poool.")
        st.error(e)
        return companies
    

def find_similar_companies(companies: List[Company], search_name: str, cutoff: float = 0.8) -> List[Company]:
    # Extract company names
    company_names = [company.name for company in companies if company.name]
    
    # Find close matches
    similar_names = get_close_matches(search_name, company_names, n=3, cutoff=cutoff)
    
    # Filter companies with similar names
    similar_companies = [company for company in companies if company.name in similar_names]
    
    return similar_companies

