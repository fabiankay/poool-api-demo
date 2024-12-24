import streamlit as st
from src.components import sidebar

st.set_page_config(
    page_title="Poool API Demo",
    page_icon="👋",
    layout="centered",
    initial_sidebar_state="expanded",
)

sidebar.show_sidebar()

st.write("# Welcome to Poool API! 👋")

st.markdown(
    """
    This is a demo of the Poool API. You can use this app to explore the API and see how it works.
    We have provided a few examples for you to explore our API and get you started.

    ### Getting Started
    To get started, you will need an API key.
    You can get your API key from the settings by signing up to your account at [Poool](https://app.poool.cc/).

    """)

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