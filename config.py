import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import pywhatkit

# Text to Speech
engine = pyttsx3.init()
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# Listen Function
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="en-in").lower()
        print("You said:", command)
        return command
    except:
        return ""

# Main Program
speak("Hello, I am Jarvis. How can I help you Boss?")

while True:
    command = listen()

    if "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {time}")

    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "play song" in command or "play music" in command:
        song = command.replace("play song", "").replace("play music", "").strip()
        if song:
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            speak("Which song should I play?")

    elif "exit" in command or "quit" in command:
        speak("Goodbye Sir")
        break

    else:
        if command != "":
            speak("Sorry, I don't understand")
