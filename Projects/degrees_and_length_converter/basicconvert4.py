import tkinter as tk
from tkinter import ttk

class UnitConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Unit Converter")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#E1DADA")
        self.style.configure("TLabel", background="#E1DADA", font=('Arial', 12))
        self.style.configure("TRadiobutton", background="#E1DADA", font=('Arial', 10))
        self.style.configure("TButton", background="#5A5A5A", foreground="white", font=('Arial', 12))

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.master)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame.columnconfigure(1, weight=1)

        self.label = ttk.Label(frame, text="Choose conversion:")
        self.label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        self.choice_var = tk.StringVar()
        self.choice_var.set("1")

        self.choices = [
            ("Fahrenheit to Celsius", "1"),
            ("Celsius to Fahrenheit", "2"),
            ("Inches to Centimeters", "3"),
            ("Centimeters to Inches", "4"),
        ]

        row_num = 1
        for text, value in self.choices:
            choice_radio = ttk.Radiobutton(frame, text=text, variable=self.choice_var, value=value)
            choice_radio.grid(row=row_num, column=0, columnspan=2, sticky="w", padx=(0, 20))
            row_num += 1

        self.entry_label = ttk.Label(frame, text="Enter value:")
        self.entry_label.grid(row=row_num, column=0, pady=5, sticky="w")

        self.entry_var = tk.DoubleVar()
        self.entry_entry = ttk.Entry(frame, textvariable=self.entry_var)
        self.entry_entry.grid(row=row_num, column=1, pady=5, sticky="ew")

        self.convert_button = ttk.Button(frame, text="Convert", command=self.convert)
        self.convert_button.grid(row=row_num + 1, column=0, columnspan=2, pady=(10, 0))

        self.result_label = ttk.Label(frame, text="")
        self.result_label.grid(row=row_num + 2, column=0, columnspan=2, pady=10)

    def convert(self):
        choice = int(self.choice_var.get())
        value = self.entry_var.get()

        if choice == 1:
            result = fahrenheit_to_celsius(value)
            unit_from = "Fahrenheit"
            unit_to = "Celsius"
        elif choice == 2:
            result = celsius_to_fahrenheit(value)
            unit_from = "Celsius"
            unit_to = "Fahrenheit"
        elif choice == 3:
            result = inches_to_centimeters(value)
            unit_from = "Inches"
            unit_to = "Centimeters"
        elif choice == 4:
            result = centimeters_to_inches(value)
            unit_from = "Centimeters"
            unit_to = "Inches"
        else:
            result = None

        if result is not None:
            self.result_label.config(text=f"{value} {unit_from} is equal to {result:.2f} {unit_to}")
        else:
            self.result_label.config(text="Invalid choice. Please select a conversion.")

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def inches_to_centimeters(inches):
    return inches * 2.54

def centimeters_to_inches(centimeters):
    return centimeters / 2.54

def main():
    root = tk.Tk()
    app = UnitConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
