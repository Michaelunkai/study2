# Exploring the Color Chooser Module in Python with Tkinter
from tkinter import colorchooser
import tkinter as tk
# Explanation: We import the colorchooser module from Tkinter to access the color selection functionality.

#  Create a function to handle button click
def click():
    color = colorchooser.askcolor()[1]
    window.config(bg=color)

# Step 2: Create a Tkinter window and a button
window = tk.Tk()
window.geometry("420x420")

button = tk.Button(window, text="Click me", command=click)
button.pack()
# Explanation: We create a Tkinter window with a specified size and a button that will trigger the color selection.

# Step 4: Print and extract hexadecimal color value
color = colorchooser.askcolor()[1]
color_hex = color[1]
print(color_hex)

# Step 5: Change the background color of the window
window.config(bg="#87CEEB")  # Set default background color to sky blue

# Step 6: Condense the code for changing the background color
color = colorchooser.askcolor()[1]
window.config(bg=color)
# Explanation: We demonstrate condensing the code by directly assigning the color value to the background.
