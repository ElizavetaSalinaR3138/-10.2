import time
import pyttsx3
import requests
import speech_recognition as sr
import webbrowser
from speech_recognition import UnknownValueError

engine = pyttsx3.init()
newVoiceRate = 120

voices = engine.getProperty('voices')
engine.setProperty('voices', 'en')

for voice in voices:
    if voice.name == 'Shelley (English (UK))':
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', newVoiceRate)

r = sr.Recognizer()


def talk(say):
    engine.say(say)
    engine.runAndWait()


def start_msg():
    talk('Hello, I am your personal assistant.'+\
         'I can find some information about random dogs.'+\
         'Just tell me: find random dog. '+\
         'If you wan\'t close the program, you can say EXIT.')


def listening():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('Listening to you...')
        voice = r.listen(source)
        try:
            time.sleep(1.5)
            command = r.recognize_google(voice, language="en-GB")
            return command
        except UnknownValueError:
            talk("Could not recognize your speech.")
            return 'Request error'


def ELIZA(url):
    url = requests.get('https://dog.ceo/api/breeds/image/random')
    s = url.json()
    talk('do you want to open/download a photo of a dog,\
         find out its breed or find the next one?')
    command = listening()
    print(command)
    if 'open' in command:
        webbrowser.open_new_tab(s.get('message'))
    if 'download' in command:
        rqst_img = requests.get(s.get('message'))
        with open('req_img.png', 'wb') as file:
            file.write(rqst_img.content)

    if 'next' in command:
        print('aaaaa')
        return
    if 'breed' in command:
        breed = s.get('message').split('/')[4]
        try:
            breed = s.get('message').split('/')[4].replace('-',' ')
            talk(breed)
        except:
            talk(s.get('message').split('/')[4])
    if 'Request error' in command:
        talk("Could not recognize your speech.")


start_msg()
url = requests.get('https://dog.ceo/api/breeds/image/random')

while True:
    speech = ''
    speech = listening()
    print(speech)
    if 'dog' in speech:
        ELIZA(url)
        talk('just tell dog')
    elif 'exit' in speech:
        quit()
    if speech == '':
        talk(f'Did not hear the word. Please repeat the request again.')
        continue
