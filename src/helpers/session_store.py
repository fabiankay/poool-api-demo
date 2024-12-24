import streamlit as st

def set_api_key( service_name, key, password=None):
    if service_name == 'poool':
        st.session_state['poool_api_key'] = key
    elif service_name == 'openai':
        st.session_state['openai_api_key'] = key
    elif service_name == 'poool_prism_db':
        st.session_state['poool_prism_db_user'] = key
        st.session_state['poool_prism_db_password'] = password
    else:
        raise ValueError("Invalid service name")

def remove_api_key(self, service_name):
    if service_name == 'poool':
        st.session_state['poool_api_key'] = None
    elif service_name == 'openai':
        st.session_state['openai_api_key'] = None
    elif service_name == 'poool_prism_db':
        st.session_state['poool_prism_db_user'] = None
        st.session_state['poool_prism_db_password'] = None
    else:
        raise ValueError("Invalid service name")
    
# @todo: Is needed?
def get_api_key(self, service_name):
    if service_name == 'poool':
        return st.session_state['poool_api_key']
    elif service_name == 'openai':
        return st.session_state['openai_api_key']
    elif service_name == 'poool_prism_db':
        return [
            st.session_state['poool_prism_db_user'],
            st.session_state['poool_prism_db_password']
        ]
    else:
        raise ValueError("Invalid service name")
