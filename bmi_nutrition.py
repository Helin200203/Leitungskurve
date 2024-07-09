import streamlit as st
from utils import berechne_bmi, berechne_kalorienbedarf, bmi_bereich
import pandas as pd
import plotly.express as px
from PIL import Image
from database import add_weight, add_bmi, get_weights, get_bmi, add_meal, get_meals, add_workout, get_workouts

def display_bmi_nutrition_section(user_data):
    st.write("### BMI berechnen")
    
    gewicht = st.number_input("Gewicht (kg)", min_value=0.0, step=0.1)
    groesse = st.number_input("Größe (cm)", min_value=0.0, step=0.1)
    geschlecht = st.selectbox("Geschlecht", ["Männlich", "Weiblich"])

    if groesse > 0:
        bmi = berechne_bmi(gewicht, groesse)
        st.write(f"Ihr BMI ist: {bmi:.2f}")
        bmi_status = bmi_bereich(bmi)
        st.write(f"BMI-Status: {bmi_status}")
    else:
        st.write("Bitte geben Sie eine gültige Größe ein.")

    st.write("### Täglicher Kalorienbedarf")
    
    alter = st.number_input("Alter", min_value=0)
    aktivitaetslevel = st.selectbox("Aktivitätslevel", ["Wenig aktiv", "Mäßig aktiv", "Aktiv", "Sehr aktiv"])
    
    kalorienbedarf = berechne_kalorienbedarf(gewicht, groesse, alter, geschlecht, aktivitaetslevel)
    st.write(f"Ihr täglicher Kalorienbedarf beträgt: {kalorienbedarf:.2f} Kalorien")
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
        st.success("Daten erfolgreich gespeichert")

    st.write("### Mahlzeiten hinzufügen")
    meal_date = st.date_input("Datum der Mahlzeit")
    meal_type = st.selectbox("Art der Mahlzeit", ["Frühstück", "Mittagessen", "Abendessen", "Snack"])
    meal = st.text_input("Beschreibung der Mahlzeit")
    meal_calories = st.number_input("Kalorien (kcal)", min_value=0.0, step=0.1)
    if st.button("Mahlzeit hinzufügen"):
        add_meal(st.session_state.user_id, meal_date.isoformat(), meal_type, meal, meal_calories)
        st.success("Mahlzeit erfolgreich hinzugefügt")

    st.write("### Aktivitäten hinzufügen")
    workout_date = st.date_input("Datum der Aktivität")
    workout = st.text_input("Beschreibung der Aktivität")
    workout_duration = st.number_input("Dauer (Minuten)", min_value=0)
    workout_calories = st.number_input("Kalorienverbrauch (kcal)", min_value=0.0, step=0.1)
    if st.button("Aktivität hinzufügen"):
        add_workout(st.session_state.user_id, workout_date.isoformat(), workout, workout_duration, workout_calories)
        st.success("Aktivität erfolgreich hinzugefügt")

    tab1, tab2, tab3 = st.tabs(["Gewichts- und BMI-Verlauf", "Mahlzeitenverlauf", "Aktivitätenverlauf"])
    try: 
        with tab1:
            st.write("### Gewichtsdaten")
            weights = get_weights(st.session_state.user_id)
            if weights:
                weight_df = pd.DataFrame(weights, columns=["Datum", "Gewicht"])
                weight_df["Datum"] = pd.to_datetime(weight_df["Datum"])
                fig = px.line(weight_df, x="Datum", y="Gewicht", title="Gewichtsverlauf")
                st.plotly_chart(fig)
            else:
                st.write("Keine Gewichtsdaten vorhanden")

            st.write("### BMI-Verlauf")
            bmis = get_bmi(st.session_state.user_id)
            if bmis:
                bmi_df = pd.DataFrame(bmis, columns=["Datum", "BMI"])
                bmi_df["Datum"] = pd.to_datetime(bmi_df["Datum"])
                fig = px.line(bmi_df, x="Datum", y="BMI", title="BMI-Verlauf")
                st.plotly_chart(fig)
            else:
                st.write("Keine BMI-Daten vorhanden")

        with tab2:
            st.write("### Mahlzeitenverlauf")
            meals = get_meals(st.session_state.user_id)
            if meals:
                meals_df = pd.DataFrame(meals, columns=["Datum", "Art", "Beschreibung", "Kalorien"])
                st.dataframe(meals_df)
            else:
                st.write("Keine Mahlzeitendaten vorhanden")

        with tab3:
            st.write("### Aktivitätenverlauf")
            workouts = get_workouts(st.session_state.user_id)
            if workouts:
                workouts_df = pd.DataFrame(workouts, columns=["Datum", "Beschreibung", "Dauer (Minuten)", "Kalorienverbrauch"])
                st.dataframe(workouts_df)
            else:
                st.write("Keine Aktivitätendaten vorhanden")
    except:
        st.write("Keine Daten vorhanden")
