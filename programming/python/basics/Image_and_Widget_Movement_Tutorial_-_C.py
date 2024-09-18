# Import necessary modules
from tkinter import Tk, Label, Canvas, PhotoImage, mainloop

# Create the main window
window = Tk()
window.title("Advanced Image and Widget Movement in Python")

# Section 1: Moving a Widget within a Window
# Set window geometry
window.geometry("500x500")

# Create a label widget with a racecar image
my_image = PhotoImage(file="racecar.png")
label = Label(window, image=my_image)
label.place(x=0, y=0)

# Define move functions for up, down, left, right
def move_up(event):
    label.place(x=label.winfo_x(), y=label.winfo_y() - 10)

def move_down(event):
    label.place(x=label.winfo_x(), y=label.winfo_y() + 10)

def move_left(event):
    label.place(x=label.winfo_x() - 10, y=label.winfo_y())

def move_right(event):
    label.place(x=label.winfo_x() + 10, y=label.winfo_y())

# Bind keys for moving the label
window.bind("w", move_up)
window.bind("s", move_down)
window.bind("a", move_left)
window.bind("d", move_right)
window.bind("<Up>", move_up)
window.bind("<Down>", move_down)
window.bind("<Left>", move_left)
window.bind("<Right>", move_right)

# Section 2: Moving an Image on a Canvas
# Create a canvas with width and height
canvas = Canvas(window, width=500, height=500)
canvas.pack()

# Load image for the canvas
canvas_image = PhotoImage(file="racecar.png")
canvas.create_image(0, 0, anchor="nw", image=canvas_image)

# Define move functions for canvas image
def move_up_canvas(event):
    canvas.move(canvas_image, 0, -10)

def move_down_canvas(event):
    canvas.move(canvas_image, 0, 10)

def move_left_canvas(event):
    canvas.move(canvas_image, -10, 0)

def move_right_canvas(event):
    canvas.move(canvas_image, 10, 0)

# Bind keys for moving the canvas image
window.bind("W", move_up_canvas)
window.bind("S", move_down_canvas)
window.bind("A", move_left_canvas)
window.bind("D", move_right_canvas)
window.bind("<Up>", move_up_canvas)
window.bind("<Down>", move_down_canvas)
window.bind("<Left>", move_left_canvas)
window.bind("<Right>", move_right_canvas)

# Start the Tkinter main loop
mainloop()
