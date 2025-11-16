# Standard library
import os
import requests

# Third-party libraries
from PIL import Image, ImageTk
import pyttsx3
import pygame
import speech_recognition as sr
import wolframalpha
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
from openai import OpenAI


# Tkinter (GUI) imports
from tkinter import Button
from tkinter import Entry
from tkinter import Frame
import tkinter as tk
from tkinter import ttk
from tkinter import Label
from tkinter import messagebox
from tkinter import PhotoImage



# ----------------- CONFIG -----------------
WOLFRAM_APP_ID = "MY PERSONAL ID"# used my personal id
HF_API_TOKEN = "MY PERSONAL TOKEN"# used my personal token
HF_MODEL = "bigscience/bloom-560m"  # Can replace with any HuggingFace hosted model

wolfram_client = wolframalpha.Client(WOLFRAM_APP_ID)
engine = pyttsx3.init()


# ----------------- MUSIC -----------------
pygame.mixer.init()
song = "lofi-study-calm-peaceful-chill-hop-112191.mp3"
pygame.mixer.music.load(song)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)

# ----------------- GUI/UI -----------------

window = tk.Tk() # The Main Window
window.geometry("500x600") 

window.title("main window/homepage")
icon = PhotoImage(file='book.png')
window.iconphoto(True,icon)
window.config(bg="lightblue")


# ------------ Enter Username ---------------
frame1 = Frame(window, bg="pink", width=500, height=600)
frame1.pack()

enterNameLabel = Entry(frame1,width=15)
enterNameLabel.config(font=('Arial', 15, "bold"))
enterNameLabel.config(bg='lightblue')
enterNameLabel.config(fg='Black')
enterNameLabel.insert(0, "Enter Username")
enterNameLabel.place(relx=0.5, rely=0.5, anchor='center')


# Function for Submitting Username
def submit():
    username = enterNameLabel.get()
    switch_frame(frame1, frame2)

# FUNCTIONS FOR SWITCHING BETWEEN FRAMES
def big_city():
    switch_frame(frame2, frame3)


def switch_frame(current_frame, next_frame):
    #"""Hide the current frame and show the next frame."""
    current_frame.pack_forget()
    next_frame.pack()

# Submit Button for Submitting Username
submitted = Button(frame1, text="submit", width=10, command=submit)
submitted.place(relx=0.8, rely=0.47, anchor=tk.NW)

# Next Frame - For Selecting Characters
frame2 = Frame(window,bg="blue", width=500, height=600)
frame2.pack()

babyFrame = Frame(frame2, width=500, height=600, bg="lightblue")
babyFrame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Text Telling User to Choose a Character
meetCharacters = Label(babyFrame, text="Choose a Literacy League Character!", fg="Black").pack()

# The 4 Characters(PHOTOS and BUTTONS)
photo1 = PhotoImage(file='Scorchin Syllable2.png')
photo2 = PhotoImage(file='StoryBoy2.png')
photo3 = PhotoImage(file='Grandma Grammar2.png')
photo4 = PhotoImage(file='Captain Adjective2.png')

button = Button(babyFrame, text="Scorchin Syllable", image = photo1, width=93, height=90,compound="top")
button.pack(side="left")
    
button = Button(babyFrame, text="StoryBoy", image = photo2, width=93, height=90,compound="top")
button.pack(side="right") 

button = Button(babyFrame, text="GrandmaGrammar", image = photo3, width=93, height=90,compound="top")
button.pack(side="bottom") 

button = Button(babyFrame, text="Captain Adjective", image = photo4, width=93, height=90,compound="top", command=big_city)
button.pack(side="right") 

# Third Frame - For  Cookie Clicker
frame3 = Frame(window, bg='lightblue', width=500, height=600)
frame3.pack()


# Smaller Frames for Extra Positioning of the City Image
smallFrame = Frame(frame3, width=500, height=600, bg="lightblue")
smallFrame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
cityBg = PhotoImage(file='city.png')
citySetting = Label(smallFrame, image=cityBg, width=500, height=600)
citySetting.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

cookiePhoto = PhotoImage(file='cookie.png')

# Cookie Clicker Function
count = 0
def clicker():
  global count
  count+=1
  clicks.config(text=count)
  if count == 40:
    switch_frame(frame3, frame4)

cookie = Button(citySetting, image=cookiePhoto, text=count, width=93, height=90, compound="top") 
cookie.place(relx=0.5, rely=0.55, anchor=tk.S)
cookie.config(command=clicker)

clicks = Label(citySetting, text=count)
clicks.config(font=('Times New Roman', 50, 'bold'))
clicks.place(relx=0.8, rely=0.8, anchor=tk.S)



#frame4 - AI Assistant
frame4 = Frame(window, width=500, height=600)
frame4.pack()

# AI Character Image
try:
    image = Image.open("Captain Adjective2.png").resize((200, 200))
    photo = ImageTk.PhotoImage(image)
    character = tk.Label(frame4, image=photo)
    character.pack(pady=10)
except:
    character = tk.Label(frame4, text="Literacy Quest", font=("Arial", 24))
    character.pack(pady=10)

# Output box
output = tk.Text(frame4, height=15, width=60, wrap=tk.WORD)
output.pack(pady=10)

# Entry box
entry = tk.Entry(frame4, width=50)
entry.pack(pady=5)

# ----------------- FUNCTIONS for AI-----------------
def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_speech_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        output.insert(tk.END, "Listening...\n")
        output.see(tk.END)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        output.insert(tk.END, f"You said: {text}\n")
        return text
    except sr.UnknownValueError:
        output.insert(tk.END, "Sorry, I couldn't understand.\n")
        return ""
    except sr.RequestError:
        output.insert(tk.END, "Speech service error.\n")
        return ""

# WolframAlpha query
def ask_wolfram(question):
    try:
        res = wolfram_client.query(question)
        answer = next(res.results).text
    except Exception:
        answer = None
    return answer

# Openai fallback
from openai import OpenAI
client = OpenAI(api_key="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"
)

def ask_openai(question):
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": question}],
            max_tokens=100,
            temperature=0.7
        )

        reply = completion.choices[0].message.content
        if not reply:
            return "The AI couldn't generate a response."
        return reply.strip()

    except Exception as e:
        return f"OpenAI API error: {e}"



# Main ask function
def ask():
    question = entry.get()
    if not question.strip():
        return

    # Try WolframAlpha first
    answer = ask_wolfram(question)
    if not answer:
        # Fallback to openai
        answer = ask_openai(question)

    # Show in GUI
    output.insert(tk.END, f"> {question}\n{answer}\n\n")
    output.see(tk.END)
    entry.delete(0, tk.END)

    # Speak the answer
    speak(answer)

# Listen button
def listen_and_ask():
    question = get_speech_input()
    if question:
        entry.delete(0, tk.END)
        entry.insert(0, question)
        ask()

# ----------------- BUTTONS -----------------
btn_ask = tk.Button(window, text="Ask", command=ask)
btn_ask.pack(pady=5)

btn_listen = tk.Button(window, text="Speak", command=listen_and_ask)
btn_listen.pack(pady=5)







window.mainloop()