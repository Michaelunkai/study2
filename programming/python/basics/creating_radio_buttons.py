# import tkinter as tk

# def order():
#     if x.get() == 0:
#         print("You ordered pizza")
#     elif x.get() == 1:
#         print("You ordered a hamburger")
#     elif x.get() == 2:
#         print("You ordered a hot dog")
#     else:
#         print("Huh?")

# window = tk.Tk()

# # Create a list of food items
# food = ['Pizza', 'Hamburger', 'Hot dog']

# # Create a Tkinter variable
# x = tk.IntVar()

# # Create radio buttons in a loop
# for index in range(len(food)):
#     radio_button = tk.Radiobutton(window, text=food[index], variable=x, value=index, command=order)
#     radio_button.pack(anchor='w', padx=25)
#     radio_button.config(font=('impact', 50), indicatoron=0, width=375, compound='left')

#     # Add images to radio buttons (replace with actual file paths)
#     food_images = [tk.PhotoImage(file='pizza.png'), tk.PhotoImage(file='hamburger.png'), tk.PhotoImage(file='hotdog.png')]
#     radio_button.config(image=food_images[index])

# window.mainloop()

# ____________________________________________
# without images:

import tkinter as tk

def order():
    if x.get() == 0:
        print("You ordered pizza")
    elif x.get() == 1:
        print("You ordered a hamburger")
    elif x.get() == 2:
        print("You ordered a hot dog")
    else:
        print("Huh?")

window = tk.Tk()

# Create a list of food items
food = ['Pizza', 'Hamburger', 'Hot dog']

# Create a Tkinter variable
x = tk.IntVar()

# Create radio buttons in a loop
for index in range(len(food)):
    radio_button = tk.Radiobutton(window, text=food[index], variable=x, value=index, command=order)
    radio_button.pack(anchor='w', padx=25)
    radio_button.config(font=('impact', 20), indicatoron=0, width=200, compound='left')

# Set the window size
window.geometry("400x200")

window.mainloop()
