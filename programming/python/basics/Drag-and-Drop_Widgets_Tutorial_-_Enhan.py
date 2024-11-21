# Import necessary modules
from tkinter import Tk, Label, mainloop

# Create the main window
window = Tk()
window.title("Drag-and-Drop Widgets in Python")

# Define the drag start function
def drag_start(event):
    # Get the widget and store start coordinates
    widget = event.widget
    widget.start_x = event.x
    widget.start_y = event.y

# Define the drag motion function
def drag_motion(event):
    # Get the widget and calculate new coordinates
    widget = event.widget
    x = widget.winfo_x() - widget.start_x + event.x
    y = widget.winfo_y() - widget.start_y + event.y

    # Place the widget at the new coordinates
    widget.place(x=x, y=y)

# Create and configure the first label widget
label1 = Label(window, text="Label 1", bg="red", width=10, height=5)
label1.place(x=0, y=0)

# Bind events for dragging and dropping for the first label
label1.bind("<Button-1>", drag_start)
label1.bind("<B1-Motion>", drag_motion)

# Create and configure the second label widget
label2 = Label(window, text="Label 2", bg="blue", width=10, height=5)
label2.place(x=100, y=100)

# Bind events for dragging and dropping for the second label
label2.bind("<Button-1>", drag_start)
label2.bind("<B1-Motion>", drag_motion)

# Start the Tkinter main loop
mainloop()
