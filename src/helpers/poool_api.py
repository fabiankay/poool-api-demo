from requests import get, post
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
    

def create_company(api_key, company_data):
    api_endpoint = "https://app.poool.cc/api/2/companies"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response = post(api_endpoint, headers=headers, json=company_data)
        return response
    except Exception as e:
        st.error("Error creating company in Poool.")
        st.error(e)
        return response
    

def create_person(api_key, person_data):
    api_endpoint = "https://app.poool.cc/api/2/persons"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response = post(api_endpoint, headers=headers, json=person_data)
        return response
    except Exception as e:
        st.error("Error creating person in Poool.")
        st.error(e)
        return response
    

def get_companies(api_key):
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
        return companies
    except Exception as e:
        st.error("Error getting companies from Poool.")
        st.error(e)
        return companies


    try:
        response = get(api_endpoint, headers=headers)
        return response
    except Exception as e:
        st.error("Error getting companies from Poool.")
        st.error(e)
        return response