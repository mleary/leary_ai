import os
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()


# Constants
MODEL_PROVIDERS = ["Azure OpenAI"]
AZURE_OPENAI_MODELS = ["gpt-4o-mini", "gpt-4o"]


def initialize_session_state():
    """
    Initialize session state variables.
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    if "model_name" not in st.session_state:
        st.session_state["model_name"] = AZURE_OPENAI_MODELS[0]


def render_sidebar():
    """
    Render the sidebar content for the Chat page.
    """
    st.sidebar.header("Chat Settings")
    st.sidebar.markdown("---")  # Add a line after the header
    
    model_provider = st.sidebar.selectbox("Select Model Provider", MODEL_PROVIDERS, key="model_provider")
    
    if model_provider == "Azure OpenAI":
        model_name = st.sidebar.selectbox("Model Name", AZURE_OPENAI_MODELS, key="aoai_model_name")
        st.session_state.model_name = model_name

    st.sidebar.markdown("---")  # Add a line at the end



def setup_azure_openai_client():
    """
    Set up the Azure OpenAI client.

    Returns:
        AzureOpenAI: The Azure OpenAI client.
    """
    try:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
            api_version="2024-07-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        return client
    except Exception as e:
        st.error(f"An error occurred while setting up the Azure OpenAI client: {e}")
        return None


def render():
    st.header("Chat")
    render_sidebar()
    initialize_session_state()
    client = setup_azure_openai_client()

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Input for new messages
    if prompt := st.chat_input():

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model=st.session_state.model_name, messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
     
    # Button to clear chat history
    if st.button("Clear Chat History"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        st.rerun()
        


