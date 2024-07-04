# meals_sport.py
import streamlit as st
from database import add_meal, add_weight, get_meals, get_weights
import plotly.express as px
import pandas as pd

def track_meals_sports(user_id, user_data):
    st.write("# Mahlzeiten & Sport")
    
    st.write("### Mahlzeiten tracken")
    meal_date = st.date_input("Datum", key="meal_date")
    meal_name = st.text_input("Mahlzeit", key="meal_name")
    meal_calories = st.number_input("Kalorien", min_value=0.0, step=0.1, key="meal_calories")
    if st.button("Mahlzeit hinzufügen"):
        add_meal(user_id, meal_date.isoformat(), meal_name, meal_calories)
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
    selected_date = st.date_input("Datum auswählen", key="select_meal_date")
    if selected_date:
        meals = [meal for meal in user_data['meals'] if meal['date'] == selected_date]
        for meal in meals:
            st.write(f"{meal['meal']}: {meal['calories']} kcal")

    st.write("### Getrackte Sportaktivitäten")
    if selected_date:
        workouts = [workout for workout in user_data['workouts'] if workout['date'] == selected_date]
        for workout in workouts:
            st.write(f"{workout['workout']} ({workout['duration']} Minuten): {workout['calories_burned']} kcal verbrannt")

    st.write("### Gewichtsdaten")
    weights = get_weights(user_id)
    if weights:
        weight_df = pd.DataFrame(weights, columns=["Datum", "Gewicht"])
        weight_df["Datum"] = pd.to_datetime(weight_df["Datum"])
        fig = px.line(weight_df, x="Datum", y="Gewicht", title="Gewichtsverlauf")
        st.plotly_chart(fig)
    else:
        st.write("Keine Gewichtsdaten verfügbar")
