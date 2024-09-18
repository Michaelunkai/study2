import requests
import tkinter as tk
from tkinter import ttk

def find_open_food_places(api_key, location, radius):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'key': api_key,
        'location': location,
        'radius': radius * 1000,  # Convert to meters
        'type': 'restaurant',  # filter for restaurants
        'opennow': 'true'  # filter for currently open places
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        places = data['results']
        for i, place in enumerate(places, start=1):
            name = place['name']
            vicinity = place['vicinity']
            place_id = place['place_id']
            phone_number = get_phone_number(api_key, place_id)
            opening_hours = get_opening_hours(api_key, place_id)
            result_text.insert(tk.END, f'{i}. {name} - {vicinity} - Phone: {phone_number}\n')
            if opening_hours:
                result_text.insert(tk.END, f'   Opening hours: {opening_hours}\n')
    else:
        result_text.insert(tk.END, 'Failed to retrieve data.\n')

def get_phone_number(api_key, place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'key': api_key,
        'place_id': place_id
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        return data['result'].get('formatted_phone_number', 'Phone number not available')
    else:
        return 'Phone number not available'

def get_opening_hours(api_key, place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'key': api_key,
        'place_id': place_id,
        'fields': 'opening_hours'
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        opening_hours = data['result'].get('opening_hours', {})
        if 'weekday_text' in opening_hours:
            return '\n'.join(opening_hours['weekday_text'])
    return None

def get_radius():
    try:
        radius = float(radius_entry.get())
        find_open_food_places(api_key_entry.get(), get_current_location(), radius)
    except ValueError:
        result_text.insert(tk.END, 'Invalid input for radius.\n')

def get_current_location():
    # Hardcoded latitude and longitude
    return "alltitude, here!"

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Open Food Places")
    root.geometry("800x600")  # Set a fixed window size

    # Define font styles
    title_font = ("Helvetica", 16, "bold")
    label_font = ("Helvetica", 12)
    entry_font = ("Helvetica", 12)

    # Set background color
    root.configure(bg="#F0F0F0")

    # Create a main frame to hold the widgets
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # API key label and entry
    api_key_label = ttk.Label(main_frame, text="Enter your Google Places API Key:", font=label_font)
    api_key_label.pack(pady=5)

    api_key_entry = ttk.Entry(main_frame, font=entry_font)
    api_key_entry.pack(pady=5)
    api_key_entry.insert(tk.END, "api key here")  # Insert the API key

    # Radius label and entry
    radius_label = ttk.Label(main_frame, text="Enter the maximum distance from your location to search for open food places (in kilometers):", font=label_font, wraplength=400)
    radius_label.pack(pady=5)

    radius_entry = ttk.Entry(main_frame, font=entry_font)
    radius_entry.pack(pady=5)

    # Search button
    search_button = ttk.Button(main_frame, text="Search", command=get_radius, style="Accent.TButton")
    search_button.pack(pady=10)

    # Result label
    result_label = ttk.Label(main_frame, text="Results:", font=title_font)
    result_label.pack(pady=10)

    # Result text box
    result_text = tk.Text(main_frame, height=20, width=80, font=entry_font)
    result_text.pack(pady=10)

    # Configure the style
    style = ttk.Style()
    style.theme_use("clam")  # Set the theme
    style.configure("Accent.TButton", foreground="white", background="#4CAF50")  # Configure the accent color for the button

    root.mainloop()