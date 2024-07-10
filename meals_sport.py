# meals_sport.py
import streamlit as st
from database import add_meal, get_meals, add_workout, get_workouts, add_weight, add_bmi, get_weights, get_bmi
import pandas as pd
import plotly.express as px
from utils import berechne_bmi, berechne_kalorienbedarf, bmi_bereich

def track_meals_sports(user_id, user_data):
    st.write("# Mahlzeiten & Sport")
    
    st.write("### Mahlzeiten tracken")
    meal_date = st.date_input("Datum", key="meal_date")
    meal_type = st.selectbox("Mahlzeitentyp", ["Frühstück", "Mittagessen", "Abendessen", "Snack"], key="meal_type")
    meal_name = st.text_input("Mahlzeit", key="meal_name")
    meal_calories = st.number_input("Kalorien", min_value=0.0, step=0.1, key="meal_calories")
    if st.button("Mahlzeit speichern"):
        add_meal(user_id, meal_date.isoformat(), meal_type, meal_name, meal_calories)
        user_data['meals'].append({'date': meal_date, 'type': meal_type, 'meal': meal_name, 'calories': meal_calories})
        st.success("Mahlzeit erfolgreich hinzugefügt!")
    
    st.write("### Sportaktivitäten tracken")
    workout_date = st.date_input("Datum", key="workout_date")
    workout_name = st.text_input("Sportaktivität", key="workout_name")
    workout_duration = st.number_input("Dauer (in Minuten)", min_value=0, step=1, key="workout_duration")
    workout_calories_burned = st.number_input("Verbrannte Kalorien", min_value=0.0, step=0.1, key="workout_calories_burned")
    if st.button("Sportaktivität speichern"):
        add_workout(user_id, workout_date.isoformat(), workout_name, workout_duration, workout_calories_burned)
        user_data['workouts'].append({'date': workout_date, 'workout': workout_name, 'duration': workout_duration, 'calories_burned': workout_calories_burned})
        st.success("Sportaktivität erfolgreich hinzugefügt!")
    
    st.write("### Getrackte Mahlzeiten")
    selected_meal_date = st.date_input("Datum auswählen für Mahlzeiten", key="select_meal_date")
    if selected_meal_date:
        meals = get_meals(user_id, selected_meal_date.isoformat())
        if meals:
            meal_df = pd.DataFrame(meals, columns=["Datum", "Typ", "Mahlzeit", "Kalorien"])
            st.table(meal_df)
        else:
            st.write("Keine Mahlzeiten für das ausgewählte Datum gefunden.")

    st.write("### Getrackte Sportaktivitäten")
    selected_workout_date = st.date_input("Datum auswählen für Sportaktivitäten", key="select_workout_date")
    if selected_workout_date:
        workouts = get_workouts(user_id, selected_workout_date.isoformat())
        if workouts:
            workout_df = pd.DataFrame(workouts, columns=["Datum", "Sportaktivität", "Dauer", "Verbrannte Kalorien"])
            st.table(workout_df)
        else:
            st.write("Keine Sportaktivitäten für das ausgewählte Datum gefunden.")