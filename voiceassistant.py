import datetime
import subprocess
import webbrowser
import pyttsx3
import speech_recognition as sr
import wikipedia
import pyjokes

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window

Window.size = (550, 450)
Window.clearcolor = (0.3, 0.3, 0.3, 1)
Window.title = "Jame Assistant"

# --- Голосовий асистент ---

def speak(text):
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    except:
        print("Speech output not supported in Colab")


def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning Yasha!")
    elif hour < 18:
        speak("Good Afternoon Yasha!")
    else:
        speak("Good Evening Yasha!")
    speak("I am your voice assistant. How can I help you today?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="uk-UA")
        print(f"Your said: {query}")
    except FileNotFoundError:
        print("Sorry, I did not catch that. Please try again.")
        return "none"

    return query.lower()

def run_assistant():
    wish_user()
    while True:
        query = take_command()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia: ")
                speak(result)
            except:
                speak("Sorry, i couldn't find anything")

        elif 'open spotify' in query:
            speak("Opening Spotify...")
            webbrowser.open("https://open.spotify.com/")

        elif 'open youtube' in query:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com/")

        elif 'open firefox' in query:
            speak("Opening FireFox...")
            subprocess.Popen(["open", "-a" "FireFox"])

        elif 'open pycharm' in query:
            speak("Opening PyCharm...")
            subprocess.Popen(["open", "-a", "PyCharm"])

        #elif 'time' in query:
            #strTime = datetime.datetime.now().strftime("%H:%M:%S")
            #speak(f"The current time is {strTime}")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'Goodbye' in query or 'bye' in query:
            speak("Goodbye! Have a nice day ")
            break

        else:
            speak("Sorry, iI didn't understand that. Try again.")

# --- Kivy інтерфейс ---
class Myassistant(App):

    def build(self):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(text="Вас вітає\nJame assistant!", color=(0, 0, 0, 1), halign='center')
        btn = Button(text="Тисни на мене!", background_color=(0.2, 0.4, 1, 1))
        btn.bind(on_press=lambda x: run_assistant())
        commands = Label(text="Команди:\n- wikipedia\n- open firefox\n- open youtube\n- open spotify\n- open pycharm\n- Goodbye")
        box.add_widget(label)
        box.add_widget(btn)
        box.add_widget(commands)

        return box


if __name__ == "__main__":
    Myassistant().run().run_assistant()


