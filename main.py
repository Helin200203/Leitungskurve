# main.py
import streamlit as st
from person import Person
from PIL import Image
from ekgdata import EKGDaten
import plotly.graph_objects as go
from auth import register_user_interface, login_user_interface
from database import init_db, get_user, get_all_users, get_all_meals, get_all_weights, get_all_bmi
from meals_sport import track_meals_sports
import pandas as pd
import plotly.express as px
import json
import os
import sqlite3
from language import languages
from bmi_nutrition import display_bmi_nutrition_section

# Initialisiere die Datenbank
init_db()

# Sprachumschaltung
if 'language' not in st.session_state:
    st.session_state.language = 'Deutsch'

def set_language():
    st.session_state.language = st.sidebar.radio("Sprache / Language", options=['Deutsch', 'English'])

set_language()
language = st.session_state.language
lang = languages[language]

st.sidebar.title(lang['welcome'])
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'gewicht': 0.0,
        'groesse': 0.0,
        'geschlecht': lang['male'],
        'alter': 0,
        'aktivitaetslevel': lang['activity_levels'][0],
        'bmi': 0.0,
        'kalorienbedarf': 0.0,
        'meals': [],
        'workouts': []
    }

if 'reset_password_flag' not in st.session_state:
    st.session_state.reset_password_flag = False

# Login oder Registrierung
if not st.session_state.logged_in:
    st.sidebar.title(lang['welcome'])
    option = st.sidebar.radio(lang['login_register'], [lang['login'], lang['register'], lang['forgot_password']])

    if option == lang['login']:
        login_user_interface()
        
    elif option == lang['register']:
        register_user_interface()

if st.session_state.logged_in:
    user_data = st.session_state.user_data

    # Haupt-Tabs für verschiedene Bereiche
    tabs = st.tabs([lang['ekg_data'], lang['bmi_nutrition'], lang['track_meals_sports'], lang['ki_features'], lang['db_management']])

    with tabs[0]:  # EKG-Daten Bereich
        # Laden der Personendaten und Erstellen der Namensliste
        personen_daten = Person.lade_personen_daten() 
        personen_namensliste = Person.get_personen_liste(personen_daten)

        # Session State wird leer angelegt, solange er noch nicht existiert
        if 'aktueller_benutzer' not in st.session_state:
            st.session_state.aktueller_benutzer = 'None'

        st.write("# EKG APP")
        st.write(f"### {lang['select_person']}")

        st.session_state.aktueller_benutzer = st.selectbox(
            lang['select_person'],
            options=personen_namensliste, key="sbVersuchsperson")

        # Finden der Person - den String haben wir im Session state
        aktuelle_person = Person.finde_personen_daten_nach_name(st.session_state.aktueller_benutzer)
        aktuelle_person_obj = Person(aktuelle_person)  # Erstellen eines Person-Objekts aus dem Dictionary
        person_ekg_liste = Person.ekgs_von_person(personen_daten, aktuelle_person_obj.id)  # Erstellen einer Liste von EKGs der gewählten Person

        bild = Image.open(aktuelle_person_obj.bild_pfad)  # Bild laden und Auslesen des Pfades aus dem zurückgegebenen Dictionary

        # Bild und Informationen nebeneinander anzeigen
        links, spalte1, mitte, spalte2 = st.columns([10, 1, 10, 20])
        with spalte1:
            st.image(bild, width=140)
        with spalte2:
            st.write(f'**{lang["gender"]}:**', aktuelle_person_obj.vorname)
            st.write(f'**{lang["gender"]}:**', aktuelle_person_obj.nachname)
            st.write(f'**{lang["age"]}:**', aktuelle_person_obj.alter)
            st.write(f'**Max HR:**', aktuelle_person_obj.max_hr_bpm)

        st.session_state.aktueller_benutzer = st.selectbox(
            lang['select_person'],
            options=person_ekg_liste, key="sbEKGliste")

        st.write(f"{lang['ekg_data']}: ", st.session_state.aktueller_benutzer, "von:", aktuelle_person_obj.vorname, aktuelle_person_obj.nachname)

        try:
            ekg = EKGDaten(aktuelle_person_obj.id, st.session_state.aktueller_benutzer)
            ekg.finde_spitzen(340, 4)
            hr = ekg.schätze_hr()
        except:
            st.write(lang['no_data'])

        # Tab-Elemente für die EKG-Daten
        tab1, tab2 = st.tabs([lang['data'], lang['graph']])

        try:
            with tab1:
                st.write(f"{lang['ekg_data']}: {st.session_state.aktueller_benutzer}")
                st.write('Datum:', ekg.datum)
                st.write(f"{lang['average_heart_rate']}: ", int(hr.mean()))

            with tab2:
                fig = go.Figure(data=go.Scatter(x=hr.index/1000, y=hr), layout=go.Layout(title="Herzfrequenz", xaxis_title="Zeit in s", yaxis_title="Herzfrequenz in bpm"))
                fig.update_layout(
                    xaxis=dict(
                        rangeslider=dict(
                            visible=True
                        ),
                        type="linear"
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
        except:
            st.write(lang['no_data'])
            
    with tabs[1]:  # BMI & Ernährung Bereich
        display_bmi_nutrition_section(user_data)
            
    with tabs[2]:  # Mahlzeiten & Sport Bereich
        track_meals_sports(st.session_state.user_id, user_data)

    with tabs[3]:  # KI-Funktionalitäten Bereich
        st.write(f"# {lang['ki_features']}")
        st.write(lang['ki_description'])

    with tabs[4]:  # Datenbank-Verwaltung Bereich
        st.write(f"# {lang['db_management']}")
        
        st.subheader(lang['user_management'])
        username = st.text_input(lang['show_user'])
        if st.button(lang['show_user']):
            user = get_user(username)
            if user:
                st.write(f"ID: {user[0]}, Benutzername: {user[1]}, E-Mail: {user[3]}, Name: {user[4]}")
            else:
                st.write(lang['user_not_found'])

        st.subheader(lang['clean_data'])
        if st.button(lang['delete_all_data']):
            if st.button(lang['confirm']):
                os.remove('data.db')
                init_db()
                st.success(lang['success_delete'])

        st.subheader(lang['export_data'])
        if st.button(lang['export_data']):
            data = {
                'users': get_all_users(),
                'meals': get_all_meals(),
                'weights': get_all_weights(),
                'bmi': get_all_bmi()
            }
            with open('data_export.json', 'w') as f:
                json.dump(data, f)
            st.success(lang['export_success'])

        st.subheader(lang['backup_restore'])
        if st.button(lang['create_backup']):
            conn = sqlite3.connect('data.db')
            with open('backup.db', 'w') as f:
                for line in conn.iterdump():
                    f.write(f'{line}\n')
            st.success(lang['backup_success'])

        uploaded_file = st.file_uploader(lang['upload_backup'], type=["db"])
        if uploaded_file is not None:
            with open('data.db', 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.success(lang['restore_success'])
