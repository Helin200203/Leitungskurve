import streamlit as st
from person import Person  # Make sure to have the correct import statements for your modules
from PIL import Image
from ekgdata import EKGDaten
import plotly.graph_objects as go
from auth import get_authenticator, register_user
from utils import berechne_bmi, berechne_kalorienbedarf, bmi_bereich  
from database import create_table, insert_user, update_user_data, get_user_data  # Importiere die Funktionen aus database.py

# Datenbank initialisieren
create_table()
# Authentifikator und Konfiguration laden
authenticator, config = get_authenticator()

# Login oder Registrierung
st.sidebar.title("Willkommen")
option = st.sidebar.radio("Login/Registrierung", ["Login", "Registrierung"])

if option == "Login":
    name, authentication_status, username = authenticator.login("main")

    if authentication_status:
        # Haupt-Tabs für verschiedene Bereiche
        tabs = st.tabs(["EKG-Daten","BMI & Kalorienbedraf", "KI-Funktionalitäten", "Datenbank-Verwaltung"])

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

        with tabs[2]:  # KI-Funktionalitäten Bereich
            st.write("# KI-Funktionalitäten")
            # Hier kannst du deine KI-Funktionalitäten hinzufügen
            st.write("Hier werden KI-Funktionalitäten implementiert.")

        with tabs[3]:  # Datenbank-Verwaltung Bereich
            st.write("# Datenbank-Verwaltung")
            # Hier kannst du die Datenbank-Verwaltung implementieren
            st.write("Hier wird die Datenbank-Verwaltung implementiert.")

    elif authentication_status == False:
        st.error('Benutzername/Passwort ist inkorrekt')
    elif authentication_status == None:
        st.warning('Bitte geben Sie Ihren Benutzernamen und Ihr Passwort ein')

elif option == "Registrierung":
    register_user()