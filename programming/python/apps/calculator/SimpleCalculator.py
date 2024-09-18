from tkinter import Tk, Label, Button, StringVar, Frame

def button_press(num):
    global equation_text
    equation_text = equation_text + str(num)
    equation_var.set(equation_text)

def equals():
    global equation_text
    try:
        total = eval(equation_text)
        equation_text = str(total)
        equation_var.set(equation_text)
    except ZeroDivisionError:
        equation_var.set("Arithmetic Error")
        equation_text = ""
    except SyntaxError:
        equation_var.set("Syntax Error")
        equation_text = ""

def clear():
    global equation_text
    equation_var.set("")
    equation_text = ""

# Create the GUI window
window = Tk()
window.title("Calculator Program")
window.geometry("500x500")
equation_text = ""
equation_var = StringVar()

# Create and display the label
equation_label = Label(window, textvariable=equation_var, font=("Arial", 12), bg="white", width=24, height=2)
equation_label.pack()

# Create and display buttons
frame = Frame(window)
frame.pack()

buttons = [
    ("1", 0, 0, 4, 9), ("2", 0, 1, 4, 9), ("3", 0, 2, 4, 9),
    ("4", 1, 0, 4, 9), ("5", 1, 1, 4, 9), ("6", 1, 2, 4, 9),
    ("7", 2, 0, 4, 9), ("8", 2, 1, 4, 9), ("9", 2, 2, 4, 9),
    ("0", 3, 0, 4, 9), (".", 3, 1, 4, 9), ("=", 3, 2, 4, 9),
    ("+", 0, 3, 4, 9), ("-", 1, 3, 4, 9), ("*", 2, 3, 4, 9), ("/", 3, 3, 4, 9),
    ("Clear", 4, 0, 1, 12)
]

for btn_text, r, c, h, w in buttons:
    btn = Button(frame, text=btn_text, height=h, width=w, font=("Arial", 12))
    if btn_text != "Clear":
        btn["command"] = lambda text=btn_text: button_press(text) if text != "=" else equals()
    else:
        btn["command"] = clear
    btn.grid(row=r, column=c)

# Run the program
window.mainloop()
