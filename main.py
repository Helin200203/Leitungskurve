from PIL import Image
import streamlit as st
from auth import login_user_interface, register_user_interface
import fit_ekg_description

def main():
    st.set_page_config(page_title="FitEKG", page_icon="🏋️")

    st.title("FitEKG")

    logo = Image.open("final_logo_in_black_circle.png")  
    st.image(logo, width=200)
    st.sidebar.success("login sie sich ein oder registrieren sie sich, um die App zu nutzen.")

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
            fit_ekg_description.fit_ekg_description()
        elif page == "EKG-Daten":
            from _1ekgpage import ekg_page
            ekg_page()
        elif page == "Fitnessdaten":
            from _2fitnesspage import show_fitness_page
            show_fitness_page(st.session_state.user_id, st.session_state.user_data)
        elif page == "KI-Funktionen":
            from _3kipage import show_ki_page
            show_ki_page()
        elif page == "Datenbank-Verwaltung":
            # Passwortabfrage
            if 'db_admin' not in st.session_state:
                st.session_state.db_admin = False

            if not st.session_state.db_admin:
                password = st.text_input("Geben Sie das Passwort ein", type="password")
                if password == "zu9gierig":
                    st.session_state.db_admin = True
                    st.success("Zugriff gewährt!")
                else:
                    st.error("Falsches Passwort")

            if st.session_state.db_admin:
                from _4dbmanagementpage import show_db_management_page
                show_db_management_page()

if __name__ == "__main__":
    main()

