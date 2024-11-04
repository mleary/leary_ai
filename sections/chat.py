import os
import time
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI
from anthropic import Anthropic
from utils.llm_helpers import setup_azure_openai_client, setup_anthropic_client
from config import CHAT_MATT_PROMPT, CHAT_AM_PROMPT, CHAT_USER_PROMPT

# Load environment variables from .env file
load_dotenv()

# Constants
MODEL_PROVIDERS = ["Azure OpenAI", 'Anthropic']
AZURE_OPENAI_MODELS = ["gpt-4o-mini", "gpt-4o"]
ANTHROPIC_MODELS = ["claude-3-haiku-20240307", "claude-3-5-sonnet-20241022"]

def initialize_session_state(GREETING):
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": GREETING}]
    if "model_name" not in st.session_state:
        st.session_state["model_name"] = AZURE_OPENAI_MODELS[0]

def set_system_prompt():
    """Set the system prompt based on the user's role."""
    if st.session_state["username"] == "matt":
        return CHAT_MATT_PROMPT
    if st.session_state["username"] == "am":
        return CHAT_AM_PROMPT
    else:
        return CHAT_USER_PROMPT

def set_greeting():
    return f"Hi {st.session_state['username'].capitalize()}, how can I help you today?"

def render_sidebar():
    """Render the sidebar content for the Chat page."""
    st.sidebar.header("Chat Settings")
    st.sidebar.markdown("---")
    model_provider = st.sidebar.selectbox("Select Model Provider", MODEL_PROVIDERS, key="model_provider")
    
    if model_provider == "Azure OpenAI":
        model_name = st.sidebar.selectbox("Model Name", AZURE_OPENAI_MODELS, key="aoai_model_name")
        st.session_state.model_name = model_name
    elif model_provider == "Anthropic":
        model_name = st.sidebar.selectbox("Model Name", ANTHROPIC_MODELS, key="anthropic_model_name")
        st.session_state.model_name = model_name
    st.sidebar.markdown("---")

def update_text_with_delay(message_placeholder, text):
    """Update text with a small delay to make streaming visible"""
    message_placeholder.markdown(text + "▌")
    time.sleep(0.01)  # Small delay to make streaming visible

def get_streaming_response(client, system_prompt, messages, message_placeholder):
    """Stream responses from either Azure OpenAI or Anthropic"""
    full_response = ""
    
    if st.session_state.model_provider == "Azure OpenAI":
        # Convert messages to format expected by Azure OpenAI
        azure_messages = []
        for msg in messages:
            # Skip the initial greeting message if it exists
            if msg["content"] == st.session_state.messages[0]["content"] and msg["role"] == "assistant":
                continue
            azure_messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add system message at the start
        messages_with_system_prompt = [{"role": "system", "content": system_prompt}] + azure_messages
        
        try:
            stream = client.chat.completions.create(
                model=st.session_state.model_name,
                messages=messages_with_system_prompt,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices and hasattr(chunk.choices[0], 'delta'):
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content is not None:
                        full_response += delta.content
                        update_text_with_delay(message_placeholder, full_response)
                        
        except Exception as e:
            print(f"Azure OpenAI Error: {str(e)}")
            print(f"Messages being sent: {messages_with_system_prompt}")
            raise e
    
    else:  # Anthropic
        anthropic_messages = []
        for msg in messages:
            if msg["role"] == "assistant":
                anthropic_messages.append({"role": "assistant", "content": msg["content"]})
            elif msg["role"] == "user":
                anthropic_messages.append({"role": "user", "content": msg["content"]})

        stream = client.messages.create(
            model=st.session_state.model_name,
            system=system_prompt,
            messages=anthropic_messages,
            max_tokens=2000,
            stream=True
        )
        
        for chunk in stream:
            if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'):
                if chunk.delta.text:
                    full_response += chunk.delta.text
                    update_text_with_delay(message_placeholder, full_response)
    
    # Final update without the cursor
    message_placeholder.markdown(full_response)
    return full_response
    

def render():
    st.header("Chat")
    render_sidebar()
    
    GREETING = set_greeting()
    initialize_session_state(GREETING)
    system_prompt = set_system_prompt()
    
    client = setup_azure_openai_client() if st.session_state.model_provider == "Azure OpenAI" else setup_anthropic_client()

    # Display chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Handle user input
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Create a placeholder for the assistant's response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_streaming_response(
                client, 
                system_prompt, 
                st.session_state.messages, 
                message_placeholder
            )
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Button to clear chat history
    if st.button("Clear Chat History"):
        st.session_state["messages"] = [{"role": "assistant", "content": GREETING}]
        st.rerun()