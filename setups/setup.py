# setup.py
# Ensure Tkinter is installed: pip install tk
from tkinter import *

window = Tk()
width, height = 500, 500
window.geometry(f"{width}x{height}")

canvas = Canvas(window, width=width, height=height)
canvas.pack()
