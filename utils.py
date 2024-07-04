# utils.py
def berechne_bmi(gewicht, groesse):
    if groesse > 0:
        bmi = gewicht / ((groesse / 100) ** 2)
        return bmi
    else:
        raise ValueError("Größe muss größer als 0 sein.")

def berechne_kalorienbedarf(gewicht, groesse, alter, geschlecht, aktivitaetslevel):
    if geschlecht == "Männlich":
        grundumsatz = 88.36 + (13.4 * gewicht) + (4.8 * groesse) - (5.7 * alter)
    else:
        grundumsatz = 447.6 + (9.2 * gewicht) + (3.1 * groesse) - (4.3 * alter)

    if aktivitaetslevel == "Wenig aktiv":
        kalorienbedarf = grundumsatz * 1.2
    elif aktivitaetslevel == "Mäßig aktiv":
        kalorienbedarf = grundumsatz * 1.55
    elif aktivitaetslevel == "Aktiv":
        kalorienbedarf = grundumsatz * 1.725
    else:
        kalorienbedarf = grundumsatz * 1.9

    return kalorienbedarf

def bmi_bereich(bmi):
    if bmi < 18.5:
        return "Untergewicht"
    elif 18.5 <= bmi < 24.9:
        return "Normalgewicht"
    elif 25 <= bmi < 29.9:
        return "Übergewicht"
    else:
        return "Adipositas"
