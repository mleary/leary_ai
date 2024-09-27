import os
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Constants
MODEL_PROVIDERS = ["OpenAI"]
OPENAI_MODELS = ["gpt-4o-mini", "gpt-4o"]


def initialize_session_state():
    """
    Initialize session state variables.
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    if "model_name" not in st.session_state:
        st.session_state["model_name"] = OPENAI_MODELS[0]


def render_sidebar():
    """
    Render the sidebar content for the Chat page.
    """
    st.sidebar.header("Chat Settings")
    model_provider = st.sidebar.selectbox("Select Model Provider", MODEL_PROVIDERS, key="model_provider")

    if model_provider == "OpenAI":
        model_name = st.sidebar.selectbox("Model Name", OPENAI_MODELS, key="openai_model_name")
        st.session_state.model_name = model_name
    # Future support for other model providers can be added here
    # elif model_provider == "Anthropic":
    #     model_name = st.sidebar.selectbox("Model Name", ANTHROPIC_MODELS, key="anthropic_model_name")
    #     st.session_state.model_name = model_name

def render():
    st.header("Chat")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # Sidebar content for Chat page
    with st.sidebar:
        st.header("Chat Settings")  
        model_provider = st.selectbox("Select Model Provider", ["OpenAI"])#["OpenAI", "Anthropic"])

        if model_provider == "OpenAI":
            model_name = st.selectbox("Model Name", ["gpt-4o-mini", "gpt-4o"])
            st.session_state.model_name = model_name
        # else:
        #     model_name = st.selectbox("Model Name", ["claude-3-5-sonnet-20240620", "claude-3-haiku-20240307"])

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if model_provider == "OpenAI":
            # Set up the Azure OpenAI client
            client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
                api_version="2024-07-01-preview",
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"))
            response = client.chat.completions.create(model=st.session_state.model_name,
                                                    messages=[{'role': 'user', 'content': prompt}])
            msg = response.choices[0].message.content
        # else:
        #     client = Anthropic(api_key=ANTHROPIC_KEY)
        #     response = client.messages.create(model=model_name, messages=st.session_state.messages, max_tokens=450)
        #     msg = response.completion

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)