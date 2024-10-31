import streamlit as st
import streamlit_authenticator as stauth
from openai import OpenAI
from utils.auth import config
from sections import home, chat, calendar, kids_stories, kids_images, play_ai

####################################
# Constants & setup
####################################

PAGE_TITLE = "learyAI"
LAYOUT = "wide"
PAGE_ICON = ':rocket:'
NAVIGATION_TITLE = "Navigation"
PAGES = {
    "Home": home,
    "Chat": chat,
    "Calendar": calendar,
    "Create a story!": kids_stories,
    "Create an image!": kids_images,
    "Play a game with AI": play_ai
}

###################################
# helper function(s)
###################################

def render_page(page):
    """
    Render the selected page.

    Args:
        page (str): The name of the page to render.
    """
    try:
        PAGES[page].render()
    except KeyError:
        st.error(f"Page '{page}' not found.")
    except Exception as e:
        st.error(f"An error occurred while rendering the page: {e}")

###################################
# main function
###################################

def main():
    """
    Main function to run the Streamlit app.
    """
    # Set page configuration
    st.set_page_config(
        page_title=PAGE_TITLE, 
        layout=LAYOUT,
        page_icon=PAGE_ICON,
        menu_items={
        'About': 'https://github.com/mleary/leary_ai'
    })

    # Authentication
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    authenticator.login(location='main')

    # App - If successful login, proceed to page selection
    if st.session_state['authentication_status']:
        authenticator.logout()

        # Sidebar for navigation
        st.sidebar.title(NAVIGATION_TITLE)
        page = st.sidebar.selectbox("Select a page", list(PAGES.keys()), index=0)

        # Page content
        render_page(page)

        # Common sidebar content
        with st.sidebar:
            st.write("Powered by Python, LLMs, and ☕")

    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')

    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

if __name__ == "__main__":
    main()