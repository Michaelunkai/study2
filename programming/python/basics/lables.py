# lables

# from tkinter import * 

# # label = an area widget that holds text and/or an image within a windows

# window = Tk()

# label = Label(window, text="Hello World")
# label.pack()

# window.mainloop()
# _______________________________________________-
# from tkinter import * 

# window = Tk()

# label = Label(window, text="Hello World")
# label.place()

# window.mainloop()
# ______________________________________________-
# example:
# from tkinter import * 

# window = Tk()

# label = Label(window, text="Hello World")
# label.place(x=0,y=0)

# window.mainloop()
# _______________________________________________

# from tkinter import * 

# window = Tk()

# label = Label(window, text="Hello World",font=('Ariel',40,'bold'))
# label.pack()

# window.mainloop()
# __________________________________________________-
# from tkinter import * 

# window = Tk()

# label = Label(window, text="Hello World",font=('Ariel',40,'bold'),fg='green',bg='red')
# label.pack()

# window.mainloop()
# fg = front color #bg = background color
# _________________________________________________________
# from tkinter import * 

# window = Tk()

# label = Label(window,
#                text="Hello World",
#                font=('Ariel',40,'bold'),
#                fg='blue',
#                bg='black',
#                relief=RAISED,
#                bd=10)
# label.pack()

# window.mainloop()
# _______________________________________________
# another relief:
# from tkinter import * 

# window = Tk()

# label = Label(window,
#                text="Hello World",
#                font=('Ariel',40,'bold'),
#                fg='blue',
#                bg='black',
#                relief=SUNKEN,
#                bd=10,
#                padx=20
#                pady=20)
# label.pack()

# window.mainloop()
# ______________________________________________

# add photo:
from tkinter import * 

window = Tk()

photo = PhotoImage(file='path\\to\\image.png')

label = Label(window,
               text="Hello World",
               font=('Ariel',40,'bold'),
               fg='blue',
               bg='black',
               relief=SUNKEN,
               bd=10,
               padx=20,
               pady=20)
label.pack()

window.mainloop()