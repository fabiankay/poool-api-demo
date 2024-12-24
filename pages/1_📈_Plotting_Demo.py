import streamlit as st
import openai
import requests

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key'

# Function to extract details using OpenAI
def extract_details(signature):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Extract the company and person details from the following email signature:\n\n{signature}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlit page
st.title("📈 Plotting Demo")
st.header("Email Signature Extractor")

# Large text input for email signature
signature = st.text_area("Paste your email signature here:", height=200)

if st.button("Extract Details"):
    if signature:
        details = extract_details(signature)
        st.subheader("Extracted Details")
        company = st.text_input("Company", value=details.split('\n')[0])
        person = st.text_input("Person", value=details.split('\n')[1])
        
        if st.button("Send to API"):
            api_endpoint = "https://your-api-endpoint.com"
            data = {"company": company, "person": person}
            response = requests.post(api_endpoint, json=data)
            if response.status_code == 200:
                st.success("Details sent successfully!")
            else:
                st.error("Failed to send details.")
    else:
        st.error("Please paste an email signature.")