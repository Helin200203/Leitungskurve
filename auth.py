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
            st.session_state.username = username
            st.success("Login erfolgreich")
        else:
            st.error("Benutzername/Passwort ist inkorrekt")

    if st.session_state.get('logged_in'):
        st.write("Eingeloggt als:", st.session_state.username)
        change_password_interface(st.session_state.user_id)
    elif st.session_state.get('reset_password_flag'):
        reset_password_interface(st.session_state.user_id)
    else:
        forgot_password_interface()

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
            st.session_state.reset_password_flag = True
            st.session_state.user_id = user[0]
            st.success("Bitte setzen Sie Ihr neues Passwort.")
        else:
            st.error("E-Mail-Adresse nicht gefunden")

def get_user_by_email(email):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user

def reset_password_interface(user_id):
    st.subheader("Neues Passwort setzen")
    new_password = st.text_input("Neues Passwort", type="password", key="new_password_reset")
    confirm_new_password = st.text_input("Neues Passwort bestätigen", type="password", key="confirm_new_password_reset")
    
    if st.button("Passwort setzen"):
        if new_password == confirm_new_password:
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            update_password(user_id, hashed_password)
            st.success("Passwort erfolgreich gesetzt. Bitte einloggen.")
            st.session_state.reset_password_flag = False
        else:
            st.error("Die neuen Passwörter stimmen nicht überein")

def change_password_interface(user_id):
    st.subheader("Passwort ändern")
    current_password = st.text_input("Aktuelles Passwort", type="password", key="current_password")
    new_password = st.text_input("Neues Passwort", type="password", key="new_password")
    confirm_new_password = st.text_input("Neues Passwort bestätigen", type="password", key="confirm_new_password")
    
    if st.button("Passwort ändern"):
        user = get_user_by_id(user_id)
        if user and bcrypt.checkpw(current_password.encode(), user[2].encode()):
            if new_password == confirm_new_password:
                hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                update_password(user_id, hashed_password)
                st.success("Passwort erfolgreich geändert")
            else:
                st.error("Die neuen Passwörter stimmen nicht überein")
        else:
            st.error("Aktuelles Passwort ist falsch")

def get_user_by_id(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_password(user_id, hashed_password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
    conn.commit()
    conn.close()

