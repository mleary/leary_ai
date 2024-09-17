import streamlit as st

def render():
    st.header("About")
    st.write("This is a personal family chatbot powered by AI. It uses OpenAI GPT-series models and Anthropics Claude.")

    # Sidebar content for About page
    with st.sidebar:
        st.header("About")
        st.write("This is a personal family chatbot powered by AI. I's a place to explore Gen AI capability and provide some fun tools for the family to use!")
