# Import necessary modules
from tkinter import Tk, mainloop

window = Tk()
window.title("Mouse Events in Python")

# Define the function to handle mouse events
def handle_mouse_event(event):
    mouse_action = ""
    
    if event.num == 1:  # Left mouse click
        mouse_action = "Left Mouse Click"
    elif event.num == 2:  # Scroll wheel press
        mouse_action = "Scroll Wheel Press"
    elif event.num == 3:  # Right mouse click
        mouse_action = "Right Mouse Click"

    # Display mouse coordinates
    mouse_coordinates = f"Mouse Coordinates: ({str(event.x)}, {str(event.y)})"

    # Print event details
    print(f"{mouse_action} at {mouse_coordinates}")

# Bind various mouse events to the function
window.bind("<Button-1>", handle_mouse_event)  # Left mouse click
window.bind("<Button-2>", handle_mouse_event)  # Scroll wheel press
window.bind("<Button-3>", handle_mouse_event)  # Right mouse click
window.bind("<ButtonRelease>", handle_mouse_event)  # Button release
window.bind("<Enter>", handle_mouse_event)  # Enter window
window.bind("<Leave>", handle_mouse_event)  # Leave window
window.bind("<Motion>", handle_mouse_event)  # Mouse motion

# Start the Tkinter main loop
mainloop()
