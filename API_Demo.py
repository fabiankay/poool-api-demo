import datetime
import streamlit as st

from src.components import sidebar
from src.helpers.poool_api import get_companies

# Initialize session state data
if "data" not in st.session_state:
    st.session_state["data"] = {}

# Initialize session state data
if "options" not in st.session_state:
    st.session_state["options"] = {}

if "features" not in st.session_state["options"]:
    st.session_state["options"]["features"] = ["Total revenue", "Total cost", "Total timetrack cost", "Total profit"]

if "timeframe" not in st.session_state["options"]:
    today = datetime.date.today()
    st.session_state["options"]["timeframe"] = [datetime.date(today.year - 1, 1, 1), datetime.date(today.year - 1, 12, 31)]

if "num_clusters" not in st.session_state["options"]:
    st.session_state["options"]["num_clusters"] = 3

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
