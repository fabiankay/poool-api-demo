import streamlit as st

@st.fragment
def show_congifuration():
    st.header('Setup Status:')
    if "poool_api_key" in st.session_state:
        st.write("✅ Poool API Key Verified")
    else:
        st.write("❌ Poool API Key Missing")
    if "openai_api_key" in st.session_state:
        st.write("✅ Open AI Key Verified")
    else:
        st.write("❌ Open AI Key Missing")
    if "prism_username" in st.session_state and "prism_password" in st.session_state:
        st.write("✅ Database Connection Verified")
    else:
        st.write("❌ Database Connection Missing")
    st.write("---")


def show_sidebar():
    with st.sidebar:
        # Load & show logo image
        logo_path = "assets/image_logo.png"
        st.logo(logo_path, size="large", link=None, icon_image=None)

        st.write(st.session_state)
        
        show_congifuration()
