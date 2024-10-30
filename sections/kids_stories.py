import os
import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv

from config import AZURE_API_VERSION

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
        api_version=AZURE_API_VERSION,
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
            st.session_state.system_prompt = "You are a creative author of children stories. You write stories for six year olds."
            system_prompt = st.text_input("Enter a system prompt for the story:", value=st.session_state.system_prompt)
            st.session_state.system_prompt = system_prompt
        
        model_provider = st.selectbox("Select Model Provider", ["OpenAI"])#["OpenAI", "Anthropic"])

        if model_provider == "OpenAI":
            model_name = st.selectbox("Model Name", ["gpt-4o-mini", "gpt-4o"])
            st.session_state.model_name = model_name

    # Create a dropdown selection
    # Create two columns
    col1, col2 = st.columns(2)

    # Place the dropdown selection in the first column
    with col1:
        length = st.selectbox(
            'How many paragraphs?', (3, 4, 5, 6))

    # Place the multiselect in the second column
    with col2:
        tone = st.multiselect(
            'What type of story?', ("Funny", "Mystery", "Adventure", "Silly"))

    user_input = st.text_input("Enter a story prompt here!")

    # Create a button
    if st.button('Create'):
        # Print request & create a placeholder
        placeholder = st.empty()
        placeholder.text('Creating a story based on your input...')
        st.markdown('---')

        # Update the placeholder with a the result
        details = f'The story should be approximately {length} paragraphs long and it is a {tone} story'
        prompt = st.session_state.system_prompt + details
        result = openai_story(st.session_state.system_prompt, prompt)
        placeholder.text('Creating an audio output of your story.')
        st.markdown(result)
        #text_to_audio(result)
        # Create a button
    
    # if st.button('Play Audio'):
    #     # Embed the audio file in the app
    #     st.audio('./audio.wav', format='audio/wav')
    
    # placeholder.text('Audio file created, all items completed!')


