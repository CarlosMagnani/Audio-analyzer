import tkinter as tk
import threading
import speech_recognition as sr
import noisereduce as nr
from textblob import TextBlob as blob
import pyttsx3


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Gravador")
        self.pack()

        self.master.geometry("400x150")  # Tamanho da janela
        self.master.eval('tk::PlaceWindow %s center' % self.master.winfo_toplevel())
        self.create_widgets()

    def create_widgets(self):
        self.record_button = tk.Button(self)
        self.record_button["text"] = "Gravar"
        self.record_button["command"] = self.record_audio
        self.record_button.pack(side="bottom")

        self.status_label = tk.Label(self, text="Clique no botão para começar a gravar.")
        self.status_label.pack(side="bottom")

    def record_audio(self):
        threading.Thread(target=self.record_thread).start()

    def record_thread(self):
        self.status_label.config(text="Escutando...")
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1.0
            r.energy_threshold = 4000
            audio = r.listen(source)

        self.status_label.config(text="Analisando...")
        try:
            # audioClean = nr.reduce_noise(audio_clip=audio, noise_clip=audio, verbose=False)
            query = r.recognize_google(audio, language="en-in")

        except:
            self.status_label.config(text="Não foi possível reconhecer o áudio.")
            return

        sentiment = self.get_sentiment(query)
        speak_text = "Você disse algo {}.".format(sentiment)
        self.status_label.config(text=speak_text)
        self.speak(speak_text)

    def get_sentiment(self, text):
        tb = blob(text)
        result = tb.sentiment
        polarity = result.polarity
        print({"polaridade": polarity, "Você falou": text})
        if polarity == 0:
            return "neutro"
        elif polarity > 0:
            return "positivo"
        else:
            return "negativo"

    def speak(self, audio):
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)
        engine.say(audio)
        engine.runAndWait()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
