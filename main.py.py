import pyttsx3  #text to speech module
import speech_recognition as sr  #speech recognation module
import webbrowser  #module for accessing web pages or sites
import datetime #module for accessing the current time and date
import time
import pyjokes #module for generating jokes
import requests #module for  sending request
from bs4 import BeautifulSoup #module which helps extract data from web pages
import musiclibrary #module created by me
import google.generativeai as genai #for accessing or integrating google gemeni
from selenium import webdriver    #for youtube function
from selenium.webdriver.common.by import By #for automating web browser interactions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pygame 
import random 
import json #for memory retention
import os #for accessing operating system features
import sys #for accessing system
import pyaudio
import pyuac
import yt_dlp
# pyuac.runAsAdmin()
#---------------------------------------------------------
def speak(text):
    """Converts text to speech"""
    engine = pyttsx3.init() #initilize the text to  speech  engine 
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) #0 for male and 1 for female
    engine.setProperty('rate', 156)  
    engine.setProperty('volume', 1.0)  #CHECKED full  volume 
    engine.say(text)     #text ko bolega 
    engine.runAndWait()  #jb tk pura bol nhi deta tb tk wo  wait krega
    #-----------------------------------------------------
# shutdown laptop
#-----------------------------------------------------
def shutdown_vasuki():
    print("Shutting down Vasuki and your laptop...")  #CHECKED
    os.system("shutdown /s /t 7")  # window ko  shutdown krdega in 7 seconds
    sys.exit()  # programme ko turant bnd krdega 
#-----------------------------------------------------------------------------
#setting alarm
def set_alarm(hour, minute):
    speak(f"Alarm set for {hour}:{minute}")
    while True:
        current_time = time.localtime()           #current time ko  fetch krega 
        if current_time.tm_hour == hour and current_time.tm_min == minute:        #check krega ki time hua ya nhi
            pygame.mixer.init()           #pygame mixer module ko initialise krega taki audio play back kr ske 
            pygame.mixer.music.load(r"C:\PROJECT\VASUKI\ADVANCED\all.mp3")     #ringtone load krega 
            pygame.mixer.music.play()   #ringtone play krega 
            while pygame.mixer.music.get_busy():
             pass  
  
            break
        time.sleep(30)  # Check time every 30 seconds and then again check conditions
#alarm complete
#-------------------------------------------------------------------------------
#-----------------------------------------------------------------------
#FUNCTION FOR DOWNLOADING IMAGES 
def download_image(s,filename):
  response = requests.get(s)                     #CHECKED
  with open(f"{filename}.jpg", "wb") as file:
     file.write(response.content)

#------------------------------------------------------------------------

#PAST CONVERSATION RECALLING POWER FOR VASUKI
#ABB VASUKI SB YAAD RKHEGA
filename="data.json"
def load_memory():
    try:
        with open(filename,"r") as file:
          return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
         return {"conversation":[]}
def save_memory(memory):
    with open(filename,"w") as file:
        json.dump(memory,file,indent=4)
def store_conversation(user_msg,vasuki_reply):
    memory=load_memory()
    memory["conversations"].append({"user": user_msg, "vasuki": vasuki_reply})
    save_memory(memory) 

#searching user_msg in past data 
def get_past_response(user_msg):
    memory = load_memory()  
    for convo in reversed(memory["conversations"]): 
        if user_msg.lower() in convo["user"].lower():   
            return convo["vasuki"] 
    return None   
#checking for reposnse in past data
def vasuki_reply(user_msg):
    # Check if the response exists in memory
    past_response = get_past_response(user_msg)
    if past_response:
        return f"I remember you asked this before! My answer was: {past_response}"
    
    # If no past response, generate a new one
    else:
     speak("I'm still learning! Can you tell me what should, i reply when this question is asked" )
     new_response=listen_for_command()
     store_conversation(user_msg, new_response) 
     return new_response



def conversation_mode():
    recognizer = sr.Recognizer()
    
    speak("Conversation mode on. Bol bhai, sun raha hoon...")
    
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

            text = recognizer.recognize_google(audio, language="en-IN").lower()
            print("You said:", text)

            if "close" in text or "exit" in text:  # Only stops when "close" or "exit" is said
                speak("Okay, conversation mode off!")
                break  # Exit the loop
            else:
             speak(vasuki_reply(text))  # Vasuki responds based on memory
            
        except sr.UnknownValueError:
            print("Kuch samajh nahi aaya...")

    listen_for_command()  
#-------------------------------------------------------------------------
#creating class for emotions
class Vasukii:
    def __init__(self):
        self.emotions = {
            "happy": 0,
            "sad": 0,
            "angry": 0,
            "neutral": 1  # Default state
        }
    def update_emotion(self, user_input):
        user_input = user_input.lower()

        # Positive interaction
        if any(word in user_input for word in ["good job", "thanks", "awesome", "great"]):
            self.emotions["happy"] += 2
            self.emotions["neutral"] += 1
        
        # Negative interaction
        elif any(word in user_input for word in ["useless", "bad", "stupid", "hate"]):
            self.emotions["sad"] += 2
            self.emotions["angry"] += 1
        
        # Neutral interaction
        else:
            self.emotions["neutral"] += 1
        
        # Keep values balanced
        self.normalize_emotions()

    def normalize_emotions(self):
        # Prevent extreme values
        for key in self.emotions:
            if self.emotions[key] > 10:
                self.emotions[key] = 10
            elif self.emotions[key] < 0:
                self.emotions[key] = 0

    def get_current_emotion(self):
        # Determine dominant emotion
        max_emotion = max(self.emotions, key=self.emotions.get)
        return max_emotion

    def respond(self, user_input):
        self.update_emotion(user_input)
        emotion = self.get_current_emotion()

        responses = {
            "happy": ["I'm feeling great! ", "Thanks! That made my day! "],
            "sad": ["I'm feeling a bit down... ", "That hurt a little. "],
            "angry": ["I'm not happy with that. ", "That wasn't nice. "],
            "neutral": ["I'm here to help. ", "What can I do for you? "]
        }

        speak(random.choice(responses[emotion]))
#---------------------------------------------------------------------

# == MUSIC LIBRARY DICTIONARY ==
# == Recognizer object ==
recognizer = sr.Recognizer()
newsapi="b355058d3d8844b5bd958013023f5824"  #news api key h
#gemini start
genai.configure(api_key="AIzaSyBSMGLK9ifCqHBr2tGdfgYzc1D1b2bl1wE") 
def aiProcess(command):
    # Google Gemini se jawab lenge           #CHECKED
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(command)
    return response.text if response.text else "Sorry, I couldn't process that."

      #AI SEARCHING FUNCTIONS ENDS HERE 
#----------------------------------------------------------------------------
def google_search(query):
    webbrowser.open(f"https://www.google.com/search?q={query}") #CHECKED
    return f"Searching Google for {query}..."
#------------------------------------------------------------------
def get_greeting():
    """Returns a greeting based on the time of day"""
    hour = datetime.datetime.now().hour   #hours m current time lega
    if hour < 12:
        return "Good morning!"
    elif 12 <= hour < 18: #CHECKED 
        return "Good afternoon!"
    else:
        return "Good evening!"
#------------------------------------------------------------------------
#ye function copy kiya h but smjh liya h
def search_youtube(song):
    query = song.replace(" ", "+")
    search_url = f"https://www.youtube.com/results?search_query={query}"

    # Fetch video URL using yt_dlp
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "force_generic_extractor": True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_url, download=False)
        if "entries" in info and len(info["entries"]) > 0:
            video_url = info["entries"][0]["url"]  # First video link
            print(f"Playing: {video_url}")
            webbrowser.open(video_url)  # Open in default browser
        else:
            print("No results found!")
#--------------------------------------------------------------------------------
def processcommand(c):
     """Process user command"""
     print("Command:", c)
     c = c.lower()   #text ko lower case m convert krliya
     if "open google" in c:
        webbrowser.open("https://google.com")
     elif "open chat gpt" in c or "open chat" in c:
        webbrowser.open("https://chatgpt.com")
     elif "shutdown" in c.lower():
        shutdown_vasuki()
     elif "open youtube" in c:
        webbrowser.open("https://www.youtube.com/") 
     elif "alarm" in c:
         speak("enter time for alarm")
         h=int(input("enter the hour"))
         m=int(input("enter the minute"))
         set_alarm(h,m) 
     elif "open replit" in c:
        webbrowser.open("https://replit.com/~")
     elif "open whatsapp" in c or "whatsapp" in c:
        webbrowser.open("https://web.whatsapp.com/")
     elif "created" in  c:
        speak("i am vasuki an AI VOICE ASSISTANT CREATED BY RAGHAV")
     elif "open gmail" in c or "gmail" in c:
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
     elif c.startswith("play"):
        song = c[5:].strip()  # "play" ke baad ka text extract karna
        if song in musiclibrary.music:
            speak(f"Playing {song}...")
            webbrowser.open(musiclibrary.music[song])  # Dictionary se link fetch karna
        else:
            speak(f"{song} not found, searching on YouTube...")
            link = search_youtube(song)
            if link:
                speak(f"Playing {song} from YouTube...")
                webbrowser.open(link)
            else:
                speak("Sorry bro, song not found.")
     elif "news" in c:
      webbrowser.open("https://www.hindustantimes.com/")
      r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
      if r.status_code == 200:
        data=r.json()
        articles=data.get('articles',[])[:10] 
        speak("HERE ARE TOP 10 NEWS HEADLINE")
        for article in articles:
            speak(article['title'])
     elif "conversation" in c:
          speak("conversation mode on")
          while True:
               try:
                   with sr.Microphone() as source:
                    print("Bol bhai, sun raha hoon...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

                   text = recognizer.recognize_google(audio, language="en-IN").lower()
                   print("You said:", text)
                   speak(vasuki_reply(text))
                   
                   if "close" in text:
                     speak("ok")
                     speak("conversation mode off!")
                     break 
                     listen_for_command()  # Abcontinuous commands lega
               except sr.UnknownValueError:
                   print("Kuch samajh nahi aaya...")
     else:
     #  #GEMENI k API k use paid h 
         output=aiProcess(c)
         speak(output)
    # #EMOTIONS 
     v = Vasukii()
     while True:
      if c.lower() in ["exit", "quit"]:
        break
      else:
          v.respond(c)
          break
#----------------------------------------------------------------------------
def listen_for_keyword():
    """Listen for the keyword 'Vasuki' before activating"""
    while True:
        try:
            with sr.Microphone() as source:
                print("Bol bhai, sun raha hoon...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

                text = recognizer.recognize_google(audio, language="en-IN").lower()
                print("You said:", text)

                if "vasuki" in text:
                    speak("yaa")
                    speak("please wait, activating vasuki")
                    speak("VASUKI ACTIVATED")
                    listen_for_command()  # Ab continuous commands lega
        except sr.UnknownValueError:
            print("Kuch samajh nahi aaya...")
        except sr.RequestError:
            print("Internet check kar bhai!")
def listen_for_command():
    """Continuously listen for user commands after Vasuki is activated"""
    while True:
        try:
            with sr.Microphone() as source:
                print("Bol bhai, command de...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

                text = recognizer.recognize_google(audio, language="en-IN").lower()
                print("Command:", text)
                speak("You said: " + text)
                processcommand(text)

                if "exit" in text or "bye" in text:
                    speak("DEACTIVATING VASUKI")
                    break  # Exit loop if user says "exit" or "bye"
        except sr.UnknownValueError:
            speak("Bro, kuch samajh nahi aaya.")
        except sr.RequestError:
            speak("Google se response nahi mila, net check kar.")

# == Correct Entry Point ==
if __name__ == "__main__":
    speak(get_greeting() + " I am VASUKI, waiting for activation.")
    listen_for_keyword()  # Hotword "Vasuki" sunne ke liye

#PROJECT COMPLETED 