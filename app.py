from openai import OpenAI
import streamlit as st
from sections import chat, calendar, about


# Header with page selection
st.set_page_config(page_title="learyAI", layout="wide")
st.title("learyAI")
st.caption("🚀 A personal family chatbot powered by AI")

# Page selection
page = st.selectbox("Select a page", ["Chat", "Calendar", "About"], index=0)

# Page content
if page == "Chat":
    chat.render()
elif page == "Calendar":
    calendar.render()
elif page == "About":
    about.render()


# Common sidebar content
with st.sidebar:
    st.write("Powered by Python, LLMs, and ☕")