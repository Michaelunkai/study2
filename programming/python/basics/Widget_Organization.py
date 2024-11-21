import tkinter as tk

# Step 2: Create a Window
window = tk.Tk()

# Step 3: Create Buttons in the Window
button = tk.Button(window, text="W", font=("console", 25), width=3)
button.pack()

# Step 4: Add More Buttons
buttons = ["A", "S", "D"]
for btn_text in buttons:
    button = tk.Button(window, text=btn_text, font=("console", 25), width=3)
    button.pack(side="left")

# Step 5: Create a Frame and Add Buttons to It
frame = tk.Frame(window)
frame.pack()
for btn_text in buttons:
    button = tk.Button(frame, text=btn_text, font=("console", 25), width=3)
    button.pack(side="left")

# Step 6: Customize Frame Appearance
frame.configure(bg="pink", bd=5, relief="sunken")

# Step 7: Adjust Frame Placement
frame.pack(side="bottom")

# Step 8: Understanding the Place Function
frame.place(x=100, y=100)

# Step 9: Finalize and Run
window.mainloop()
