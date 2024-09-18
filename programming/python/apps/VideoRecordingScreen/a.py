import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import pyautogui
import threading
import time

class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")
        self.root.geometry("300x150")
        self.root.attributes("-topmost", True)  # Make the window always on top
        self.is_recording = False
        self.recording_thread = None
        self.start_time = None

        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)

        self.timer_label = tk.Label(root, text="Recording time: 00:00")
        self.timer_label.pack(pady=10)

    def start_recording(self):
        if self.is_recording:
            messagebox.showwarning("Warning", "Already recording!")
            return
        self.is_recording = True
        self.start_time = time.time()
        self.update_timer()
        self.recording_thread = threading.Thread(target=self.record_screen)
        self.recording_thread.start()

    def stop_recording(self):
        if not self.is_recording:
            messagebox.showwarning("Warning", "Not recording!")
            return
        self.is_recording = False
        self.recording_thread.join()
        messagebox.showinfo("Info", "Recording stopped and saved as C:/Users/micha/Downloads/output.avi")
        self.timer_label.config(text="Recording time: 00:00")

    def update_timer(self):
        if self.is_recording:
            elapsed_time = time.time() - self.start_time
            mins, secs = divmod(int(elapsed_time), 60)
            timer_text = f"Recording time: {mins:02}:{secs:02}"
            self.timer_label.config(text=timer_text)
            self.root.after(1000, self.update_timer)

    def record_screen(self):
        SCREEN_SIZE = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter("C:/Users/micha/Downloads/output.avi", fourcc, 20.0, SCREEN_SIZE)

        while self.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)

        out.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()
