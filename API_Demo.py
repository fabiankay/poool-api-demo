import streamlit as st
from requests import get

# Load the logo image
logo_path = "assets/image_logo.png"

# Display the logo
st.logo(logo_path, size="large", link=None, icon_image=None)  # Adjust the width as needed

st.set_page_config(
    page_title="Poool API Demo",
    page_icon="👋",
    layout="centered",
)

# if developer mode is enabled, display session state in the sidebar
st.sidebar.write("Session State")
st.sidebar.write(st.session_state)

st.write("# Welcome to Poool API! 👋")

st.markdown(
    """
    This is a demo of the Poool API. You can use this app to explore the API and see how it works.
    We have provided a few examples for you to explore our API and get you started.

    ### Getting Started
    To get started, you will need an API key.
    You can get your API key from the settings by signing up to your account at [Poool](https://app.poool.cc/).

    """)

# Form to enter API key and verify with server on https://app.poool.cc/api/2/hello_its_me
api_key = st.text_input("Enter your API key:", type="password")
if st.button("Verify API Key"):
    if api_key:
        # semd a request to the server to verify the API key
        # if the response is 200, then the API key is valid
        response = get("https://app.poool.cc/api/2/hello_its_me", headers={"Authorization": f"Bearer {api_key}"})
        if response.status_code == 200:
            # Save API key to session state
            st.session_state.api_key = api_key
            st.success("API key verified successfully!")
        else:
            if "api_key" in st.session_state:
                del st.session_state.api_key
            st.error("Invalid API key. Please try again.")
    else:
        st.write("Please enter your API key.")

st.markdown(
    """    
    **Not have an API key?** Contact us at [support@poool.cc](mailto:support@poool.cc) to get one.
    """
)

with st.expander("Additional access for Example #2"):
    st.write("""
            For *Example 2* you will also need access to [Poool Prism](https://academy.poool.cc/poool-prism/hwyKfRavBuU2jXpb7kJfDf) - our Data Platform.
    """)

st.markdown("""
    ### Examples
    - **Example #1:** [Get List of Articles](pages/1_.py)
    - **Example #2:** [Get Article Details](pages/2_.py)

    ### Support
    Please refer to the [documentation](https://app.poool.cc/api/docs) for more information on how to use the API.
    If you have any questions or need help, please feel free to reach out to us at [support@poool.cc](mailto:support@poool.cc).

    #### Happy Exploring! 🚀
    """
)