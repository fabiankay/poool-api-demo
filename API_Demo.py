import streamlit as st
from src.components import sidebar

sidebar.show_sidebar()

# define navigation
home = st.Page("sites/home.py", title="Home", icon="🏠", default=True)
setup = st.Page("sites/setup.py", title="Setup", icon="🚀")
signature = st.Page("sites/signature_reader.py", title="Signature Reader", icon="✏️")
clustering = st.Page("sites/clustering.py", title="Clustering", icon="🔍")

pg = st.navigation({
    "Basics": [home, setup],
    "Examples": [signature, clustering]
})

pg.run()
