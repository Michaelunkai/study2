import tkinter as tk

def submit():
    print("The temperature is", str(scale.get()) + " degrees Celsius")

window = tk.Tk()

scale = tk.Scale(window, from_=0, to=100, length=600, orient=tk.VERTICAL, font=("Arial", 20), tickinterval=10, showvalue=1, troughcolor="#69EAFF", bg="black")
scale.pack()

button = tk.Button(window, text="Submit", command=submit)
button.pack()

scale.set(100)

# Text labels for hot and cold
hot_label = tk.Label(text="Hot", font=("Arial", 14, "bold"), fg="red")
hot_label.pack()

cold_label = tk.Label(text="Cold", font=("Arial", 14, "bold"), fg="blue")
cold_label.pack()

window.mainloop()
