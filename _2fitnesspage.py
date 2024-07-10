import streamlit as st
from bmi_nutrition import display_bmi_nutrition_section
import fitness_info
import meals_sport

def show_fitness_page(user_id, user_data):
    st.title("Fitnessdaten")
    st.write("Wählen Sie eine Option:")

    tabs = st.tabs(["Meine Gesundheit", "Meine Maßen", "Mahlzeit Tracker"])
    
    with tabs[0]:
        fitness_info.fitness_info()
    with tabs[1]:
        display_bmi_nutrition_section(user_data)
    with tabs[2]:
        meals_sport.track_meals_sports(user_id, user_data)