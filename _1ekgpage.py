import streamlit as st
import herz_info
from schow_ekg import show_ekg
from schow_ekg_upload import ekg_upload 

def ekg_page():
    st.subheader(f"Willkommen, {st.session_state['username']}!")
    st.write("Wählen Sie eine Option:")

    tabs = st.tabs(["Unser Herz", "Probe EKG-Daten", "Deine Ekg-Daten"])

    with tabs[0]:
        herz_info.heart_info()
         
    with tabs[1]:
       show_ekg()
       
    with tabs[2]:
        st.write("Um EKG-Daten hochzuladen, klicke auf 'Upload EKG-Daten'.")
        if st.button("Upload EKG-Daten"):
            ekg_upload()
