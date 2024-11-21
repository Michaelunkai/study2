# Exploring the Text Widget  with Tkinter
import tkinter as tk

# define submit
def submit():
    input_text = text.get("1.0", "end")
    print(input_text)

#  Create a Tkinter window and a text widget
window = tk.Tk()
text = tk.Text(window, bg="light yellow", font=("ink free", 25), height=8, width=20, padx=20,pady=20, fg="purple")
text.pack()

# Create a button and a function for submitting text
button = tk.Button(window, text="submit", command=submit)
button.pack()

text.config(bg="light yellow")
text.config(font=("ink free", 25))
text.config(height=8, width=20)
text.config(padx=20, pady=20)
text.config(fg="purple")

window.mainloop()