import tkinter as tk
from tkinter import messagebox

def calculate_bmi():
    height = float(height_entry.get()) / 100 # Convert cm to m
    weight = float(weight_entry.get())

    bmi = round(weight / (height * height), 2)

    messagebox.showinfo("BMI Calculator", f"Your BMI is: {bmi}")

root = tk.Tk()
root.title('BMI Calculator')

# Create labels and entries for height and weight inputs
height_label = tk.Label(root, text="Enter your height (in cm):")
weight_label = tk.Label(root, text="Enter your weight (in kg):")

height_entry = tk.Entry(root)
weight_entry = tk.Entry(root)

# Create button for calculating BMI
calculate_button = tk.Button(root, text="Calculate", command=calculate_bmi)

# Position the labels and entries using grid layout
height_label.grid(row=0, column=0)
weight_label.grid(row=1, column=0)

height_entry.grid(row=0, column=1)
weight_entry.grid(row=1, column=1)

# Position the calculate button below height and weight entries
calculate_button.grid(row=2, columnspan=2)

root.mainloop()
