import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclib
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import time

# Constants
NEWS_API_KEY = "YOUR_NEWS_API_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("voice", "com.apple.speech.synthesis.voice.Alex")  # Use Mac's built-in voice

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Pygame Mixer for TTS
pygame.mixer.init()


def speak(text):
    """Convert text to speech using gTTS and play it."""
    try:
        tts = gTTS(text)
        tts.save("speech.mp3")

        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)  # Prevents CPU overload
    except Exception as e:
        print(f"[ERROR] TTS failed: {e}")


def ai_process(command):
    """Handles AI-based responses using OpenAI."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Assistant."},
                {"role": "user", "content": command}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR] AI processing failed: {e}"


def fetch_news():
    """Fetches top news headlines and speaks them."""
    try:
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}")
        response.raise_for_status()  # Raise an error for HTTP issues
        articles = response.json().get("articles", [])

        if not articles:
            speak("No news found at the moment.")
            return

        for article in articles[:5]:  # Limit to 5 headlines
            speak(article["title"])
            time.sleep(1)

    except requests.RequestException as e:
        speak(f"[ERROR] Failed to fetch news: {e}")


def process_command(command):
    """Processes user voice commands and executes actions."""
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
    elif "open linkedin" in command:
        webbrowser.open("https://www.linkedin.com")
    elif command.startswith("play"):
        song = command.split(" ", 1)[-1]
        link = musiclib.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in library.")
    elif "news" in command:
        fetch_news()
    else:
        speak(ai_process(command))  # Default to AI response


def listen_for_command():
    """Listens for the wake word 'Jarvis' and executes commands."""
    with sr.Microphone() as source:
        print("Listening for 'Jarvis'...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            wake_word = recognizer.recognize_google(audio).lower()
            if wake_word == "jarvis":
                speak("Yes Sir")
                print("Jarvis Activated")

                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                process_command(command)

        except sr.UnknownValueError:
            print("[INFO] Could not understand audio.")
        except sr.RequestError as e:
            print(f"[ERROR] Speech recognition request failed: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")


if __name__ == "__main__":
    speak("Initializing Jarvis")
    while True:
        listen_for_command()
