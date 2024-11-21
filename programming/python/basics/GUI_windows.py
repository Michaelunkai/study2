# # GUI windows

# from tkinter import *

# # windows vs wighets:
# # widgets = GUI elemets: buttons, textboxes, labels, images
# # windows = serves as a container to hold or contain these widgets

# # creating simple window:

# window = Tk()  #instantiate an instance if a window

# window.mainloop()  # place window on computer screen, listen for events
# # _____________________________________________________

from tkinter import *

window = Tk()
window.geometry("420x420")
window.title("Misha's first GUI program")

window.mainloop()