import streamlit as st
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API keys from environment variables
OPENAI_KEY = os.getenv("OPENAI_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY")

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
        # else:
        #     model_name = st.selectbox("Model Name", ["claude-3-5-sonnet-20240620", "claude-3-haiku-20240307"])

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if model_provider == "OpenAI":
            client = OpenAI(api_key=OPENAI_KEY)
            response = client.chat.completions.create(model=model_name, messages=st.session_state.messages)
            msg = response.choices[0].message.content
        # else:
        #     client = Anthropic(api_key=ANTHROPIC_KEY)
        #     response = client.messages.create(model=model_name, messages=st.session_state.messages, max_tokens=450)
        #     msg = response.completion

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)