import json
import datetime

class Person:
    
    @staticmethod
    def lade_personen_daten():
        """Eine Funktion, die weiß, wo sich die Personendatenbank befindet, und ein Wörterbuch mit den Personen zurückgibt."""
        datei = open("data/person_db.json")
        personen_daten = json.load(datei)
        return personen_daten

    @staticmethod
    def lade_mit_id(id):
        """Eine Funktion, die eine Person anhand der ID lädt."""
        personen_daten = Person.lade_personen_daten()
        for eintrag in personen_daten:
            if eintrag["id"] == id:
                return Person(eintrag)     
        raise ValueError("Person mit der ID {} nicht gefunden".format(id))                             

    @staticmethod
    def get_personen_liste(personen_daten):
        """Eine Funktion, die das Personen-Wörterbuch nimmt und eine Liste aller Personennamen zurückgibt."""
        namen_liste = []

        for eintrag in personen_daten:
            namen_liste.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return namen_liste
    
    @staticmethod
    def finde_personen_daten_nach_name(suchstring):
        """Eine Funktion, der Nachname, Vorname als ein String übergeben wird und die die Person als Wörterbuch zurückgibt."""
        personen_daten = Person.lade_personen_daten()
        if suchstring == "None":
            return {}

        zwei_namen = suchstring.split(", ")
        vorname = zwei_namen[1]
        nachname = zwei_namen[0]

        for eintrag in personen_daten:
            if eintrag["lastname"] == nachname and eintrag["firstname"] == vorname:
                return eintrag
        else:
            return {}

    @staticmethod
    def berechne_alter(geburtsdatum):
        """Alter berechnen mit dem Geburtsdatum als Eingabe."""
        heute = datetime.date.today()
        alter = heute.year - geburtsdatum
        return alter

    @staticmethod
    def berechne_max_hr(alter: int) -> int:
        """Maximale Herzfrequenz anhand des Alters berechnen."""
        max_hr_bpm =  223 - 0.9 * alter
        return int(max_hr_bpm)
    
    @staticmethod 
    def get_ekg_liste(personen_daten):
        """Eine Funktion, die das Personen-Wörterbuch nimmt und eine Liste aller EKGs zurückgibt."""
        ekg_liste = []
        for eintrag in personen_daten:
            ekg_tests = eintrag.get("ekg_tests", [])  # Liste der ekg_tests abrufen oder eine leere Liste, wenn sie nicht existiert
            for ekg_test in ekg_tests:
                ekg_id = ekg_test.get("id")
                ekg_datum = ekg_test.get("date")
                ekg_liste.append((ekg_id, ekg_datum))
        return ekg_liste

    @staticmethod
    def ekgs_von_person(personen_daten, id): 
        """Eine Funktion, die das Personen-Wörterbuch und eine ID nimmt und die ekg_tests für diese ID zurückgibt."""
        ekgs_liste_von_person = []
        ekg_ids_liste = []
        try:
            for eintrag in personen_daten:
                if eintrag["id"] == id:
                    ekg_tests = eintrag.get("ekg_tests")
                    for ekg_test in ekg_tests:
                        ekg_id = ekg_test.get("id")
                        ekg_datum = ekg_test.get("date")
                        ekgs_liste_von_person.append("EKG-ID: {} am {} ".format(ekg_id, ekg_datum))
                        ekg_ids_liste.append(ekg_id)
                    return ekg_ids_liste
            return []
        except:
            return []

    def __init__(self, personen_dict) -> None:
        self.geburtsdatum = personen_dict["date_of_birth"]
        self.vorname = personen_dict["firstname"]
        self.nachname = personen_dict["lastname"]
        self.bild_pfad = personen_dict["picture_path"]
        self.id = personen_dict["id"]
        self.alter = self.berechne_alter(self.geburtsdatum)
        self.max_hr_bpm = self.berechne_max_hr(self.alter)

if __name__ == "__main__":
    print("Dies ist ein Modul mit einigen Funktionen zum Lesen der Personendaten")
    personen = Person.lade_personen_daten()
    personen_namen = Person.get_personen_liste(personen)
    print(personen_namen)
