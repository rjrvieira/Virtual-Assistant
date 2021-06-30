import speech_recognition as sr
import pyttsx3
import wikipedia
import sys
import subprocess
import webbrowser
import pyaudio
from pydub import AudioSegment
sys.path.append('/usr/local/Cellar/ffmpeg/4.3.1_9/bin/ffmpeg')

def playSound(start, end):
    
    mp3 = AudioSegment.from_mp3("/Users/vieira/Desktop/Programas/Siri.mp3")
    mp3 = mp3[int(start):int(end)]
    player = pyaudio.PyAudio()

    stream = player.open(format = player.get_format_from_width(mp3.sample_width),
            channels = mp3.channels,
            rate = mp3.frame_rate,
            output = True)

    data = mp3.raw_data

    while data:
        stream.write(data)
        data=0

    stream.close()
    player.terminate()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():

    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        playSound(0, 1000)
        audio=r.listen(source)
        print(audio)

        try:
            statement=r.recognize_google(audio,language='pt-pt')
            print(f"user said: {statement}\n")

        except Exception as e:
            speak("Desculpa, não percebi, podes repetir?")
            return "None"

        playSound(1000, 2000)
        return statement



def action(statement):

    if 'wikipédia' in statement:
        try:
            speak('Segundo a Wikipédia...')
            statement = statement.replace("wikipédia", "")
            results = wikipedia.summary(statement, sentences=3)
            print(results)
            speak(results)

        except wikipedia.DisambiguationError as e:
                s = random.choice(e.options)
                p = wikipedia.summary(s)
    
    elif any(word in statement for word in ['abrir', 'abre']):

        if 'youtube' in statement:
            webbrowser.open_new_tab("https://youtube.com")

        elif 'google' in statement:
            webbrowser.open_new_tab("https://google.com")

        elif 'gmail' in statement:
            webbrowser.open_new_tab("https://gmail.com")

        elif 'e-mail' in statement:
            subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "/System/Applications/Mail.app"]) 

    elif any(word in statement for word in ['procurar', 'pesquisar', 'mostrar']):

        if 'imagens' in statement:
            statement = statement[statement.find('imagens'):]
            statement = statement.replace(' ', '+')
            webbrowser.open_new_tab("https://www.google.com/search?q="+statement)
        
        else:
            if 'procurar' in statement:
                statement = statement[statement.find('procurar'):]
                statement = statement.replace('procurar', '')
            elif 'pesquisar' in statement:
                statement = statement[statement.find('pesquisar'):]
                statement = statement.replace('pesquisar', '')
            elif 'mostrar' in statement:
                statement = statement[statement.find('mostrar'):]
                statement = statement.replace('mostrar', '')

            statement = statement.replace(' ', '+')
            webbrowser.open_new_tab("https://www.google.com/search?q="+statement)

    elif any(word in statement for word in ['adeus', 'xau', 'sair', 'até à próxima', 'até já']):
        speak("A encerrar a assistente. Até à próxima")
        sys.exit()

    else:
        speak("Não consigo realizar a ação")



if __name__ == '__main__':

    engine = pyttsx3.init('nsss')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[13].id)

    speak("Olá! Sou a sua assistente virtual, em que posso ajudar?")

    while True:
        statement = listen().lower()
        #if 'alexa' in statement:
        action(statement)