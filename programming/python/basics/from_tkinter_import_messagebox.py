from tkinter import messagebox
import tkinter as tk

window = tk.Tk()

def click():
    messagebox.showinfo("This is an info message box", "You are a person. Click me.")

button = tk.Button(window, text="Click me", command=click)
button.pack()

# Warning message box
messagebox.showwarning("Warning", "You have a virus")

# Error message box
messagebox.showerror("Error", "Something went wrong")

# Ask OK, Cancel message box
response = messagebox.askokcancel("Ask OK, Cancel", "Do you want to do the thing?")
if response:
    print("You did a thing")
else:
    print("You canceled a thing")

# Ask Retry, Cancel message box
response = messagebox.askretrycancel("Ask Retry, Cancel", "Do you want to retry the thing?")
if response:
    print("You retried a thing")
else:
    print("You canceled a thing")

# Ask Yes, No message box
response = messagebox.askyesno("Ask Yes, No", "Do you like cake?")
if response:
    print("I like cake too")
else:
    print("Why do you not like cake?")

# Ask Question message box
answer = messagebox.askquestion("Ask Question", "Do you like pie?")
if answer == "yes":
    print("I like pie too")
else:
    print("Why do you not like pie?")

# Ask Yes, No, Cancel message box with icon
answer = messagebox.askyesnocancel("Ask OK, Cancel", "Do you want to do the thing?")
if response:
    print("You did a thing!")
else:
    print("You cancled a thing!")

# Step 5: Additional message boxes

# Ask Retry, Cancel message box
response = messagebox.askretrycancel("Ask Retry, Cancel", "Do you want to retry the thing?")
if response:
    print("You retried a thing")
else:
    print("You camceld a thing")

# Ask Yes, No message box
response = messagebox.askyesno("Ask Yes, No", "Do you like cake?")
if response:
    print("I like cake too")
else:
    print("Why do you not like cake?")

# Ask Question message box
answer = messagebox.askquestion("Ask Question", "Do you like pie?")
if answer == "yes":
    print("I like pie too")
else:
    print("Why do you not like pie?")

# Step 6: Ask Yes, No, Cancel message box with icon
answer = messagebox.askyesnocancel("Yes, No, Cancel", "Do you like to code?", icon='warning')
if answer is True:
    print("You like to code")
elif answer is False:
    print("Why are you watching a video on coding?")
else:
    print("You have dodged the question")

# Step 7: Change the icon of the message box
# Change icon to warning
messagebox.showinfo("Custom Icon", "This has a warning icon", icon='warning')
