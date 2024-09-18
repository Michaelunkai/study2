import tkinter as tk

# Define submit
def submit():
    food = [listbox.get(index) for index in listbox.curselection()]
    print("You have ordered", ", ".join(food))

# Define add
def add():
    item = entry_box.get()
    listbox.insert(tk.END, item)
    listbox.config(height=listbox.size())

# Define delete
def delete():
    for index in reversed(listbox.curselection()):
        listbox.delete(index)
    listbox.config(height=listbox.size())

# Create the Main Window
window = tk.Tk()

# Create a Listbox Widget with MULTIPLE select mode
listbox = tk.Listbox(window, selectmode=tk.MULTIPLE, bg="#F7FFDE", font=("Constantia", 35), width=12, height=1)
listbox.pack()

# Insert Items to the Listbox
menu_items = ["Pizza", "Pasta", "Garlic Bread", "Soup", "Salad"]
for index, item in enumerate(menu_items, start=1):
    listbox.insert(index, item)
listbox.config(height=listbox.size())

# Create a Submit Button
submit_button = tk.Button(window, text="Submit", command=submit)
submit_button.pack()

# Create an Entry Box for Custom Items
entry_box = tk.Entry(window)
entry_box.pack()

# Create an Add Button
add_button = tk.Button(window, text="Add", command=add)
add_button.pack()

# Create a Delete Button
delete_button = tk.Button(window, text="Delete", command=delete)
delete_button.pack()

# Run the Main Loop
window.mainloop()
