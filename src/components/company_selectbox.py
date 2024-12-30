from typing import List
import streamlit as st

from src.models.company import Company

# Fetch companies and create a select box
def company_selectbox(companies: List[Company]) -> int:    
    # Create a dictionary mapping company names to their IDs
    company_dict = {company.name: company.id for company in companies if company.name and company.id}
    
    # Create a select box for company names
    selected_company_name = st.selectbox("Select a company", list(company_dict.keys()))
    
    # Get the ID of the selected company
    selected_company_id = company_dict[selected_company_name]
    
    # st.write(f"Selected Company ID: {selected_company_id}")
    return selected_company_id