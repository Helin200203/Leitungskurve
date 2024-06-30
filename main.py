import streamlit as st
from person import Person
from PIL import Image
from ekgdata import EKGDaten
import plotly.graph_objects as go

# Laden der Personendaten und Erstellen der Namensliste
personen_daten = Person.lade_personen_daten() 
personen_namensliste = Person.get_personen_liste(personen_daten)

# Session State wird leer angelegt, solange er noch nicht existiert
if 'aktueller_benutzer' not in st.session_state:
    st.session_state.aktueller_benutzer = 'None'

st.write("# EKG APP") # Eine Überschrift der ersten Ebene
st.write("### Versuchsperson auswählen") # Eine Überschrift der zweiten Ebene

st.session_state.aktueller_benutzer = st.selectbox(
    'Versuchsperson',
    options = personen_namensliste, key="sbVersuchsperson")

# Finden der Person - den String haben wir im Session state
aktuelle_person = Person.finde_personen_daten_nach_name(st.session_state.aktueller_benutzer)
aktuelle_person_obj = Person(aktuelle_person) # Erstellen eines Person-Objekts aus dem Dictionary
person_ekg_liste = Person.ekgs_von_person(personen_daten, aktuelle_person_obj.id) # Erstellen einer Liste von EKGs der gewählten Person

bild = Image.open(aktuelle_person_obj.bild_pfad) # Bild laden und Auslesen des Pfades aus dem zurückgegebenen Dictionary

# Bild und Informationen nebeneinander anzeigen
links, spalte1, mitte, spalte2 = st.columns([10,1,10,20])
with spalte1:
    st.image(bild, width=140)
with spalte2:
    st.write('**Vorname:**', aktuelle_person_obj.vorname)
    st.write('**Nachname:**', aktuelle_person_obj.nachname)
    st.write('**Alter:**', aktuelle_person_obj.alter)
    st.write('**Max HR:**', aktuelle_person_obj.max_hr_bpm)

st.session_state.aktueller_benutzer = st.selectbox(
    'EKG-Daten auswählen:',
    options = person_ekg_liste, key="sbEKGliste")

st.write("Ausgewähltes EKG: ", st.session_state.aktueller_benutzer, "von:", aktuelle_person_obj.vorname, aktuelle_person_obj.nachname)

try:
    ekg = EKGDaten(aktuelle_person_obj.id, st.session_state.aktueller_benutzer)
    ekg.finde_spitzen(340, 4)
    hr = ekg.schätze_hr()
except:
    st.write("Keine Daten vorhanden. Andere Person wählen!")

# Tab-Elemente erstellen
tab1, tab2 = st.tabs(["Daten", "Grafik"])

try:
    with tab1:
        st.write("Daten des EKGs: {}".format(st.session_state.aktueller_benutzer))
        st.write('Datum:', ekg.datum)
        st.write("Durchschnittliche Herzfrequenz: ", int(hr.mean()))

    with tab2:
        fig = go.Figure(data=go.Scatter(x=hr.index/1000, y=hr), layout=go.Layout(title="Herzfrequenz", xaxis_title="Zeit in s", yaxis_title="Herzfrequenz in bpm"))
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
                type="linear"
            )
        )
        st.plotly_chart(fig, use_container_width=True)
except:
    st.write("Keine Daten vorhanden. Andere Person wählen!")
