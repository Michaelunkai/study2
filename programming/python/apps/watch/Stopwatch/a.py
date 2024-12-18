import time
import winsound  # For Windows systems; use an alternative for Linux/Mac
import tkinter as tk
import sys

def show_popup_and_exit():
    """Displays a popup message for 5 seconds, then exits the application."""
    popup = tk.Tk()
    popup.title("Timer Alert")
    popup.geometry("300x100")
    popup.resizable(False, False)

    label = tk.Label(popup, text="Time's Up!", font=("Arial", 16))
    label.pack(pady=20)

    # Close the popup and exit the application after 5 seconds
    popup.after(5000, lambda: (popup.destroy(), sys.exit()))
    popup.mainloop()

def start_timer():
    try:
        minutes = int(input("Enter the number of minutes for the timer: "))
        seconds = int(input("Enter the number of additional seconds for the timer: "))
        total_seconds = minutes * 60 + seconds

        print(f"Timer set for {minutes} minutes and {seconds} seconds.")
        input("Press Enter to start the countdown...")

        print("Countdown started. Counting:")
        for second in range(1, total_seconds + 1):
            print(f"{second} second{'s' if second > 1 else ''} passed...")
            time.sleep(1)

        print("Time's up! Playing sound and showing popup...")
        # Play a softer sound by reducing frequency
        frequency = 1000  # Reduced frequency in Hertz for a less loud sound
        sound_duration = 5000  # Duration in milliseconds
        winsound.Beep(frequency, sound_duration)

        # Show popup and exit
        show_popup_and_exit()

    except ValueError:
        print("Invalid input. Please enter numbers only.")

if __name__ == "__main__":
    start_timer()

