import subprocess
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import threading
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import wikipedia
import smtplib
import requests
import pygame
from pygame import mixer

# Initialize pygame mixer safely
try:
    pygame.mixer.init()
except Exception as e:
    print("⚠️ Error initializing mixer:", e)

# ---------------- SPEAK FUNCTION ---------------- #
def speak(text, voice_id=1):
    """Speak text using pyttsx3"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if 0 <= voice_id < len(voices):
            engine.setProperty('voice', voices[voice_id].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Speech Error:", e)
        print(f"DHRUVA: {text}")

# ---------------- MUSIC FUNCTIONS ---------------- #
def play_exit_song():
    path = r"D:\new python\Thanos reality stone.mp3"
    if os.path.exists(path):
        subprocess.run(["start", "wmplayer", path], shell=True)
    else:
        print("Exit song not found:", path)

def play_background_music():
    try:
        path = r"D:\new python\Thanos Destiny.mp3"
        if os.path.exists(path):
            mixer.music.load(path)
            mixer.music.set_volume(0.5)
            mixer.music.play(-1)  # loop background music
        else:
            print("Background music not found:", path)
    except Exception as e:
        print("Music error:", e)

# ---------------- GIF DISPLAY ---------------- #
def play_gif():
    try:
        root = Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")
        gif_path = r"D:\new python\what-if-marvel-studios.gif"
        if not os.path.exists(gif_path):
            print("GIF not found:", gif_path)
            return

        img = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame.resize((screen_width, screen_height)))
                  for frame in ImageSequence.Iterator(img)]

        lbl = Label(root)
        lbl.place(x=0, y=0)

        def update_frame(idx=0):
            lbl.config(image=frames[idx])
            root.update()
            if idx + 1 < len(frames):
                root.after(50, lambda: update_frame(idx + 1))
            else:
                root.after(2000, root.destroy)

        root.after(2000, update_frame)
        root.mainloop()
    except Exception as e:
        print("GIF error:", e)

# ---------------- WEATHER ---------------- #
def get_weather(city):
    api_key = '76117e892a1559cf109230e958f1892c'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    try:
        response = requests.get(base_url, params=params)
        weather_data = response.json()
        if response.status_code == 200:
            temp = weather_data['main']['temp']
            desc = weather_data['weather'][0]['description']
            speak(f'The current temperature in {city} is {temp}°C with {desc}.')
        else:
            speak(f"Error: {weather_data.get('message', 'unknown error')}")
    except Exception as e:
        print("Weather error:", e)
        speak("Sorry, I could not fetch the weather data.")

# ---------------- FAVORITE SONG ---------------- #
def play_favorite_song():
    path = r"C:\Users\pande\Music\old_Kalakaar-Neele Neele Ambar.mp3"
    if os.path.exists(path):
        os.startfile(path)
    else:
        speak("Favorite song not found.")

# ---------------- ASSISTANT CORE ---------------- #
def run_assistant():
    recognizer = sr.Recognizer()

    def listen():
        """Try to listen from mic, fallback to text input if PyAudio not found"""
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            try:
                print("Recognizing...")
                query = recognizer.recognize_google(audio)
                print(f"User: {query}")
                return query.lower()
            except sr.UnknownValueError:
                speak("Sorry, I didn't get that.")
                return ""
            except sr.RequestError:
                speak("Speech service unavailable.")
                return ""
        except Exception as mic_error:
            print("⚠️ Mic not available:", mic_error)
            speak("Microphone not found. Please type your command.")
            return input("Type your command: ").lower()

    speak("Nice meeting you again! I am dhruva , your personal assistant. How can I help you today?")

    while True:
        user_input = listen()

        if not user_input:
            continue

        if "hello" in user_input:
            speak("Hi there! How can I assist you?")

        elif "play music" in user_input:
            speak("Sure, what would you like to listen to?")
            query = listen()
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")


        elif "stop music" in user_input:
            mixer.music.stop()
            speak("Music stopped.")

        elif "time" in user_input:
            speak(f"The current time is {datetime.datetime.now().strftime('%H:%M')}.")

        elif "date" in user_input:
            speak(f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}.")

        elif "search" in user_input:
            speak("What would you like to search for?")
            query = listen()
            webbrowser.open(f"https://www.google.com/search?q={query}")

        elif "tell me about" in user_input:
            speak("What would you like to know about?")
            topic = listen()
            try:
                info = wikipedia.summary(topic, sentences=2)
                speak(info)
            except Exception:
                speak(f"Sorry, I couldn’t find info about {topic}.")

        elif "weather" in user_input:
            speak("Which city?")
            city = listen()
            get_weather(city)

        elif "exit" in user_input or "quit" in user_input:
            speak("Goodbye! Before going, listen to your favorite song.")
            play_favorite_song()
            break

        else:
            speak("I'm sorry, I didn't understand that. Can you repeat?")

# ---------------- THREADING ---------------- #
if __name__ == "__main__":
    background_music_thread = threading.Thread(target=play_background_music, daemon=True)
    gif_thread = threading.Thread(target=play_gif, daemon=True)
    assistant_thread = threading.Thread(target=run_assistant, daemon=True)

    background_music_thread.start()
    gif_thread.start()
    assistant_thread.start()

    background_music_thread.join()
    gif_thread.join()
    assistant_thread.join()
