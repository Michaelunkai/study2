# Python GUI checkbox
from tkinter import *

def display():
    if(x.get()==1):
        print("You agree!")
    else:
        print("You dont agree! ")

window = Tk()

x = IntVar()

check_button = Checkbutton(window,
                           text="i Agree to something",
                           variable=x,
                           onvalue=1,
                           offvalue=0,
                           command=display,
                           font=('Ariel',20),
                           fg='blue',
                           bg='black',
                           activeforeground='blue',
                           activebackground='black',
                           padx=25,
                           pady=10)
check_button.pack()
window.mainloop()