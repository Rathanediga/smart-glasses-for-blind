#!/usr/bin/env python3

import speech_recognition as sr
import os

global x
from playsound import playsound



def speech():

    try:
        with sr.Microphone() as source:
            global x
            r = sr.Recognizer()
            audio = r.listen(source)
            x = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("No clue what you said, listening again... \n")
        speech()


if __name__ == '__main__':
    flag=1
    a=1
    while(flag==1):
        print('Choose the mode by saying Indoor mode or in house mode or Outdoor mode \n')
        playsound('mode.mp3')
        speech()
        print(x)
        
        if(x=="outdoor mode"):
            print('Going to outdoor mode')
            flag=0
            
        elif(x=="indoor mode"or x=="Indore mod" or x=="in house mode"):
            print('Going to indoor mode')
            flag=0
    if(x=="outdoor mode"):
        exec(open('outdoor.py').read())

    elif(x=="indoor mode"or x=="Indore mod" or x=="in house mode"):
        exec(open('indoor.py').read())
    
            