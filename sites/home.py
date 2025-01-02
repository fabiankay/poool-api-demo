import streamlit as st

st.write("# Welcome to Poool API! 👋")

st.markdown(
    """
    This is a demo of the Poool API. You can use this app to explore the API and see how it works.
    We have provided a few examples for you to explore our API and get you started.

    ### Getting Started
    To get started, you will need an API key.
    You can get your API key from the settings by signing up to your account at [Poool](https://app.poool.cc/).
    Depending on the example you want to run, you may also need an OpenAI API key or access to Poool Prism.

    > **Note:** You will need to set your API keys in the setup page before running any of the examples.
    """)

st.page_link("sites/setup.py", label="Setup", icon="🚀")

st.markdown(
    """
    **Missing a key?** Contact us at [support@poool.cc](mailto:support@poool.cc) to get one.

    ### Examples
    """
)

st.markdown(
    """
    **Example #1: Signature Reader**
    
    This example demonstrates how to extract details from an email signature using OpenAI. 
    Copy and paste an email signature in the text area below and click the 'Extract Details' button to get the extracted details.
    """
)

st.page_link("sites/signature_reader.py", label="Signature Reader", icon="✏️")

st.markdown(
    """
    **Example #2: Clustering**
   
    In this example, we will use the Poools Prism database to run a clustering algorithm on clients.
    This will help us identify different segments of clients based on their behavior. Results will be sent to Poool as Tags for further analysis.
    """
)
st.page_link("sites/clustering.py", label="Clustering", icon="🔍")

st.markdown("""
    ### Support
    Please refer to the [documentation](https://app.poool.cc/api/docs) for more information on how to use the API.
    If you have any questions or need help, please feel free to reach out to us at [support@poool.cc](mailto:support@poool.cc).

    #### Happy Exploring! 🚀
    """
)