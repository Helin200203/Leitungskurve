# FitEKG

FitEKG ist eine Anwendung zur Überwachung und Analyse von EKG-Daten und Fitnessinformationen. Diese App bietet eine benutzerfreundliche Oberfläche zur Verwaltung und Auswertung von Gesundheitsdaten, einschließlich Herzfrequenz, BMI, und Nährwertinformationen.

## Inhaltsverzeichnis

- [FitEKG](#fitekg)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Einführung](#einführung)
  - [Installation](#installation)
  - [Verwendung](#verwendung)
  - [Konfiguration](#konfiguration)
    - [OpenAI API-Schlüssel und Assistant-ID](#openai-api-schlüssel-und-assistant-id)
  - [Beitragende](#beitragende)

## Einführung

FitEKG ist eine vielseitige Gesundheitsanwendung, die Ihnen hilft, Ihre Herzgesundheit und Fitness zu überwachen. Mit dieser App können Sie Ihre EKG-Daten hochladen und analysieren, Fitnessinformationen anzeigen und Ernährungsanalysen durchführen.

## Installation

Folgen Sie diesen Schritten, um FitEKG auf Ihrem lokalen System zu installieren:

1. **Repository klonen**:
    ```bash
    git clone https://github.com/dein-benutzername/fit-ekg.git
    cd fit-ekg
    ```

2. **Virtuelle Umgebung erstellen**:
    Erstellen Sie eine virtuelle Umgebung, um Abhängigkeiten isoliert zu installieren:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Auf Windows: venv\Scripts\activate
    ```

3. **Abhängigkeiten installieren**:
    Installieren Sie alle notwendigen Python-Pakete mit pip:
 
   ```bash
    pip install -r requirements.txt
    ```

## Verwendung

1. **Streamlit-Anwendung starten**:
    Starten Sie die Anwendung mit dem folgenden Befehl:

    ```bash
    streamlit run app.py
    ```

2. **Öffnen Sie die Anwendung**:
    Öffnen Sie Ihren Webbrowser und gehen Sie zu `http://localhost:8501`, um die Streamlit-Anwendung zu verwenden.

3. **API-Schlüssel und Assistant-ID eingeben**:
    - Sobald die Anwendung geladen ist, geben Sie Ihren OpenAI API-Schlüssel und die Assistant-ID ein, um die Funktionen der App nutzen zu können.

## Konfiguration

### OpenAI API-Schlüssel und Assistant-ID

1. **API-Schlüssel und Assistant-ID in der Anwendung eingeben**:
    - Öffnen Sie die Streamlit-Anwendung im Browser.
    - Geben Sie Ihren OpenAI API-Schlüssel und die Assistant-ID in die entsprechenden Felder ein.

2. **API-Schlüssel und Assistant-ID in den Quellcode einfügen**:
    - Alternativ können Sie den API-Schlüssel und die Assistant-ID direkt im Quellcode einfügen, um sie fest zu hinterlegen:
  
    ```python
    import openai

    openai.api_key = "dein-openai-api-schluessel"
    assistant_id = "deine-assistant-id"
    ```

## Beitragende

Helin Hussein und Jonny Hermann
