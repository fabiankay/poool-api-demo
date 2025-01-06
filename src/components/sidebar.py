import streamlit as st
from src.helpers.poool_api import get_companies
from src.helpers.prism import create_clustering_df

@st.fragment
def show_configuration() -> None:
    st.header('Setup Status:')
    if "poool_api_key" in st.session_state:
        st.write("✅ Poool API Key Verified")
    else:
        st.write("❌ Poool API Key Missing")
    if "openai_api_key" in st.session_state:
        st.write("✅ Open AI Key Verified")
    else:
        st.write("❌ OpenAI Key Missing")
    if "prism_username" in st.session_state and "prism_password" in st.session_state:
        st.write("✅ Prism Connection Verified")
    else:
        st.write("❌ Prism Connection Missing")
    st.write("---")

@st.fragment
def show_options() -> None:
    st.header('Data Handling:')
    if "companies" in st.session_state["data"] and "poool_api_key" in st.session_state:
        reload_companies = st.button("📥 Reload Companies", key="reload_companies")
        if reload_companies:
            with st.spinner("Loading companies..."):
                st.session_state["data"]["companies"] = get_companies(st.session_state.poool_api_key)
    
    if "clustering_df" in st.session_state["data"]:
        reload_clustering_df = st.button("📥 Reload Clustering Data")
        if reload_clustering_df:
            with st.spinner("Loading clustering data..."):
                st.session_state["data"]["clustering_df"] = create_clustering_df(timeframe=st.session_state["options"]["timeframe"])
                   
    st.write("---")


def show_sidebar() -> None:
    with st.sidebar:
        # Load & show logo image
        logo_path = "assets/image_logo.png"
        st.logo(logo_path, size="large", link=None, icon_image=None)

        # st.write(st.session_state)
        
        show_configuration()

        # show_options()
