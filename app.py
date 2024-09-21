import streamlit as st
import streamlit_authenticator as stauth

from openai import OpenAI
from auth import config

from sections import home, chat, calendar, kids_stories, kids_images

##########################################################
# Set page configuration (needs to be first streamlit call)
##########################################################

st.set_page_config(page_title="learyAI", layout="wide")

##########################################################
# Authentication
##########################################################

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login(location='main')

##########################################################
# App - If successful login, proceed to page selection
##########################################################
if st.session_state['authentication_status']:
    authenticator.logout()

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Home", "Chat", "Calendar", "Create a story!", "Create an image!"], index=0)

    # Page content
    if page == "Home":
        home.render()
    elif page == "Chat":
        chat.render()
    elif page == "Calendar":
        calendar.render()
    elif page == "Create a story!":
        kids_stories.render()
    elif page == "Create an image!":
        kids_images.render()

    # Common sidebar content
    with st.sidebar:
        st.write("Powered by Python, LLMs, and ☕")

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')

elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')
    

    