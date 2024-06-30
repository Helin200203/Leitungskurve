# auth.py
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import bcrypt

# Funktion zum Laden der Anmeldedaten
def load_credentials():
    with open('credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

# Funktion zum Speichern der Anmeldedaten
def save_credentials(credentials):
    with open('credentials.yaml', 'w') as file:
        yaml.dump(credentials, file)

def get_authenticator():
    config = load_credentials()
    authenticator = stauth.Authenticate(
        config['credentials'],
        'cookie_name', 
        'signature_key', 
        cookie_expiry_days=30
    )
    return authenticator, config

# Registrierung
def register_user():
    st.subheader("Registrieren Sie sich")
    new_username = st.text_input("Benutzername", key="register_user")
    new_email = st.text_input("Email", key="register_email")
    new_name = st.text_input("Name", key="register_name")
    new_password = st.text_input("Passwort", type="password", key="register_password")
    confirm_password = st.text_input("Passwort bestätigen", type="password", key="register_confirm_password")
    
    if st.button("Registrieren"):
        if new_password == confirm_password:
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            config = load_credentials()
            config['credentials']['usernames'][new_username] = {
                'email': new_email,
                'name': new_name,
                'password': hashed_password
            }
            save_credentials(config)
            st.success("Registrierung erfolgreich")
        else:
            st.error("Passwörter stimmen nicht überein")