import streamlit as st
import pandas as pd
import os

# File to save responses
CSV_FILE = "responses.csv"

# Load existing responses
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["Grade", "Favorite Color", "Favorite Ice Cream", "Favorite Sport"])

# Function to save responses
def save_response(grade, color, ice_cream, sport):
    new_response = pd.DataFrame({
        "Grade": [grade],
        "Favorite Color": [color],
        "Favorite Ice Cream": [ice_cream],
        "Favorite Sport": [sport]
    })
    updated_df = pd.concat([df, new_response], ignore_index=True)
    updated_df.to_csv(CSV_FILE, index=False)

def render():
    # Streamlit page
    st.title("Favorite Things Survey")

    # Grade selection
    grade = st.selectbox("Select your grade", ["K", "1", "2", "3", "4", "5"])

    # Favorite color
    colors = df["Favorite Color"].unique().tolist()
    color = st.selectbox("Select your favorite color", colors)
    new_color = st.text_input("Or add a new favorite color")
    if new_color:
        color = new_color

    # Favorite ice cream flavor
    ice_creams = df["Favorite Ice Cream"].unique().tolist()
    ice_cream = st.selectbox("Select your favorite ice cream flavor", ice_creams)
    new_ice_cream = st.text_input("Or add a new favorite ice cream flavor")
    if new_ice_cream:
        ice_cream = new_ice_cream

    # Favorite sport
    sports = df["Favorite Sport"].unique().tolist()
    sport = st.selectbox("Select your favorite sport", sports)
    new_sport = st.text_input("Or add a new favorite sport")
    if new_sport:
        sport = new_sport

    # Submit button
    if st.button("Submit"):
        save_response(grade, color, ice_cream, sport)
        st.success("Response saved!")

    # Display existing responses
    st.write("Existing Responses")
    st.dataframe(df)