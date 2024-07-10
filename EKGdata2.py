import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.signal as signal
<<<<<<< HEAD
from database import get_user, init_db
init_db()
=======
from database import get_user

>>>>>>> a622fa8d3a9be039d2fb7608e63221e9e16c8859
class EKGdata:

    def __init__(self, df, person_info):
        self.df = df
        self.type = "Ruhe" if "Ruhe" in person_info.get('file_type', '') else "Belastung" if "Belastung" in person_info.get('file_type', '') else "Unbekannt"
        self.person_info = person_info
        self.df.columns = ['Time in s', 'ECG Signal (mV)']  # Rename columns for consistency
        self.ecg_signal = self.df['ECG Signal (mV)'].values
        self.time = self.df['Time in s'].values

    @staticmethod
    def find_peaks(series, threshold, distance):
        peaks, _ = signal.find_peaks(series, height=threshold, distance=distance)
        return peaks

    @staticmethod
    def estimate_hr(peaks, time_in_s):
        peak_times_sec = time_in_s[peaks]
        rr_intervals = np.diff(peak_times_sec)
        heart_rate_at_peaks = 60 / rr_intervals
        heart_rate_times = peak_times_sec[1:]
        return heart_rate_times, heart_rate_at_peaks

    @staticmethod
    def make_ekg_plot(peaks, df, start_time, end_time):
        mask = (df["Time in s"] >= start_time) & (df["Time in s"] <= end_time)
        filtered_df = df[mask]
        filtered_peaks = [peak for peak in peaks if df["Time in s"].iloc[peak] >= start_time and df["Time in s"].iloc[peak] <= end_time]

        fig = px.line(filtered_df, x="Time in s", y='ECG Signal (mV)')
        fig.add_trace(go.Scatter(x=df["Time in s"].iloc[filtered_peaks], y=df["ECG Signal (mV)"].iloc[filtered_peaks], mode='markers', name='Peaks', marker=dict(color='red', size=8)))
        fig.update_layout(title='EKG über die Zeit', xaxis_title='Zeit in s', yaxis_title='EKG in mV')
        return fig
    
    @staticmethod
    def make_hf_plot(heart_rate_times, heart_rate_at_peaks, start_time, end_time):
        mask = (heart_rate_times >= start_time) & (heart_rate_times <= end_time)
        filtered_times = heart_rate_times[mask]
        filtered_hr = heart_rate_at_peaks[mask]

        df = pd.DataFrame({
            'Time in s': filtered_times,
            'Heart Rate (bpm)': filtered_hr
        })

        fig = px.line(df, x='Time in s', y='Heart Rate (bpm)')
        fig.update_layout(title='Herzfrequenz über die Zeit', xaxis_title='Zeit in s', yaxis_title='Herzfrequenz in bpm')
        return fig

    @staticmethod
    def plot_moving_average_heart_rate(heart_rate, heart_rate_time, window_size, start_time, end_time):
        mask = (heart_rate_time >= start_time) & (heart_rate_time <= end_time)
        filtered_heart_rate_time = heart_rate_time[mask]
        filtered_heart_rate = heart_rate[mask]

        if len(filtered_heart_rate) == 0:
            st.error("Nicht genügend Daten für die Berechnung des gleitenden Durchschnitts im ausgewählten Zeitbereich.")
            return go.Figure()

        smoothed_heart_rate = np.convolve(filtered_heart_rate, np.ones(window_size)/window_size, mode='valid')
        smoothed_heart_rate_time = filtered_heart_rate_time[:len(smoothed_heart_rate)]  # Zeitpunkte entsprechend anpassen

        df = pd.DataFrame({
            'Time in s': smoothed_heart_rate_time,
            'Smoothed Heart Rate (bpm)': smoothed_heart_rate
        })

        title = f"Geglättete Herzfrequenz über die Zeit (Gleitender Durchschnitt, Fenstergröße={window_size})"
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Time in s'], y=df['Smoothed Heart Rate (bpm)'], mode='lines+markers', name='Geglättete Herzfrequenz (bpm)'))
        fig.update_layout(
            title=title,
            xaxis_title='Zeit (s)',
            yaxis_title='Geglättete Herzfrequenz (bpm)',
            margin=dict(l=40, r=40, t=40, b=80),
        )
        
        explanation_text = (
            f"**Fenstergröße**: Die Anzahl der Datenpunkte, die im gleitenden Durchschnitt enthalten sind. "
            f"Eine Fenstergröße von {window_size} bedeutet, dass der Durchschnitt über {window_size} aufeinanderfolgende "
            f"Datenpunkte berechnet wird. Dies hilft, kurzfristige Schwankungen zu glätten und den zugrunde liegenden Trend deutlicher zu machen."
        )

        st.write(explanation_text)

        return fig
