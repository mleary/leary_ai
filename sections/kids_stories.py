import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def openai_story(system_prompt, user_prompt):
    """
    Generates a response by having a chat conversation with the GPT-4o model.

    Args:
        system_prompt (str): The initial prompt for the system.
        user_prompt (str): The user's input prompt.

    Returns:
        str: The generated response from the GPT-4o model.
    """

    load_dotenv()
    
    # Set up the Azure OpenAI client
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
        api_version="2024-07-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"))

    completion = client.chat.completions.create(
        model=st.session_state.model_name,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}])

    response = completion.choices[0].message.content
    return response



def render():
    st.header("📖 Story Generator")

    # Sidebar content for Chat page
    with st.sidebar:
        st.header("Story Settings")  
        if "system_prompt" not in st.session_state:
            st.session_state.system_prompt = "test"
            system_prompt = st.text_input("Enter a system prompt for the story:", value=st.session_state.system_prompt)
            st.session_state.system_prompt = system_prompt
        
        model_provider = st.selectbox("Select Model Provider", ["OpenAI"])#["OpenAI", "Anthropic"])

        if model_provider == "OpenAI":
            model_name = st.selectbox("Model Name", ["gpt-4o-mini", "gpt-4o"])
            st.session_state.model_name = model_name

    # Create a dropdown selection
    option = st.selectbox(
        'What do you want to do?',
        ('Write a story', 'Make an image'))

    user_input = st.text_input("Enter some text")

    # Create a button
    if st.button('Create'):
        # Print request & create a placeholder
        placeholder = st.empty()
        placeholder.text('Creating a story based on your input...')
        st.markdown('---')

        # Update the placeholder with a the result
        result = openai_story(st.session_state.system_prompt, user_input)
        placeholder.text('Creating an audio output of your story.')
        st.markdown(result)
        #text_to_audio(result)
        # Create a button
    
    # if st.button('Play Audio'):
    #     # Embed the audio file in the app
    #     st.audio('./audio.wav', format='audio/wav')
    
    # placeholder.text('Audio file created, all items completed!')


