import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import webbrowser
import os
import subprocess
import sys
import pywhatkit
import time 

# ---------------------- Text-to-Speech (TTS) setup ----------------------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# choose a voice index you like; 0 or 1 usually (depends on your system)
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)   # speech rate (words per minute)
engine.setProperty('volume', 1.0) # 0.0 to 1.0

def speak(text: str):
    """Speak the given text synchronously."""
    engine.say(text)
    engine.runAndWait()

# ---------------------- Speech Recognition setup ----------------------
recognizer = sr.Recognizer()
mic = sr.Microphone()

def take_command(timeout=5, phrase_time_limit=8):
    """
    Listen from the microphone and return recognized text (lowercased).
    Returns None if nothing recognized.
    """
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return None

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')  # use 'en-in' or 'en-US'
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        speak("Sorry, I can't reach the speech recognition service.")
        return None

# ---------------------- Utility functions ----------------------
def wish_me():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        speak("Good morning. I am Jarvis. How can I help you?")
    elif 12 <= hour < 17:
        speak("Good afternoon. I am Jarvis. How can I help you?")
    elif 17 <= hour < 21:
        speak("Good evening. I am Jarvis. How can I help you?")
    else:
        speak("Hello. I am Jarvis. I'm here to help you.")

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")
    return now

def search_wikipedia(query, sentences=2):
    try:
        results = wikipedia.summary(query, sentences=sentences, auto_suggest=True, redirect=True)
        speak("According to Wikipedia")
        speak(results)
        return results
    except Exception as e:
        speak("Sorry, I couldn't find that on Wikipedia.")
        return None

def open_website(site: str):
    if not site.startswith("http"):
        site = "https://www." + site
    webbrowser.open(site)
    speak(f"Opening {site}")

def play_on_youtube(search: str):
    speak(f"Playing {search} on YouTube")
    pywhatkit.playonyt(search)
    
# Removed invalid/incomplete function definition for play_on-spotify

def open_file_or_app(path: str):
    """
    Attempt to open file/folder/application. Use absolute paths for reliability.
    On Windows, path could be "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    """
    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        speak("Opened.")
    except Exception as e:
        speak("Unable to open that path.")
        print(e)

# ---------------------- Command processing ----------------------
def process_command(command: str):
    if not command:
        return False  # no command processed

    # Wake word handling (optional): use "jarvis" as wake word.
    if "jarvis" in command:
        # strip wake word for action parsing:
        command = command.replace("jarvis", "").strip()

    # Exit
    if any(kw in command for kw in ["exit", "quit", "goodbye", "stop listening", "shutdown"]):
        speak("Goodbye. Have a nice day.")
        return "exit"

    # Time
    if "time" in command:
        tell_time()
        return True

    # Greeting
    if any(kw in command for kw in ["hello", "hi", "hey"]):
        speak("Hello. How can I help you?")
        return True

    # Wikipedia search
    if command.startswith("who is") or command.startswith("what is") or "wikipedia" in command:
        # clean command
        query = command.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
        if query:
            search_wikipedia(query)
            return True
        else:
            speak("What should I search on Wikipedia?")
            return True

    # Open website
    if command.startswith("open "):
        target = command.replace("open ", "").strip()
        # handle some natural phrases
        if "youtube" in target:
            open_website("youtube.com")
        elif "google" in target:
            open_website("google.com")
        elif "." in target or "com" in target:
            open_website(target)
        else:
            # try basic site
            open_website(target + ".com")
        return True

    # Play music or a YouTube video
    if command.startswith("play ") or command.startswith("play on youtube "):
        search = command.replace("play on youtube", "").replace("play", "").strip()
        if search:
            play_on_youtube(search)
        else:
            speak("What would you like me to play?")
        return True

    # Open file / application phrases
    if any(kw in command for kw in ["open folder", "open file", "open app", "open application", "run"]):
        # Example usage: "open app notepad" or "open folder C:\\Users\\You\\Music"-
        # Try to extract path or app name
        # If the user gives an absolute path just open it
        candidate = command.split(" ", 1)[1] if " " in command else ""
        candidate = candidate.strip()
        if os.path.exists(candidate):
            open_file_or_app(candidate)
        else:
            # provide simple app shortcuts for common apps (customize)
            apps = {
                "notepad": r"C:\Windows\system32\notepad.exe",
                "calculator": r"C:\Windows\System32\calc.exe",
                "cmd": r"C:\Windows\system32\cmd.exe",
            }
            for k, path in apps.items():
                if k in candidate:
                    open_file_or_app(path)
                    return True
            speak("I couldn't find that application. Please provide a full path or add it to the script.")
        return True

    # Search web
    if command.startswith("search ") or command.startswith("google "):
        query = command.replace("search", "").replace("google", "").strip()
        if query:
            speak(f"Searching the web for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return True

    # Say a simple joke or small talk
    if "joke" in command:
        speak("Why don't programmers like nature? It has too many bugs.")
        return True

    # If we didn't match any rule: ask or try to search
    # fallback: try Wikipedia first, else web search
    speak("I didn't understand that fully. I'll try to search the web.")
    webbrowser.open(f"https://www.google.com/search?q={command.replace(' ', '+')}")
    return True

# ---------------------- Main loop ----------------------
def run_jarvis():
    wish_me()
    speak("Say 'Jarvis' before your command, or just speak a command.")
    while True:
        query = take_command(timeout=6, phrase_time_limit=7)
        if query is None:
            # no speech recognized; continue listening
            # Optionally use a hotkey to trigger listening (e.g., press 'space')
            continue

        result = process_command(query)
        if result == "exit":
            break
        # small pause to avoid overlapping recognition
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        run_jarvis()
    except KeyboardInterrupt:
        print("\nExiting Jarvis.")
        speak("Shutting down. Goodbye.")
    except Exception as e:
        print("An error occurred:", e)
        speak("An error occurred. Please check the console for details.")
