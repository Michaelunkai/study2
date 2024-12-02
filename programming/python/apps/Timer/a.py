import tkinter as tk
import time


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")

        # Resize the window
        self.root.geometry("1000x600")

        # Timer variables
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0

        # Timer display
        self.time_label = tk.Label(
            root, text="00:00:00", font=("Helvetica", 240, "bold")
        )
        self.time_label.pack(pady=50)

        # Key bindings
        self.root.bind("<space>", self.toggle_timer)
        self.root.bind("<Return>", self.reset_timer)

    def update_timer(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))
            self.time_label.config(text=formatted_time)
            self.root.after(1000, self.update_timer)

    def start_timer(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.update_timer()

    def stop_timer(self):
        self.running = False

    def reset_timer(self, event=None):
        self.running = False
        self.elapsed_time = 0
        self.time_label.config(text="00:00:00")

    def toggle_timer(self, event=None):
        if self.running:
            self.stop_timer()
        else:
            self.start_timer()


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
