import requests
import tkinter as tk
from tkinter import ttk, messagebox

def get_weather(event=None):
    user_input = city_entry.get()
    api_key = 'dcd8c4f8fe9a2165bb574775b1a23ebc'
    
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&APPID={api_key}")
    
    if weather_data.status_code == 200:
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        result_label.config(text=f"The weather in {user_input} is: {weather}\nThe temperature in {user_input} is: {temp}°C")
    else:
        messagebox.showerror("Error", "Failed to retrieve weather data. Please check your input or try again later.")

def on_entry_click(event):
    if city_entry.get() == 'Enter city...':
        city_entry.delete(0, tk.END)
        city_entry.config(fg='black')

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.bind("<Return>", get_weather)  # Bind the Return key to the get_weather function

# Set background color to light red
root.configure(bg="red")

# Set bold fonts
font_label = ('Helvetica', 12, 'bold')
font_entry = ('Helvetica', 12, 'bold')

# City Label
city_label = tk.Label(root, text="Enter city:", font=font_label, bg="#FFCCCC")
city_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

# City Entry
city_entry = ttk.Combobox(root, font=font_entry)
city_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
city_entry.insert(0, 'Enter city...')
city_entry['values'] = ['Tel Aviv', 'Jerusalem', 'Eilat', 'Bat Yam']
city_entry.bind('<FocusIn>', on_entry_click)
city_entry.bind('<Button-1>', on_entry_click)

# Get Weather Button
get_weather_button = tk.Button(root, text="Get Weather", command=get_weather, font=font_label, bg="black", fg="yellow")
get_weather_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

# Result Label
result_label = tk.Label(root, text="", font=font_label, bg="#FFCCCC")
result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')

root.mainloop()
