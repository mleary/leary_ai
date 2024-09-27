import streamlit_authenticator as stauth

# List of plain text passwords
passwords = [''] # insert password here

# Hash the passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# Print the hashed passwords
print(hashed_passwords)