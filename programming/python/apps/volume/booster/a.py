import tkinter as tk
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeBooster:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Volume Booster")
        self.root.geometry("400x150")
        self.root.resizable(False, False)
        
        # Initialize audio
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.base_volume = self.volume.GetMasterVolumeLevelScalar()
        
        # Create slider
        self.slider = tk.Scale(
            self.root,
            from_=0,
            to=200,
            orient=tk.HORIZONTAL,
            length=340,
            command=self.update_volume
        )
        self.slider.set(100)
        self.slider.pack(pady=20)
        
        # Create label
        self.label = tk.Label(self.root, text="Boost: 100%")
        self.label.pack()
        
        # Cleanup on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def update_volume(self, value):
        boost = float(value) / 100
        new_volume = min(self.base_volume * boost, 1.0)
        self.volume.SetMasterVolumeLevelScalar(new_volume, None)
        self.label.config(text=f"Boost: {value}%")
        
    def on_closing(self):
        self.volume.SetMasterVolumeLevelScalar(self.base_volume, None)
        self.root.destroy()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VolumeBooster()
    app.run()
