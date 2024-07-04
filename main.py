# main.py
import streamlit as st
from person import Person
from PIL import Image
from ekgdata import EKGDaten
import plotly.graph_objects as go
from auth import register_user_interface, login_user_interface
from database import init_db, get_meals, get_weights, add_weight, add_bmi, get_bmi, get_user, get_all_users, get_all_meals, get_all_weights, get_all_bmi
from utils import berechne_bmi, berechne_kalorienbedarf, bmi_bereich
from meals_sport import track_meals_sports
import pandas as pd
import plotly.express as px
import json
import os
import sqlite3
# Initialisiere die Datenbank
init_db()

# Session State wird leer angelegt, solange er noch nicht existiert
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'gewicht': 0.0,
        'groesse': 0.0,
        'geschlecht': 'Männlich',
        'alter': 0,
        'aktivitaetslevel': 'Wenig aktiv',
        'bmi': 0.0,
        'kalorienbedarf': 0.0,
        'meals': [],
        'workouts': []
    }

# Login oder Registrierung
if not st.session_state.logged_in:
    st.sidebar.title("Willkommen")
    option = st.sidebar.radio("Login/Registrierung", ["Login", "Registrierung"])

    if option == "Login":
        login_user_interface()

    elif option == "Registrierung":
        register_user_interface()

if st.session_state.logged_in:
    user_data = st.session_state.user_data

    # Haupt-Tabs für verschiedene Bereiche
    tabs = st.tabs(["EKG-Daten", "BMI & Kalorienbedarf", "Mahlzeiten & Sport", "KI-Funktionalitäten", "Datenbank-Verwaltung"])

    with tabs[0]:  # EKG-Daten Bereich
        # Laden der Personendaten und Erstellen der Namensliste
        personen_daten = Person.lade_personen_daten() 
        personen_namensliste = Person.get_personen_liste(personen_daten)

        # Session State wird leer angelegt, solange er noch nicht existiert
        if 'aktueller_benutzer' not in st.session_state:
            st.session_state.aktueller_benutzer = 'None'

        st.write("# EKG APP")  # Eine Überschrift der ersten Ebene
        st.write("### Versuchsperson auswählen")  # Eine Überschrift der zweiten Ebene

        st.session_state.aktueller_benutzer = st.selectbox(
            'Versuchsperson',
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
            st.write('**Vorname:**', aktuelle_person_obj.vorname)
            st.write('**Nachname:**', aktuelle_person_obj.nachname)
            st.write('**Alter:**', aktuelle_person_obj.alter)
            st.write('**Max HR:**', aktuelle_person_obj.max_hr_bpm)

        st.session_state.aktueller_benutzer = st.selectbox(
            'EKG-Daten auswählen:',
            options=person_ekg_liste, key="sbEKGliste")

        st.write("Ausgewähltes EKG: ", st.session_state.aktueller_benutzer, "von:", aktuelle_person_obj.vorname, aktuelle_person_obj.nachname)

        try:
            ekg = EKGDaten(aktuelle_person_obj.id, st.session_state.aktueller_benutzer)
            ekg.finde_spitzen(340, 4)
            hr = ekg.schätze_hr()
        except:
            st.write("Keine Daten vorhanden. Andere Person wählen!")

        # Tab-Elemente für die EKG-Daten
        tab1, tab2 = st.tabs(["Daten", "Grafik"])

        try:
            with tab1:
                st.write("Daten des EKGs: {}".format(st.session_state.aktueller_benutzer))
                st.write('Datum:', ekg.datum)
                st.write("Durchschnittliche Herzfrequenz: ", int(hr.mean()))

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
            st.write("Keine Daten vorhanden. Andere Person wählen!")
            
    with tabs[1]:  # BMI & Ernährung Bereich
        st.write("# BMI & Ernährung")
        st.write("### BMI berechnen")
        
        # Eingabefelder für die BMI-Berechnung
        gewicht = st.number_input("Gewicht (in kg)", min_value=0.0, step=0.1)
        groesse = st.number_input("Größe (in cm)", min_value=0.0, step=0.1)
        geschlecht = st.selectbox("Geschlecht", ["Männlich", "Weiblich"])

        if groesse > 0:
            bmi = berechne_bmi(gewicht, groesse)
            st.write("Ihr BMI ist: {:.2f}".format(bmi))
            bmi_status = bmi_bereich(bmi)
            st.write(f"Sie befinden sich im Bereich: {bmi_status}")
        else:
            st.write("Bitte geben Sie eine gültige Größe ein.")

        st.write("### Täglicher Kalorienbedarf")
        
        # Eingabefelder für den Kalorienbedarf
        alter = st.number_input("Alter", min_value=0)
        aktivitaetslevel = st.selectbox("Aktivitätslevel", ["Wenig aktiv", "Mäßig aktiv", "Aktiv", "Sehr aktiv"])
        
        kalorienbedarf = berechne_kalorienbedarf(gewicht, groesse, alter, geschlecht, aktivitaetslevel)
        st.write("Ihr täglicher Kalorienbedarf ist: {:.0f} kcal".format(kalorienbedarf))
        if st.button("Daten speichern"):
            user_data['gewicht'] = gewicht
            user_data['groesse'] = groesse
            user_data['geschlecht'] = geschlecht
            user_data['alter'] = alter
            user_data['aktivitaetslevel'] = aktivitaetslevel
            user_data['bmi'] = bmi
            user_data['kalorienbedarf'] = kalorienbedarf
            add_weight(st.session_state.user_id, pd.Timestamp.now().isoformat(), gewicht)
            add_bmi(st.session_state.user_id, pd.Timestamp.now().isoformat(), bmi)
            st.success("Daten erfolgreich gespeichert!")

        st.write("### Gewichtsdaten")
        weights = get_weights(st.session_state.user_id)
        if weights:
            weight_df = pd.DataFrame(weights, columns=["Datum", "Gewicht"])
            weight_df["Datum"] = pd.to_datetime(weight_df["Datum"])
            fig = px.line(weight_df, x="Datum", y="Gewicht", title="Gewichtsverlauf")
            st.plotly_chart(fig)
        else:
            st.write("Keine Gewichtsdaten verfügbar")

        st.write("### BMI-Verlauf")
        bmis = get_bmi(st.session_state.user_id)
        if bmis:
            bmi_df = pd.DataFrame(bmis, columns=["Datum", "BMI"])
            bmi_df["Datum"] = pd.to_datetime(bmi_df["Datum"])
            fig = px.line(bmi_df, x="Datum", y="BMI", title="BMI-Verlauf")
            st.plotly_chart(fig)
        else:
            st.write("Keine BMI-Daten verfügbar")

        st.write("### Ernährungspyramide")
        # Hier könntest du ein Bild der Ernährungspyramide hinzufügen
        pyramide_bild = Image.open("images.jpeg")
        st.image(pyramide_bild, caption="Ernährungspyramide")

        st.write("### Zitate für Body Positivity")
        zitate = [
            "Liebe deinen Körper, er ist der einzige, den du hast.",
            "Schönheit kommt in allen Formen und Größen.",
            "Dein Körper ist dein Zuhause, behandle ihn mit Respekt."
        ]
        st.write("#### Body Positivity Zitate")
        for zitat in zitate:
            st.write(f"- {zitat}")

    with tabs[2]:  # Mahlzeiten & Sport Bereich
        track_meals_sports(st.session_state.user_id, user_data)

    with tabs[3]:  # KI-Funktionalitäten Bereich
        st.write("# KI-Funktionalitäten")
        # Hier kannst du deine KI-Funktionalitäten hinzufügen
        st.write("Hier werden KI-Funktionalitäten implementiert.")

    with tabs[4]:  # Datenbank-Verwaltung Bereich
        st.write("# Datenbank-Verwaltung")
        
        st.subheader("Benutzerverwaltung")
        username = st.text_input("Benutzername zum Anzeigen")
        if st.button("Benutzer anzeigen"):
            user = get_user(username)
            if user:
                st.write(f"ID: {user[0]}, Benutzername: {user[1]}, E-Mail: {user[3]}, Name: {user[4]}")
            else:
                st.write("Benutzer nicht gefunden")

        st.subheader("Datenbereinigung")
        if st.button("Alle Daten löschen"):
            if st.button("Bestätigen"):
                os.remove('data.db')
                init_db()
                st.success("Alle Daten wurden gelöscht")

        st.subheader("Datenexport")
        if st.button("Daten exportieren"):
            data = {
                'users': get_all_users(),
                'meals': get_all_meals(),
                'weights': get_all_weights(),
                'bmi': get_all_bmi()
            }
            with open('data_export.json', 'w') as f:
                json.dump(data, f)
            st.success("Daten wurden exportiert")

        st.subheader("Datenbank-Backup und Wiederherstellung")
        if st.button("Backup erstellen"):
            conn = sqlite3.connect('data.db')
            with open('backup.db', 'w') as f:
                for line in conn.iterdump():
                    f.write(f'{line}\n')
            st.success("Backup wurde erstellt")

        uploaded_file = st.file_uploader("Backup-Datei hochladen", type=["db"])
        if uploaded_file is not None:
            with open('data.db', 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.success("Backup wurde wiederhergestellt")
