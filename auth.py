# auth.py
import streamlit as st
import sqlite3
import bcrypt

def register_user_interface():
    st.subheader("Registrieren Sie sich")
    username = st.text_input("Benutzername", key="register_user")
    email = st.text_input("Email", key="register_email")
    name = st.text_input("Name", key="register_name")
    password = st.text_input("Passwort", type="password", key="register_password")
    confirm_password = st.text_input("Passwort bestätigen", type="password", key="register_confirm_password")
    
    if st.button("Registrieren"):
        if password == confirm_password:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            register_user(username, hashed_password, email, name)
            st.success("Registrierung erfolgreich")
        else:
            st.error("Passwörter stimmen nicht überein")

def register_user(username, password, email, name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (username, password, email, name)
        VALUES (?, ?, ?, ?)
    ''', (username, password, email, name))
    conn.commit()
    conn.close()

def login_user_interface():
    st.subheader("Login")
    username = st.text_input("Benutzername", key="login_user")
    password = st.text_input("Passwort", type="password", key="login_password")

    if st.button("Login"):
        user = get_user(username)
        if user and bcrypt.checkpw(password.encode(), user[2].encode()):
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.success("Login erfolgreich")
        else:
            st.error("Benutzername/Passwort ist inkorrekt")

def get_user(username):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    user = c.fetchone()
    conn.close()
    return user

def forgot_password_interface():
    st.subheader("Passwort vergessen")
    email = st.text_input("E-Mail-Adresse", key="forgot_email")

    if st.button("Passwort zurücksetzen"):
        user = get_user_by_email(email)
        if user:
            new_password = reset_password(user[0])
            st.write(f"Ihr neues Passwort lautet: {new_password}")
            st.success("Ein neues Passwort wurde an Ihre E-Mail-Adresse gesendet.")
        else:
            st.error("E-Mail-Adresse nicht gefunden")

def get_user_by_email(email):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user

def reset_password(user_id):
    new_password = "newpassword123"  # Hier können Sie ein zufälliges Passwort generieren
    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
    conn.commit()
    conn.close()
    return new_password
