import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_ekg_upload_page():
    st.title("Eigene EKG-Daten hochladen")
    uploaded_file = st.file_uploader("Wählen Sie eine Datei aus", type=["csv", "txt"])

    if uploaded_file is not None:
        # Annahme: Die Datei enthält EKG-Daten in einer Spalte
        df = pd.read_csv(uploaded_file)
        st.write("Hochgeladene EKG-Daten")
        st.dataframe(df)

        if 'uploaded_ekg_data' not in st.session_state:
            st.session_state.uploaded_ekg_data = []

        try:
            # Hier wird angenommen, dass die hochgeladenen Daten in der ersten Spalte sind
            ekg_data = df.iloc[:, 0]
            ekg_data = ekg_data.dropna().reset_index(drop=True)
            st.session_state.uploaded_ekg_data.append(ekg_data)

            hr = ekg_data.rolling(window=340).mean().dropna()  # Beispiel für Spitzenberechnung
            hr.index = hr.index / 1000  # Umwandlung von Index in Sekunden

            st.write("### Analyse der hochgeladenen EKG-Daten")
            fig = go.Figure(data=go.Scatter(x=hr.index, y=hr), layout=go.Layout(title="Herzfrequenz", xaxis_title="Zeit in s", yaxis_title="Herzfrequenz in bpm"))
            fig.update_layout(
                xaxis=dict(
                    rangeslider=dict(
                        visible=True
                    ),
                    type="linear"
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            st.write(f"Durchschnittliche Herzfrequenz: {hr.mean():.2f} bpm")
        except Exception as e:
            st.write(f"Fehler bei der Analyse der hochgeladenen EKG-Daten: {e}")
