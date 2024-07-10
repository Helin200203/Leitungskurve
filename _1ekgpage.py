import streamlit as st
import herz_info
from schow_ekg import show_ekg
import schow_ekg_upload 

def ekg_page():
    st.subheader(f"Willkommen, {st.session_state['username']}!")
    st.write("Wählen Sie eine Option:")

    tabs = st.tabs(["Unser Herz", "Probe EKG-Daten", "Deine Ekg-Daten"])

    with tabs[0]:
        herz_info.heart_info()         
    with tabs[1]:
       show_ekg()
       
    with tabs[2]:
       schow_ekg_upload.display_hr_analysis()
