import tkinter as tk
import random

# Constants
MIN_NUMBER = 1
MAX_NUMBER = 100

class GuessTheNumberGame:
    def __init__(self):
        self.target_number = random.randint(MIN_NUMBER, MAX_NUMBER)
        self.guesses = 0

    def check_guess(self, guess):
        self.guesses += 1
        if guess < self.target_number:
            return "Too low!"
        elif guess > self.target_number:
            return "Too high!"
        else:
            return "Congratulations! You guessed it in {} guesses.".format(self.guesses)

def check_guess_entry():
    try:
        guess = int(guess_entry.get())
        result = game.check_guess(guess)
        result_label.config(text=result)
    except ValueError:
        result_label.config(text="Please enter a valid number.")

# Initialize the game window
window = tk.Tk()
window.title("Guess The Number Game")
window.geometry("300x150")

# Create the game instance
game = GuessTheNumberGame()

# Create widgets
instruction_label = tk.Label(window, text="Guess a number between {} and {}:".format(MIN_NUMBER, MAX_NUMBER))
guess_entry = tk.Entry(window)
check_button = tk.Button(window, text="Check Guess", command=check_guess_entry)
result_label = tk.Label(window, text="")

# Pack widgets
instruction_label.pack()
guess_entry.pack()
check_button.pack()
result_label.pack()

# Run the game
window.mainloop()
