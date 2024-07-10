import streamlit as st
from openai import OpenAI
import time

import app


def show_ki_page():
    st.title("KI-Funktionen")
    st.write("Beschreibung der KI-Funktionalitäten")
    
    app()