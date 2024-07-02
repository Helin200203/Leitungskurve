import streamlit as st
from person import Person  # Make sure to have the correct import statements for your modules
from PIL import Image
from ekgdata import EKGDaten
import plotly.graph_objects as go
from auth import get_authenticator, register_user
from utils import berechne_bmi, berechne_kalorienbedarf, bmi_bereich  
# Authentifikator und Konfiguration laden
authenticator, config = get_authenticator()

# Login oder Registrierung
st.sidebar.title("Willkommen")
option = st.sidebar.radio("Login/Registrierung", ["Login", "Registrierung"])

if option == "Login":
    name, authentication_status, username = authenticator.login("main")

    if authentication_status:
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

        user_data = st.session_state.user_data
        # Haupt-Tabs für verschiedene Bereiche
        tabs = st.tabs(["EKG-Daten","BMI & Kalorienbedraf", "Mahlzeiten & Sport", "KI-Funktionalitäten", "Datenbank-Verwaltung"])

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
                st.success("Daten erfolgreich gespeichert!")
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
            st.write("# Mahlzeiten & Sport")
            
            st.write("### Mahlzeiten tracken")
            meal_date = st.date_input("Datum", key="meal_date")
            meal_name = st.text_input("Mahlzeit", key="meal_name")
            meal_calories = st.number_input("Kalorien", min_value=0.0, step=0.1, key="meal_calories")
            if st.button("Mahlzeit hinzufügen"):
                user_data['meals'].append({'date': meal_date, 'meal': meal_name, 'calories': meal_calories})
                st.success("Mahlzeit erfolgreich hinzugefügt!")
            
            st.write("### Sportaktivitäten tracken")
            workout_date = st.date_input("Datum", key="workout_date")
            workout_name = st.text_input("Sportaktivität", key="workout_name")
            workout_duration = st.number_input("Dauer (in Minuten)", min_value=0, step=1, key="workout_duration")
            workout_calories_burned = st.number_input("Verbrannte Kalorien", min_value=0.0, step=0.1, key="workout_calories_burned")
            if st.button("Sportaktivität hinzufügen"):
                user_data['workouts'].append({'date': workout_date, 'workout': workout_name, 'duration': workout_duration, 'calories_burned': workout_calories_burned})
                st.success("Sportaktivität erfolgreich hinzugefügt!")
            
            st.write("### Getrackte Mahlzeiten")
            if meal_date:
                meals = [meal for meal in user_data['meals'] if meal['date'] == meal_date]
                for meal in meals:
                    st.write(f"{meal['meal']}: {meal['calories']} kcal")

            st.write("### Getrackte Sportaktivitäten")
            if workout_date:
                workouts = [workout for workout in user_data['workouts'] if workout['date'] == workout_date]
                for workout in workouts:
                    st.write(f"{workout['workout']} ({workout['duration']} Minuten): {workout['calories_burned']} kcal verbrannt")               

        with tabs[3]:  # KI-Funktionalitäten Bereich
            st.write("# KI-Funktionalitäten")
            # Hier kannst du deine KI-Funktionalitäten hinzufügen
            st.write("Hier werden KI-Funktionalitäten implementiert.")

        with tabs[4]:  # Datenbank-Verwaltung Bereich
            st.write("# Datenbank-Verwaltung")
            # Hier kannst du die Datenbank-Verwaltung implementieren
            st.write("Hier wird die Datenbank-Verwaltung implementiert.")

    elif authentication_status == False:
        st.error('Benutzername/Passwort ist inkorrekt')
    elif authentication_status == None:
        st.warning('Bitte geben Sie Ihren Benutzernamen und Ihr Passwort ein')

elif option == "Registrierung":
    register_user()