import tkinter as tk
import random

# List of words for the game
words = ["python", "hangman", "programming", "computer", "science", "code"]

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")

        self.word = random.choice(words)
        self.guessed_letters = []
        self.attempts = 6

        self.word_display = tk.StringVar()
        self.word_label = tk.Label(master, textvariable=self.word_display, font=("Arial", 24))
        self.word_label.pack()

        self.input_label = tk.Label(master, text="Guess a letter:", font=("Arial", 18))
        self.input_label.pack()

        self.input_entry = tk.Entry(master, font=("Arial", 18))
        self.input_entry.pack()

        self.submit_button = tk.Button(master, text="Submit", command=self.check_guess, font=("Arial", 18))
        self.submit_button.pack()

        self.status_label = tk.Label(master, font=("Arial", 18))
        self.status_label.pack()

        self.canvas = tk.Canvas(master, width=200, height=250)
        self.canvas.pack()

        self.draw_hangman()

        self.update_display()

    def update_display(self):
        displayed_word = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                displayed_word += letter
            else:
                displayed_word += "_ "
        self.word_display.set(displayed_word)

    def draw_hangman(self):
        parts = [self.draw_head, self.draw_body, self.draw_left_arm, self.draw_right_arm, self.draw_left_leg, self.draw_right_leg]
        for i in range(self.attempts):
            parts[i]()

    def draw_head(self):
        self.canvas.create_oval(50, 50, 150, 150, outline="black", width=2)

    def draw_body(self):
        self.canvas.create_line(100, 150, 100, 200, fill="black", width=2)

    def draw_left_arm(self):
        self.canvas.create_line(100, 160, 50, 130, fill="black", width=2)

    def draw_right_arm(self):
        self.canvas.create_line(100, 160, 150, 130, fill="black", width=2)

    def draw_left_leg(self):
        self.canvas.create_line(100, 200, 50, 250, fill="black", width=2)

    def draw_right_leg(self):
        self.canvas.create_line(100, 200, 150, 250, fill="black", width=2)

    def check_guess(self):
        guess = self.input_entry.get().lower()
        self.input_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.status_label.config(text="Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            self.status_label.config(text="You already guessed that letter.")
            return

        self.guessed_letters.append(guess)

        if guess not in self.word:
            self.attempts -= 1
            self.status_label.config(text=f"Incorrect guess! Attempts left: {self.attempts}")
            self.draw_hangman()
            if self.attempts == 0:
                self.status_label.config(text=f"Sorry, you're out of attempts. The word was: {self.word}")
                self.submit_button.config(state=tk.DISABLED)
        else:
            self.status_label.config(text="Correct guess!")

        self.update_display()

        if all(letter in self.guessed_letters for letter in self.word):
            self.status_label.config(text=f"Congratulations! You guessed the word: {self.word}")
            self.submit_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
