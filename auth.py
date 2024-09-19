import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Parse the environment variables
usernames = os.getenv('USERNAMES').split(',')
emails = os.getenv('EMAILS').split(',')
passwords = os.getenv('HASHED_PASSWORDS').split(',')

# Create the credentials dictionary
credentials = {
    'usernames': {
        username: {
            'email': email,
            'name': username,
            'failed_login_attempts': 3,
            'logged_in': False,
            'password': password
        }
        for username, email, password in zip(usernames, emails, passwords)
    }
}

# Create the config dictionary
config = {
    'credentials': credentials,
    'cookie': {
        'expiry_days': 30,
        'key': 'abcdef1234',
        'name': 'learyai'
    },
    'preauthorized': {
        'emails': ''
    }
}