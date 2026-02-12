import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import time
import winsound
import re
import pywhatkit
import random
from dateutil import parser

# ========== SPEECH ENGINE SETUP ==========
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# ========== LISTEN FROM MICROPHONE ==========
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio, language='en-in')
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            speak("You didn’t say anything.")
        except sr.UnknownValueError:
            speak("I couldn’t understand what you said.")
        except sr.RequestError:
            speak("I’m having trouble connecting to the speech service.")
        return ""

# ========== GREETING ==========
def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning Boss!")
    elif 12 <= hour < 17:
        speak("Good afternoon Boss!")
    elif 17 <= hour < 20:
        speak("Good evening Boss!")
    else:
        speak("Good night Boss!")
    speak("How may I help you today?")

# ========== TELL A JOKE ==========
def tell_joke():
    # List of natural-sounding jokes
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "I told my computer I needed a break, and it froze.",
        "Why don’t oysters donate to charity? Because they’re shellfish.",
        "I used to play piano by ear, but now I use my hands.",
        "I can’t trust stairs, they’re always up to something.",
        "I told my friend 10 jokes to make him laugh. Sadly, no pun in 10 did."
    ]

    joke = random.choice(jokes)  # Randomly select a joke
    speak(joke)

# ========== TIME & DATE ==========
def tell_time():
    time_now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {time_now}")

def tell_date():
    today = datetime.datetime.today()
    speak(f"Today is {today.strftime('%B %d, %Y')}")

# ========== OPEN APP ==========
def open_app(app_name):
    speak(f"Looking for {app_name} on your system...")
    search_paths = ["C:\\Program Files", "C:\\Program Files (x86)", "C:\\Windows", "C:\\Users"]
    app_name_lower = app_name.lower()
    found_path = None

    for directory in search_paths:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if app_name_lower in file.lower() and file.lower().endswith((".exe", ".lnk")):
                    found_path = os.path.join(root, file)
                    break
            if found_path:
                break
        if found_path:
            break

    if found_path:
        try:
            os.startfile(found_path)
            speak(f"Opening {app_name}")
        except Exception as e:
            speak("I found it, but couldn't open it. Trying in browser instead.")
            webbrowser.open(f"https://www.google.com/search?q={app_name}")
    else:
        speak(f"I couldn't find {app_name}. Let me search it online.")
        webbrowser.open(f"https://www.google.com/search?q={app_name}")

# ========== YOUTUBE ==========
def play_youtube(song):
    pywhatkit.playonyt(song)
    speak(f"Playing {song} on YouTube")

# ========== ALARM ==========
def set_alarm():
    speak("At what time should I set the alarm? For example, say 7:30 AM or 19:30.")
    alarm_time_str = listen()
    try:
        alarm_time = parser.parse(alarm_time_str).time()
        speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}")
        while True:
            now = datetime.datetime.now().time()
            if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
                speak("Time to wake up!")
                winsound.Beep(1000, 2000)
                break
            time.sleep(1)
    except Exception as e:
        print("Alarm Error:", e)
        speak("Sorry, I couldn't understand the time format. Try again like 7:30 AM or 19:30.")

# ========== TIMER ==========
def set_timer():
    speak("For how long should I set the timer? For example, say 10 seconds or 2 minutes.")
    response = listen()
    try:
        seconds = 0
        if "second" in response:
            seconds = int(re.findall(r'\d+', response)[0])
        elif "minute" in response:
            seconds = int(re.findall(r'\d+', response)[0]) * 60
        elif "hour" in response:
            seconds = int(re.findall(r'\d+', response)[0]) * 3600
        else:
            seconds = int(re.findall(r'\d+', response)[0])

        speak(f"Timer set for {seconds} seconds.")
        while seconds:
            mins, secs = divmod(seconds, 60)
            print(f"⏳ {mins:02d}:{secs:02d}", end="\r")
            time.sleep(1)
            seconds -= 1
        speak("Time's up!")
        winsound.Beep(1000, 2000)
    except Exception as e:
        print("Timer Error:", e)
        speak("Sorry, I couldn't understand the duration. Try something like 1 minute or 30 seconds.")

# ========== MAIN LOOP ==========
def main():
    greet_user()
    while True:
        query = listen()
        if not query:
            continue

        if "tell me a joke" in query or "joke" in query:
            tell_joke()
        elif "set timer" in query or "start timer" in query:
            set_timer()
        elif "set alarm" in query or "make alarm" in query:
            set_alarm()
        elif "send email" in query:
            speak("Who is the recipient?")
            to = listen()
            speak("What's the subject?")
            subject = listen()
            speak("What should I say?")
            body = listen()
            send_email(to, subject, body)
        elif "play" in query and "song" in query:
            speak("Which song would you like me to play?")
            song = listen()
            play_youtube(song)
        elif "open" in query:
            app = query.replace("open", "").strip()
            open_app(app)
        elif "weather" in query:
            speak("Which city?")
            city = listen()
            get_weather(city)
        elif "time" in query:
            tell_time()
        elif "date" in query:
            tell_date()
        elif "exit" in query or "stop" in query:
            speak("Goodbye Boss!")
            break

if __name__ == "__main__":
    main()
