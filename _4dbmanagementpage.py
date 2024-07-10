import streamlit as st
from database import get_user, get_all_users, get_all_meals, get_all_weights, get_all_bmi, init_db
import json
import os
import sqlite3
init_db()
def show_db_management_page():
    st.title("Datenbank-Verwaltung")
    
    st.subheader("Benutzerverwaltung")
    username = st.text_input("Benutzer anzeigen")
    if st.button("Benutzer anzeigen"):
        user = get_user(username)
        if user:
            st.write(f"ID: {user[0]}, Benutzername: {user[1]}, E-Mail: {user[3]}, Name: {user[4]}")
        else:
            st.write("Benutzer nicht gefunden")

    st.subheader("Daten löschen")
    if st.button("Alle Daten löschen"):
        if st.button("Bestätigen"):
            os.remove('data.db')
            init_db()
            st.success("Erfolgreich gelöscht")

    st.subheader("Daten exportieren")
    if st.button("Daten exportieren"):
        data = {
            'users': get_all_users(),
            'meals': get_all_meals(),
            'weights': get_all_weights(),
            'bmi': get_all_bmi()
        }
        with open('data_export.json', 'w') as f:
            json.dump(data, f)
        st.success("Export erfolgreich")

    st.subheader("Backup & Wiederherstellung")
    if st.button("Backup erstellen"):
        conn = sqlite3.connect('data.db')
        with open('backup.db', 'w') as f:
            for line in conn.iterdump():
                f.write(f'{line}\n')
        st.success("Backup erfolgreich")

    uploaded_file = st.file_uploader("Backup hochladen", type=["db"])
    if uploaded_file is not None:
        with open('data.db', 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success("Wiederherstellung erfolgreich")
