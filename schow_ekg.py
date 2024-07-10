import streamlit as st
from person import Person
from PIL import Image
from ekgdata import EKGDaten
import plotly.graph_objects as go

def show_ekg():
    st.write("### Person auswählen")

    personen_daten = Person.lade_personen_daten()
    personen_namensliste = Person.get_personen_liste(personen_daten)

    if 'aktueller_benutzer' not in st.session_state:
        st.session_state.aktueller_benutzer = 'None'

    st.session_state.aktueller_benutzer = st.selectbox("Person auswählen", options=personen_namensliste, key="sbVersuchsperson")

    aktuelle_person = Person.finde_personen_daten_nach_name(st.session_state.aktueller_benutzer)
    if aktuelle_person:
        aktuelle_person_obj = Person(aktuelle_person)
        person_ekg_liste = Person.ekgs_von_person(personen_daten, aktuelle_person_obj.id)

        bild = Image.open(aktuelle_person_obj.bild_pfad)

        links, spalte1, mitte, spalte2 = st.columns([10, 1, 10, 20])
        with spalte1:
            st.image(bild, width=140)
        with spalte2:
            st.write(f'**Vorname:**', aktuelle_person_obj.vorname)
            st.write(f'**Nachname:**', aktuelle_person_obj.nachname)
            st.write(f'**Alter:**', aktuelle_person_obj.alter)
            st.write(f'**Max HR:**', aktuelle_person_obj.max_hr_bpm)

        st.session_state.aktueller_ekg = st.selectbox("EKG auswählen", options=person_ekg_liste, key="sbEKGliste")

        st.write(f"EKG-Daten: ", st.session_state.aktueller_ekg, "von:", aktuelle_person_obj.vorname, aktuelle_person_obj.nachname)

        try:
            ekg = EKGDaten(aktuelle_person_obj.id, st.session_state.aktueller_ekg)
            ekg.finde_spitzen(340, 4)
            hr = ekg.schätze_hr()
        except Exception as e:
            st.write("Fehler beim Laden der EKG-Daten:", e)
            st.write("Keine Daten vorhanden")

        tab1, tab2 = st.tabs(["Daten", "Graph"])

        try:
            with tab1:
                st.write(f"EKG-Daten: {st.session_state.aktueller_ekg}")
                st.write('Datum:', ekg.datum)
                st.write(f"Durchschnittliche Herzfrequenz: ", int(hr.mean()))

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
        except Exception as e:
            st.write("Fehler beim Plotten der Daten:", e)
            st.write("Keine Daten vorhanden")

if __name__ == "__main__":
    show_ekg()
