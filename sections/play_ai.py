import os
import random
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

from utils.llm_helpers import setup_azure_openai_client

# Load environment variables from .env file
load_dotenv()

SYSTEM_PROMPT = "You are playing this game with young children.  Only respond with appropriate language and content for a 6 year old. Do not use any language that resembles bad language such as 'shell yeah' or 'what the shell'."

def number_guessing_game():
    if 'target_number' not in st.session_state:
        st.session_state.target_number = random.randint(1, 10)
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    
    # Function to reset the game
    def reset_game():
        del st.session_state.target_number
        del st.session_state.attempts
        st.session_state.target_number = random.randint(1, 10)
        st.session_state.attempts = 0


    # Setup Azure OpenAI client    
    client = setup_azure_openai_client()
    
    # User inputs and buttons
    if st.button("Play Again"):
        reset_game()
    tone = st.text_input("What tone should I respond in?:")
    guess = st.number_input("Guess a number between 1 and 10:", min_value=1, max_value=100)
    
    if st.button("Make Guess"):
        st.session_state.attempts += 1
        if guess == st.session_state.target_number:
            prompt = f'You are playing a number guessing game with young children. Your opponent has guessed the right number {st.session_state.target_number} in {st.session_state.attempts} tries. Respond to tell them the guessed correctly, but do it in this style: {tone}. Include the correct answer and how many guesses it took them'

            response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}, {'role': "system", "content": SYSTEM_PROMPT}])
            
            st.success(response.choices[0].message.content)
            if st.button("Play Again"):
                del st.session_state.target_number
                del st.session_state.attempts
        elif guess < st.session_state.target_number:
            prompt = f'You are playing a number guessing game with young children. Your opponent has guessed the wrong number {guess} in {st.session_state.attempts} tries. Respond to tell them the guessed to low and the need to guess a higher number, but do it in this style: {tone}. Include how many guesses they have taken and their last guess.'

            response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}, {'role': "system", "content": SYSTEM_PROMPT}])
            st.warning(response.choices[0].message.content)
        else:
            prompt = f'You are playing a number guessing game with young children. Your opponent has guessed the wrong number {guess} in {st.session_state.attempts} tries. Respond to tell them the guessed to high and the need to guess a lower number, but do it in this style: {tone}. Include how many guesses they have taken and their last guess.'

            response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}, {'role': "system", "content": SYSTEM_PROMPT}])
            st.warning(response.choices[0].message.content)
            


def render():
    st.header("🎲 Want to play a guessing game with AI? 🤔")
    st.write("I'm thinking of a number between 1 and 10, can you guess it...")

    number_guessing_game()