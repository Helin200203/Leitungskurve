# bmi_nutrition.py
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from database import add_weight, add_bmi, get_weights, get_bmi
from utils import berechne_bmi, berechne_kalorienbedarf, bmi_bereich
from language import languages

def display_bmi_nutrition_section(user_data):
    language = st.session_state.language
    lang = languages[language]
    
    st.write(f"# {lang['bmi_nutrition']}")
    st.write(f"### {lang['bmi_calculate']}")
    
    # Eingabefelder für die BMI-Berechnung
    gewicht = st.number_input(lang['weight'], min_value=0.0, step=0.1)
    groesse = st.number_input(lang['height'], min_value=0.0, step=0.1)
    geschlecht = st.selectbox(lang['gender'], [lang['male'], lang['female']])

    if groesse > 0:
        bmi = berechne_bmi(gewicht, groesse)
        st.write(lang['bmi_is'].format(bmi))
        bmi_status = bmi_bereich(bmi)
        st.write(lang['bmi_status'].format(bmi_status))
    else:
        st.write(lang['valid_height'])

    st.write(f"### {lang['daily_calorie']}")
    
    # Eingabefelder für den Kalorienbedarf
    alter = st.number_input(lang['age'], min_value=0)
    aktivitaetslevel = st.selectbox(lang['activity_level'], lang['activity_levels'])
    
    kalorienbedarf = berechne_kalorienbedarf(gewicht, groesse, alter, geschlecht, aktivitaetslevel)
    st.write(lang['calorie_need'].format(kalorienbedarf))
    if st.button(lang['save_data']):
        user_data['gewicht'] = gewicht
        user_data['groesse'] = groesse
        user_data['geschlecht'] = geschlecht
        user_data['alter'] = alter
        user_data['aktivitaetslevel'] = aktivitaetslevel
        user_data['bmi'] = bmi
        user_data['kalorienbedarf'] = kalorienbedarf
        add_weight(st.session_state.user_id, pd.Timestamp.now().isoformat(), gewicht)
        add_bmi(st.session_state.user_id, pd.Timestamp.now().isoformat(), bmi)
        st.success(lang['success_save'])

    tab1, tab2 = st.tabs([lang['weight_bmi_progress'], lang['positive']])
    try: 
        with tab1:
            st.write(f"### {lang['weight_data']}")
            weights = get_weights(st.session_state.user_id)
            if weights:
                weight_df = pd.DataFrame(weights, columns=["Datum", "Gewicht"])
                weight_df["Datum"] = pd.to_datetime(weight_df["Datum"])
                fig = px.line(weight_df, x="Datum", y="Gewicht", title=lang['weight_progress'])
                st.plotly_chart(fig)
            else:
                st.write(lang['no_weight_data'])

            st.write(f"### {lang['bmi_progress']}")
            bmis = get_bmi(st.session_state.user_id)
            if bmis:
                bmi_df = pd.DataFrame(bmis, columns=["Datum", "BMI"])
                bmi_df["Datum"] = pd.to_datetime(bmi_df["Datum"])
                fig = px.line(bmi_df, x="Datum", y="BMI", title=lang['bmi_progress'])
                st.plotly_chart(fig)
            else:
                st.write(lang['no_bmi_data'])
        with tab2:
            st.write(f"### {lang['pyramid']}")
            pyramide_bild = Image.open("images.jpeg")
            st.image(pyramide_bild, caption=lang['pyramid'])

            st.write(f"### {lang['body_positivity_quotes']}")
            zitate = [
                "Liebe deinen Körper, er ist der einzige, den du hast.",
                "Schönheit kommt in allen Formen und Größen.",
                "Dein Körper ist dein Zuhause, behandle ihn mit Respekt."
            ]
            for zitat in zitate:
                st.write(f"- {zitat}")
    except:
        st.write(lang['no_data'])
