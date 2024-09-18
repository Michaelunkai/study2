# buttons

from tkinter import *

count = 0

def click():
    global count
    count+=1
    print(count)

window = Tk()
# add png file to the same folder
# photo = PhotoImage(file='image.png')

Button = Button(window,
                text="This is misha's text",
                command=click,
                font=("Comic sans",30),
                fg="#00FF00",
                bg="black",
                activeforeground="#00FF00",
                activebackground="black",
                state=ACTIVE)
                # compound='bottom') #will set the png image under the text 

Button.pack()

window.mainloop()