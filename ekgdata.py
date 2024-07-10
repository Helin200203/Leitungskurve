import json
import pandas as pd
import plotly.graph_objects as go

class EKGDaten:

    def __init__(self, personen_id: int, ekg_id: int):
        # Laden der Datenbank
        try:
            with open("data/person_db.json") as file:
                db = json.load(file)
        except FileNotFoundError:
            raise ValueError("Datenbankdatei nicht gefunden")
        
        person = next((p for p in db if p['id'] == personen_id), None)
        if not person:
            raise ValueError("Person nicht gefunden")
        
        ekg_dict = next((ekg for ekg in person['ekg_tests'] if ekg['id'] == ekg_id), None)
        if not ekg_dict:
            raise ValueError("EKG-Test nicht gefunden")
        
        self.id = ekg_dict["id"]
        self.datum = ekg_dict["date"]
        self.daten = ekg_dict["result_link"]
        
        try:
            self.df = pd.read_csv(self.daten, sep='\t', header=None, names=['EKG in mV', 'Zeit in ms'])
        except FileNotFoundError:
            raise ValueError("EKG-Datendatei nicht gefunden")

    def finde_spitzen(self, schwelle: float, respacing_faktor: int = 5):
        serie = self.df["EKG in mV"].iloc[::respacing_faktor]
        serie = serie[serie > schwelle]

        self.spitzen = []
        letztes, aktuelles, nächstes = 0, 0, 0

        for index, wert in serie.items():
            letztes, aktuelles, nächstes = aktuelles, nächstes, wert
            if letztes < aktuelles and aktuelles >= nächstes and aktuelles > schwelle:
                self.spitzen.append(index * respacing_faktor)

        return self.spitzen

    def schätze_hr(self):
        """
        Schätzen der Herzfrequenz aus den gefundenen R-Spitzen in den EKG-Daten
        Argumente:
        Rückgabe:
            - self.hr_pds (pd.Series): Eine Pandas-Serie mit den Herzfrequenzwerten
        """
        if not hasattr(self, 'spitzen') or len(self.spitzen) < 2:
            raise ValueError("Keine ausreichenden Spitzen gefunden - bitte zuerst finde_spitzen() ausführen")
        
        hr_liste = []
        spitzen_index = []

        for i in range(1, len(self.spitzen)):
            if self.spitzen[i] < len(self.df) and self.spitzen[i-1] < len(self.df):
                zeit_delta_ms = self.df['Zeit in ms'].iloc[self.spitzen[i]] - self.df['Zeit in ms'].iloc[self.spitzen[i-1]]
                hr_liste.append(60000 / zeit_delta_ms)
                spitzen_index.append(self.spitzen[i])

        if len(hr_liste) == 0:
            raise ValueError("Herzfrequenz konnte nicht geschätzt werden - überprüfen Sie die Spitzenfindung")
        
        self.hr_pds = pd.Series(hr_liste, name="HR", index=spitzen_index)
        return self.hr_pds

    def plot_zeitreihe(self):
        """
        Plotten der EKG-Daten mit den gefundenen Spitzen
        Argumente:
        Rückgabe:
            - self.zeitreihe (plotly.graph_objects.Figure): Eine Plotly-Figur mit den EKG-Daten
        """
        self.zeitreihe = go.Figure(data=go.Scatter(x=self.df["Zeit in ms"] / 1000, y=self.df["EKG in mV"]))
        r_spitzen = go.Scatter(x=self.df["Zeit in ms"].iloc[self.spitzen] / 1000, y=self.df["EKG in mV"].iloc[self.spitzen], mode='markers', marker=dict(color='red', size=8))
        self.zeitreihe.add_trace(r_spitzen)
        return self.zeitreihe

    @staticmethod
    def lade_mit_id(personen_id: int, ekg_id: int):
        try:
            ekg_dict = json.load(open("data/person_db.json"))[personen_id - 1]["ekg_tests"][ekg_id - 1]
        except (FileNotFoundError, IndexError, KeyError):
            raise ValueError("Fehler beim Laden der EKG-Daten")

        instance = EKGDaten(personen_id, ekg_id)
        instance.id = ekg_dict["id"]
        instance.datum = ekg_dict["date"]
        instance.daten = ekg_dict["result_link"]
        try:
            instance.df = pd.read_csv(instance.daten, sep='\t', header=None, names=['EKG in mV', 'Zeit in ms'])
        except FileNotFoundError:
            raise ValueError("EKG-Datendatei nicht gefunden")

        return instance

if __name__ == "__main__":
    print("Dies ist ein Modul mit einigen Funktionen zum Lesen der EKG-Daten")

    print('Erstellen eines EKGDaten-Objekts')
    ekg = EKGDaten(2, 3)

    print('Spitzen finden')
    ekg.finde_spitzen(340, 4)
    print(ekg.spitzen[:10])

    print('Herzfrequenz schätzen')
    print(ekg.schätze_hr()[:10])

    print('Plotten')
    ekg.plot_zeitreihe().show()

    fig_hr = go.Figure(data=go.Scatter(x=ekg.hr_pds.index, y=ekg.hr_pds))
    fig_hr.show()
