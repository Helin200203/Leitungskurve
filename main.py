import streamlit as st
from auth import login_user_interface, register_user_interface

st.set_page_config(page_title="FitEKG", page_icon="🏋️")

st.title("FitEKG")

st.sidebar.success("Wählen Sie eine Seite aus dem Menü")

st.sidebar.title("Willkommen")

# Initialisieren der Session State Variablen
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

if 'reset_password_flag' not in st.session_state:
    st.session_state.reset_password_flag = False

# Login oder Registrierung
if not st.session_state.logged_in:
    option = st.sidebar.radio("Login / Registrieren", ["Login", "Registrieren"])

    if option == "Login":
        login_user_interface()
        
    elif option == "Registrieren":
        register_user_interface()

if st.session_state.logged_in:
    st.sidebar.write("Navigation")
    page = st.sidebar.radio("Gehe zu", ["Startseite", "EKG-Daten", "Fitnessdaten", "KI-Funktionen", "Datenbank-Verwaltung"])

    if page == "Startseite":
        st.write("Willkommen bei FitEKG!")
    elif page == "EKG-Daten":
        from  ekg_page import show_ekg_page
        show_ekg_page()
    elif page == "Fitnessdaten":
        from fitness_page import show_fitness_page
        show_fitness_page()
    elif page == "KI-Funktionen":
        from ki_page import show_ki_page
        show_ki_page()
    elif page == "Datenbank-Verwaltung":
        from db_management_page import show_db_management_page
        show_db_management_page()
