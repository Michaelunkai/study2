# Form Grid Application
import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Form Submission")

# Title Label
title_label = tk.Label(window, text="Enter your info", font=("Arial", 25))
title_label.grid(row=0, column=0, columnspan=2)

# First Name Widgets
first_name_label = tk.Label(window, text="First name", width=20,  bg="red")
first_name_label.grid(row=1, column=0)

first_name_entry = tk.Entry(window)
first_name_entry.grid(row=1, column=1)

# Email Widgets
email_label = tk.Label(window, text="Email", width=20, bg="blue")
email_label.grid(row=3, column=0)

email_entry = tk.Entry(window)
email_entry.grid(row=3, column=1)

# Submit Button
submit_button = tk.Button(window, text="Submit")
submit_button.grid(row=4, column=0, columnspan=2)

# Run the main loop
window.mainloop()

