import json
import pandas as pd
import plotly.graph_objects as go

# Klasse EKG-Daten für die Spitzenfindung

class EKGDaten:

    def __init__(self, personen_id:int, ekg_id:int):
        # Laden der Datenbank
        db = json.load(open("data/person_db.json"))
        person = None
        
        # Suchen der Person anhand der ID
        for p in db:
            if p['id'] == personen_id:
                person = p
                break
        
        if not person:
            raise ValueError("Person nicht gefunden")
        
        ekg_dict = None
        
        # Suchen des EKG-Tests anhand der ID
        for ekg in person['ekg_tests']:
            if ekg['id'] == ekg_id:
                ekg_dict = ekg
                break
        
        if not ekg_dict:
            raise ValueError("EKG-Test nicht gefunden")
        
        self.id = ekg_dict["id"]
        self.datum = ekg_dict["date"]
        self.daten = ekg_dict["result_link"]
        self.df = pd.read_csv(self.daten, sep='\t', header=None, names=['EKG in mV', 'Zeit in ms'])

    def finde_spitzen(self, schwelle:float, respacing_faktor:int=5):
        """
        Funktion zum Finden der Spitzen in einer Serie
        Argumente:
            - schwelle (float): Die Schwelle für die Spitzen
            - respacing_faktor (int): Der Faktor zum Neuanordnen der Serie
        Rückgabe:
            - self.spitzen (list): Eine Liste der Indizes der Spitzen
        """
        # Neuanordnen der Serie
        serie = self.df["EKG in mV"].iloc[::respacing_faktor]
        # Filtern der Serie
        serie = serie[serie > schwelle]

        self.spitzen = []
        letztes = 0
        aktuelles = 0
        nächstes = 0

        for index, wert in serie.items():
            letztes = aktuelles
            aktuelles = nächstes
            nächstes = wert

            if letztes < aktuelles and aktuelles >= nächstes and aktuelles > schwelle:
                self.spitzen.append(index - respacing_faktor)

        return self.spitzen

    def schätze_hr(self):
        """
        Schätzen der Herzfrequenz aus den gefundenen R-Spitzen in den EKG-Daten
        Argumente:
        Rückgabe:
            - self.hr_pds (pd.Series): Eine Pandas-Serie mit den Herzfrequenzwerten
        """
        if not hasattr(self, 'spitzen'):
            raise ValueError("Keine Spitzen gefunden - bitte zuerst finde_spitzen() ausführen")
        
        hr_liste = []
        for i in range(1, len(self.spitzen)):
            zeit_delta_ms = self.df['Zeit in ms'].iloc[self.spitzen[i]] - self.df['Zeit in ms'].iloc[self.spitzen[i-1]]
            hr_liste.append(60000 / zeit_delta_ms)

        self.hr_pds = pd.Series(hr_liste, name="HR", index=self.spitzen[1:])
        return self.hr_pds

    def plot_zeitreihe(self):
        """
        Plotten der EKG-Daten mit den gefundenen Spitzen
        Argumente:
        Rückgabe:
            - self.zeitreihe (plotly.graph_objects.Figure): Eine Plotly-Figur mit den EKG-Daten
        """
        self.zeitreihe = go.Figure(data=go.Scatter(x=self.df["Zeit in ms"] / 1000, y=self.df["EKG in mV"]))
        r_spitzen = go.Scatter(x=self.df["Zeit in ms"].iloc[self.spitzen] / 1000, y=self.df["EKG in mV"].iloc[self.spitzen], mode='markers', marker=dict(color='rot', size=8))
        self.zeitreihe.add_trace(r_spitzen)
        return self.zeitreihe

    @staticmethod
    def lade_mit_id(personen_id:int, ekg_id:int):
        ekg_dict = json.load(open("data/person_db.json"))[personen_id - 1]["ekg_tests"][ekg_id - 1]
        instance = EKGDaten(personen_id, ekg_id)
        instance.id = ekg_dict["id"]
        instance.datum = ekg_dict["date"]
        instance.daten = ekg_dict["result_link"]
        instance.df = pd.read_csv(instance.daten, sep='\t', header=None, names=['EKG in mV', 'Zeit in ms'])

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
