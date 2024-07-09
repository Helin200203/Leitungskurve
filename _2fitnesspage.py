import streamlit as st
from bmi_nutrition import display_bmi_nutrition_section

def show_fitness_page():
    st.title("Fitnessdaten")
    display_bmi_nutrition_section(st.session_state.user_data)
