# # # #  Key Events Tutorial - Mastering User Input

# # # # Import necessary modules
# # # from tkinter import Tk, Label, mainloop

# # # # Create the main window
# # # window = Tk()
# # # window.title("Key Events in Python")

# # # # Create a label for displaying key events
# # # label = Label(window, font=("Helvetica", 18))
# # # label.pack()

# # # # Define the function to handle key events
# # # def handle_key_event(event):
# # #     key_pressed = event.keysym
# # #     label.config(text=f"You pressed: {key_pressed}")

# # # # Bind the key event (any key) to the function
# # # window.bind("<Key>", handle_key_event)

# # # # Start the Tkinter main loop
# # # mainloop()
# # # ___________________________________________________

# # # Step 2: Responding to Specific Keys
# # # Import necessary modules
# # from tkinter import Tk, Label, mainloop

# # # Create the main window
# # window = Tk()
# # window.title("Specific Key Events")

# # # Create a label for displaying key events
# # label = Label(window, font=("Helvetica", 18))
# # label.pack()

# # # Define the function to handle key events
# # def handle_key_event(event):
# #     key_pressed = event.keysym
# #     label.config(text=f"You pressed: {key_pressed}")

# # # Bind specific keys to the function (e.g., Enter, Q)
# # window.bind("<Return>", handle_key_event)
# # window.bind("q", handle_key_event)

# # # Start the Tkinter main loop
# # mainloop()

# # __________________________________________________
# # Step 3: Displaying Key Symbols

# # Import necessary modules
# from tkinter import Tk, Label, mainloop

# # Create the main window
# window = Tk()
# window.title("Displaying Key Symbols")

# # Create a label for displaying key events
# label = Label(window, font=("Helvetica", 18))
# label.pack()

# # Define the function to handle key events
# def handle_key_event(event):
#     key_pressed = event.keysym
#     label.config(text=f"You pressed: {key_pressed} ({event.keysym})")

# # Bind key events to the function (e.g., Key, a, space)
# window.bind("<Key>", handle_key_event)
# window.bind("a", handle_key_event)
# window.bind("<space>", handle_key_event)

# # Start the Tkinter main loop
# mainloop()

# # Step 4: Dynamic Label Text Update
# # Import necessary modules
# from tkinter import Tk, Label, mainloop

# # Create the main window
# window = Tk()
# window.title("Dynamic Label Text Update")

# # Create a label for displaying key events
# label = Label(window, font=("Helvetica", 18))
# label.pack()

# # Define the function to handle key events and update label text
# def handle_key_event(event):
#     key_pressed = event.keysym
#     label.config(text=f"You pressed: {key_pressed}")

# # Bind any key event to the function
# window.bind("<Key>", handle_key_event)

# # Start the Tkinter main loop
# mainloop()

# ___________________________________________________________
# Step 5: Advanced Key Events - Dynamic Label Text and Task Execution
# Import necessary modules
from tkinter import Tk, Label, mainloop

# Create the main window
window = Tk()
window.title("Advanced Key Events")

# Create a label for displaying key events
label = Label(window, font=("Helvetica", 18))
label.pack()

# Define the function to handle key events, update label text, and perform a task
def handle_key_event(event):
    key_pressed = event.keysym
    label.config(text=f"You pressed: {key_pressed}")

    # Perform a task based on the pressed key
    if key_pressed == "Return":
        print("Task executed: Submitting form")
    elif key_pressed.lower() == "q":
        print("Task executed: Quitting application")

# Bind specific keys to the function
window.bind("<Return>", handle_key_event)
window.bind("q", handle_key_event)

# Start the Tkinter main loop
mainloop()


# This tutorial guides you through mastering key events in Python, starting from basic introduction to handling specific keys, displaying key symbols, dynamically updating label text, and finally incorporating key events into more advanced applications.



