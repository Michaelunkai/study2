import sys
import pyaudio
import wave
import threading
import numpy as np
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QTimer

class SpeechRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_audio()
        self.init_recognizer()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Advanced Speech Recognition')
        self.setStyleSheet("background-color: black; color: white;")

        layout = QVBoxLayout()

        self.start_button = QPushButton('Start Recording', self)
        self.start_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.start_button)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def init_audio(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.frames = []
        self.recording = False
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

    def init_recognizer(self):
        self.recognizer = sr.Recognizer()

    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.start_button.setText('Stop Recording')
            self.frames = []
            threading.Thread(target=self.record_audio).start()
        else:
            self.recording = False
            self.start_button.setText('Start Recording')
            self.process_audio()

    def record_audio(self):
        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

    def detect_language(self, audio):
        try:
            # Try to recognize a small sample in English
            text = self.recognizer.recognize_google(audio, language="en-US")
            return "en-US"
        except sr.UnknownValueError:
            try:
                # If English fails, try Hebrew
                text = self.recognizer.recognize_google(audio, language="iw-IL")
                return "iw-IL"
            except sr.UnknownValueError:
                # If both fail, default to English
                return "en-US"

    def process_audio(self):
        if not self.frames:
            self.text_edit.append("No audio recorded.")
            return

        # Save the recorded audio to a WAV file
        wf = wave.open("temp.wav", 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        # Perform speech recognition
        try:
            with sr.AudioFile("temp.wav") as source:
                audio = self.recognizer.record(source)
            
            # Detect language from a small sample (first 5 seconds)
            sample_audio = sr.AudioData(audio.frame_data[:int(5 * self.RATE * audio.sample_width)], 
                                        audio.sample_rate, audio.sample_width)
            detected_language = self.detect_language(sample_audio)
            
            # Perform full transcription with detected language
            transcription = self.recognizer.recognize_google(audio, language=detected_language)
            
            language_name = "English" if detected_language == "en-US" else "Hebrew"
            self.text_edit.append(f"Detected Language: {language_name}")
            self.text_edit.append(f"Transcription: {transcription}")
        
        except sr.UnknownValueError:
            self.text_edit.append("Speech recognition could not understand audio")
        except sr.RequestError as e:
            self.text_edit.append(f"Could not request results from speech recognition service; {e}")
        except Exception as e:
            self.text_edit.append(f"An error occurred: {str(e)}")

    def paintEvent(self, event):
        if self.recording:
            qp = QPainter()
            qp.begin(self)
            self.draw_waveform(qp)
            qp.end()

    def draw_waveform(self, qp):
        pen = QPen(Qt.white, 2, Qt.SolidLine)
        qp.setPen(pen)

        width = self.width()
        height = self.height()
        center_y = height // 2

        if len(self.frames) > 0:
            waveform = np.frombuffer(self.frames[-1], dtype=np.int16)
            waveform = waveform / np.max(np.abs(waveform))
            
            points = []
            for i, sample in enumerate(waveform):
                x = int((i / len(waveform)) * width)
                y = int(sample * 100) + center_y
                points.append((x, y))

            for i in range(1, len(points)):
                qp.drawLine(points[i-1][0], points[i-1][1], points[i][0], points[i][1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SpeechRecognitionApp()
    ex.show()
    sys.exit(app.exec_())
