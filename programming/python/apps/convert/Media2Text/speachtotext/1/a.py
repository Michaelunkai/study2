import tkinter as tk
import speech_recognition as sr
import pyaudio
import tkinter.messagebox
import tkinter.ttk as ttk

class SpeechToTextApp:
    def __init__(self, master):
        self.master = master
        master.title("Speech to Text")

        self.is_listening = False
        self.transcribed_text = ""

        self.btn_microphone = tk.Button(master, text="🎤", command=self.toggle_listening)
        self.btn_microphone.pack()

        self.output_frame = tk.Frame(master)
        self.output_frame.pack()

        self.output_label = tk.Label(self.output_frame, text="", font=("Arial", 12, "bold"))
        self.output_label.pack(side=tk.LEFT)

        self.copy_button = tk.Button(self.output_frame, text="Copy", command=self.copy_text)
        self.copy_button.pack(side=tk.LEFT)

    def toggle_listening(self):
        if not self.is_listening:
            self.start_listening()
            self.btn_microphone.config(text="Stop Listening")
        else:
            self.stop_listening()
            self.btn_microphone.config(text="🎤")

    def start_listening(self):
        self.transcribed_text = ""  # Clear the transcribed text
        self.is_listening = True
        self.recognizer = sr.Recognizer()
        self.p = pyaudio.PyAudio()
        device_index = self.find_input_device()
        self.microphone = sr.Microphone(device_index=device_index)
        self.recognizer.listen_in_background(self.microphone, self.update_text)

    def stop_listening(self):
        self.is_listening = False

    def update_text(self, recognizer, audio):
        try:
            text = recognizer.recognize_google(audio)
            self.transcribed_text = text  # Replace the transcribed text with the new one
            self.output_label.config(text=self.transcribed_text)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            self.output_label.config(text=f"Error: {e}")

    def find_input_device(self):
        for i in range(self.p.get_device_count()):
            dev_info = self.p.get_device_info_by_index(i)
            if dev_info['maxInputChannels'] > 0:
                return i
        raise Exception("No input devices found")

    def copy_text(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.transcribed_text)
        tkinter.messagebox.showinfo("Copy", "Text copied to clipboard.")

def main():
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
