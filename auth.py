# auth.py
import streamlit as st
import bcrypt
from database import register_user, get_user

def register_user_interface():
    st.subheader("Registrieren Sie sich")
    new_username = st.text_input("Benutzername", key="register_user")
    new_email = st.text_input("Email", key="register_email")
    new_name = st.text_input("Name", key="register_name")
    new_password = st.text_input("Passwort", type="password", key="register_password")
    confirm_password = st.text_input("Passwort bestätigen", type="password", key="register_confirm_password")
    
    if st.button("Registrieren"):
        if new_password == confirm_password:
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            try:
                register_user(new_username, hashed_password, new_email, new_name)
                st.success("Registrierung erfolgreich")
            except Exception as e:
                st.error(f"Fehler bei der Registrierung: {e}")
        else:
            st.error("Passwörter stimmen nicht überein")

def login_user_interface():
    st.subheader("Anmelden")
    username = st.text_input("Benutzername", key="login_user")
    password = st.text_input("Passwort", type="password", key="login_password")
    
    if st.button("Anmelden"):
        user = get_user(username)
        if user and bcrypt.checkpw(password.encode(), user[2].encode()):
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.username = username
            st.session_state.name = user[4]
            st.success("Anmeldung erfolgreich")
            st.experimental_rerun()
        else:
            st.error("Benutzername oder Passwort ist falsch")
