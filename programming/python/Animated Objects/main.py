# main.py
from tkinter import *
import time
from ball import Ball

window = Tk()
width, height = 500, 500
window.geometry(f"{width}x{height}")

canvas = Canvas(window, width=width, height=height)
canvas.pack()

volleyball = Ball(canvas, 50, 50, 50, 2, 2, "white")  # Adjust initial position and size
tennis_ball = Ball(canvas, 100, 100, 20, 4, 3, "yellow")  # Adjust initial position and size
basketball = Ball(canvas, 150, 150, 60, 6, 5, "orange")  # Adjust initial position and size

# Animation loop
while True:
    volleyball.move()
    tennis_ball.move()
    basketball.move()

    window.update()
    time.sleep(0.01)

window.mainloop()  # Make sure to add the mainloop to run the Tkinter main loop
