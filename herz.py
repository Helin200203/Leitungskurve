
from streamlit import st


def heart_info():
    st.title("Informationen über das Herz und EKG-Daten")

    st.write('''
    #### Das Herz: Unser lebenswichtiges Organ

    Das Herz ist ein Muskel, der als Pumpe fungiert, um Blut durch den gesamten Körper zu transportieren. Es besteht aus vier Kammern: zwei Vorhöfen und zwei Ventrikeln. Durch regelmäßige Kontraktionen sorgt das Herz dafür, dass Sauerstoff und Nährstoffe in alle Körperzellen gelangen.

    ##### Herzstruktur:
    - **Vorhöfe (Atrien)**: Obere Kammern, die Blut aus dem Körper und der Lunge empfangen.
    - **Ventrikel**: Untere Kammern, die das Blut in den Körper und die Lunge pumpen.
    - **Herzklappen**: Sorgen dafür, dass das Blut in die richtige Richtung fließt.

    ![Herzstruktur](https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Diagram_of_the_human_heart_%28cropped%29.svg/800px-Diagram_of_the_human_heart_%28cropped%29.svg.png)

    #### Das Elektrokardiogramm (EKG)

    Ein EKG ist eine einfache und schmerzlose Untersuchung, die die elektrische Aktivität des Herzens aufzeichnet. Es gibt wichtige Hinweise auf die Herzgesundheit und kann helfen, verschiedene Herzkrankheiten zu diagnostizieren.

    ##### Wichtige EKG-Komponenten:
    - **P-Welle**: Zeigt die elektrische Aktivität der Vorhöfe.
    - **QRS-Komplex**: Stellt die Erregung der Ventrikel dar.
    - **T-Welle**: Zeigt die Erholungsphase der Ventrikel.

    ![EKG-Daten](https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/SinusRhythmLabels.svg/1024px-SinusRhythmLabels.svg.png)

    #### EKG-Daten verstehen

    Ein typisches EKG besteht aus mehreren Zyklen von Wellen und Intervallen. Diese beinhalten:

    - **Herzfrequenz**: Die Anzahl der Herzschläge pro Minute.
    - **Rhythmus**: Regelmäßigkeit der Herzschläge.
    - **Amplitude**: Höhe der Wellen, die die Stärke der elektrischen Signale anzeigen.
    - **Dauer der Intervalle**: Zeiträume zwischen den verschiedenen Wellen, die auf die Effizienz des Herzschlags hinweisen.

    ##### Beispiel einer EKG-Auswertung:
    - **Normale Herzfrequenz**: 60-100 Schläge pro Minute.
    - **Sinusrhythmus**: Regelmäßiger und normaler Herzrhythmus.

    ### Fazit

    Das Herz und die EKG-Daten liefern wichtige Informationen über Ihre Herzgesundheit. Mit einem EKG können potenzielle Probleme frühzeitig erkannt und behandelt werden. Nutzen Sie diese Informationen, um Ihre Gesundheit zu überwachen und bei Bedarf medizinische Hilfe in Anspruch zu nehmen.
    ''')
