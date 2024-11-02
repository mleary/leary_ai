import os
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

from utils.llm_helpers import setup_azure_openai_client, setup_anthropic_client
from config import CHAT_MATT_PROMPT, CHAT_USER_PROMPT

# Load environment variables from .env file
load_dotenv()


# Constants
MODEL_PROVIDERS = ["Azure OpenAI", 'Anthropic']
AZURE_OPENAI_MODELS = ["gpt-4o-mini", "gpt-4o"]
ANTHROPIC_MODELS = ["claude-3-5-sonnet-20240620", "claude-3-haiku-20240307"]
GREETING = f"Hi {st.session_state['username'].capitalize()}, how can I help you today?"

def initialize_session_state():
    """
    Initialize session state variables.
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": GREETING}]
    if "model_name" not in st.session_state:
        st.session_state["model_name"] = AZURE_OPENAI_MODELS[0]

def set_system_prompt():
    """
    Set the system prompt based on the user's role.
    """
    if st.session_state["username"] == "matt":
        return CHAT_MATT_PROMPT
    else:
        return CHAT_USER_PROMPT

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
    elif model_provider == "Anthropic":
        model_name = st.sidebar.selectbox("Model Name", ANTHROPIC_MODELS, key="anthropic_model_name")
        st.session_state.model_name = model_name

    st.sidebar.markdown("---")  # Add a line at the end


def render():
    st.header("Chat")
    render_sidebar()
    initialize_session_state()
    system_prompt = set_system_prompt()
    client = setup_azure_openai_client()
    client_claude = setup_anthropic_client

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Input for new messages
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": system_prompt}) 
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        if st.session_state.model_provider == "Azure OpenAI":
            response = client.chat.completions.create(model=st.session_state.model_name, messages=st.session_state.messages)
        elif st.session_state.model_provider == "Anthropic":
            response = client_claude.messages.create(model=st.session_state.model_name,
            messages=[{"role": m["role"], "content": m["content"]}for m in st.session_state.messages]
            )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
     
    # Button to clear chat history
    if st.button("Clear Chat History"):

        st.session_state["messages"] = [{"role": "system", "content": GREETING}]
        st.rerun()
        


