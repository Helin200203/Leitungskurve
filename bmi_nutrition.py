import streamlit as st
from utils import berechne_bmi, berechne_kalorienbedarf, bmi_bereich
import pandas as pd
import plotly.express as px
from PIL import Image
from database import add_meal, get_meals, add_workout, get_workouts, add_weight, add_bmi, get_weights, get_bmi

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