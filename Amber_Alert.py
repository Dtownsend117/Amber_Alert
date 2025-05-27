import requests
import xml.etree.ElementTree as ET
import pyttsx3
import webbrowser
import speech_recognition as sr

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")

engine.setProperty("voice", voices[3].id)
engine.setProperty("rate", 170)
engine.setProperty("volume", 1)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def listen():
    """
    Listen to user's verbal response and convert it to text.
    Returns the recognized text, or None if recognition fails.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your response...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results from speech recognition service.")
        return None

class AmberAlerts:
    """
    A simple Python module to fetch and display current Amber Alerts in the US.
    Uses the official NCMEC Amber Alert RSS feed.
    """

    FEED_URL = "https://servicesq.dps.ohio.gov/AmberAlert/" # Change to the site you want

    def __init__(self):
        pass

    def fetch_alerts(self):
        """
        Fetch the Amber Alerts RSS feed and parse the alerts.
        Returns a list of dictionaries containing alert details.
        """
        try:
            response = requests.get(self.FEED_URL)
            response.raise_for_status()
            xml_root = ET.fromstring(response.content)

            alerts = []
            for item in xml_root.findall('./channel/item'):
                alert = {
                    'title': item.findtext('title'),
                    'description': item.findtext('description'),
                    'link': item.findtext('link'),
                    'pubDate': item.findtext('pubDate')
                }
                alerts.append(alert)
            return alerts
        except requests.RequestException as e:
            print(f"Error fetching Amber Alerts: {e}")
            return []
        except ET.ParseError as e:
            print(f"Error parsing Amber Alerts feed: {e}")
            return []

    def display_alerts(self):
        """
        Fetch and display Amber Alerts in a readable format.
        """
        alerts = self.fetch_alerts()
        if not alerts:
            print("No current Amber Alerts found.")
            speak("There are no current alerts.")
            speak("Please check the official site for updates.")
        else:
            print("=== Current Amber Alerts ===\n")
            for idx, alert in enumerate(alerts, start=1):
                print(f"Alert #{idx}: {alert['title']}")
                print(f"Date: {alert['pubDate']}")
                print(f"Details: {alert['description']}")
                print(f"More info: {alert['link']}")
                print("-" * 40)
            speak("Here are the current Amber Alerts.")

        self.ask_open_website()

    def ask_open_website(self):
        """
        Ask the user if they would like to open the official Amber Alert website.
        Supports both verbal and text input.
        """
        speak("Would you like to see the website?")
        print("Do you want to see the website?")
        
        response = listen()
        if response is None:
            response = input("Could not understand your voice. Please type yes or no: ").strip().lower()
        else:
            if response not in ['yes', 'no', 'y', 'n', 'sure', 'nope', 'absolutely', 'definitely', 'no way', 'not at all']:
                print("Did you mean yes or no? Please type your answer.")
                response = input("Type yes or no: ").strip().lower()

        if response in ['yes', 'y']:
            webbrowser.open("https://ohioamberplan.org/") # Change to the site you want
            speak("Opening the official Amber Alert website for you.")
        else:
            print("No problem, lets keep working.")

if __name__ == "__main__":
    amber_alerts = AmberAlerts()
    amber_alerts.display_alerts()

