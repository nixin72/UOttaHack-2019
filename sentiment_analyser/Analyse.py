from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from pygame import mixer
import pygame as pg
import time
import os
import io
import pyaudio
import speech_recognition as rs
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        return(str(result.alternatives[0].transcript))



root = tk.Tk()
root.title('Emotion Analyser')
root.iconbitmap('mic.ico')
emo = tk.StringVar(root)
style = ttk.Style()
style.theme_use('aqua')

photo = PhotoImage(file='microphone.png').subsample(35, 35)

label1 = ttk.Label(root, text='Message')
label1.grid(row=0, column=0)

entry1 = ttk.Entry(root, width=40)
entry1.grid(row=0, column=1, columnspan=4)

btn2 = tk.StringVar()



def callback():
    try:
        os.system("start microphone-results.wav")
    except:
        print('No Audio File Found')

def buttonClick():
    mixer.init()
    mixer.music.load('chime1.mp3')
    mixer.music.play()

    r = sr.Recognizer()
    r.pause_threshold = 0.7
    r.energy_threshold = 400
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=7)
            #message = str(r.recognize_google(audio))
            mixer.music.load('chime2.mp3')
            mixer.music.play()

        except sr.UnknownValueError:
            print('Google Speech Recognition could not Understand audio')
        except sr.RequestError as e:
            print('Could not request result from Google Speech Recogniser Service')
        else:
            pass

    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())
        message = transcribe_file("microphone-results.wav")
        print(message)
        entry1.focus()
        entry1.delete(0, END)
        entry1.insert(0, message)
        # Instantiates a client
        client = language.LanguageServiceClient()

        # The text to analyze
        text = message
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(document=document).document_sentiment

        score = sentiment.score
        print(text)
        if score >= -1.0 and score < -0.25:
            print(":(")
            label2 = ttk.Label(root, text=':(')
            label2.grid(row=1, column=0, columnspan=2)
        if score >= -0.25 and score < 0.25:
            print(":/")
            label2 = ttk.Label(root, text=':/')
            label2.grid(row=1, column=0, columnspan=2)
        if score >= 0.25 and score <= 1:
            print(":)")
            label2 = ttk.Label(root, text=':)')
            label2.grid(row=1, column=0, columnspan=2)

# MyButton1 = ttk.Button(root, text='Play', width=10, command=callback)
# MyButton1.grid(row=0, column=6)

# label2 = ttk.Label(root, text='message')
# label2.grid(row=1, column=0, columnspan=2)
# entry2 = ttk.Entry(root, width=40)
# entry2.grid(row=2, column=0, columnspan=2)

label3 = ttk.Label(root, text='--> Emotion Analysed')
label3.grid(row=1, column=3)


MyButton3 = ttk.Button(root, image=photo, command=buttonClick)#, activebackground='#c1bfbf', overrelief='groove', relief='sunken')
MyButton3.grid(row=0, column=5)

root.wm_attributes('-topmost', 1)
btn2.set('google')
root.mainloop()
