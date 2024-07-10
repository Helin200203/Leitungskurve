
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.signal as signal
import EKGdata2 as EKGdata

def display_hr_analysis():
    st.title("Herzfrequenzvariabilitätsanalyse (HRV)")

    uploaded_file = st.file_uploader("Laden Sie Ihre EKG-Daten hoch", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Hochgeladene Datei:")
        st.write(df.head())

        # Annahme, dass notwendige person_info aus der Datei extrahiert oder standardisiert werden kann
        person_info = {
            'file_type': uploaded_file.name,
            'gender': st.selectbox("Geschlecht", options=["männlich", "weiblich", "divers"]),
            'type': st.selectbox("Typ des EKGs", options=["Ruhe", "Belastung"])
        }

        ekg_data = EKGdata.EKGdata(df, person_info)
        df = ekg_data.df
        peaks = EKGdata.EKGdata.find_peaks(df["ECG Signal (mV)"], 0.5, 200)
        heart_rate_times, heart_rate_at_peaks = EKGdata.EKGdata.estimate_hr(peaks, df["Time in s"])

        min_time = df["Time in s"].min()
        max_time = df["Time in s"].max()

        st.subheader("EKG und Herzfrequenzanalyse")
        st.write(f"EKG-Typ: {ekg_data.type}")

        st.write("Wählen Sie den Zeitbereich für den EKG-Plot aus:")
        start_time_ekg, end_time_ekg = st.slider(
            "Zeitbereich für EKG-Plot:",
            min_value=float(min_time),
            max_value=float(max_time),
            value=(float(min_time), float(max_time)),
            step=0.1
        )

        ekg_fig = EKGdata.EKGdata.make_ekg_plot(peaks, df, start_time_ekg, end_time_ekg)
        st.plotly_chart(ekg_fig)

        st.subheader("Wählen Sie den Zeitbereich für den Herzfrequenz-Plot aus:")
        start_time_hr, end_time_hr = st.slider(
            "Zeitbereich für Herzfrequenz-Plot:",
            min_value=float(min_time),
            max_value=float(max_time),
            value=(float(min_time), float(max_time)),
            step=0.1
        )

        heart_rate_fig = EKGdata.EKGdata.make_hf_plot(heart_rate_times, heart_rate_at_peaks, start_time_hr, end_time_hr)
        st.plotly_chart(heart_rate_fig)

        st.subheader("Wählen Sie die Fenstergröße für den gleitenden Durchschnitt:")
        window_size = st.slider("Fenstergröße:", min_value=1, max_value=50, value=10, step=1)
        smoothed_heart_rate_fig = EKGdata.EKGdata.plot_moving_average_heart_rate(heart_rate_at_peaks, heart_rate_times, window_size, start_time_hr, end_time_hr)
        st.plotly_chart(smoothed_heart_rate_fig)

if __name__ == "__main__":
    display_hr_analysis()

