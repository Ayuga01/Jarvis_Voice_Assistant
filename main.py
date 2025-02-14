
import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclib
import requests
from openai import OpenAI
from gtts import gTTS
import pygame

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("voice", "com.apple.speech.synthesis.voice.Alex")  # Use Mac's built-in voice
newsapi = "API_KEY"



def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("speech.mp3")
        # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("speech.mp3")  # Replace with your MP3 file

    # Play the file
    pygame.mixer.music.play()

    # Keep the script running so the music plays completely
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Keep the loop running while music is playing

def aiProcess(command):
    client = OpenAI(api_key="API_KEY")


    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general task like alexa and google cloud."},
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musiclib.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()  # Convert response to JSON
            articles = data.get("articles", [])  # Get the list of articles
        
            
            for article in articles:
                speak(article["title"])
    else:
        # let open ai handle the command 
        output=aiProcess(c)
        speak(output)

           



if __name__ == "__main__":
    speak("Initializing Jarvis")
    #Listen for the wake word jarvis
    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()
        # recognize speech using Sphinx
        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)
            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Yes Sir")
                with sr.Microphone() as source:
                    print("Jarvis Activated")
                    audio = r.listen(source) 
                    command = r.recognize_google(audio)   

                    processCommand(command)    
        except Exception as e:
            print("Error; {0}".format(e))
       
