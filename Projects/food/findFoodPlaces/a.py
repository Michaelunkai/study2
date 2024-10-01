import requests

def get_current_location():
    # Hardcoded latitude and longitude
    return "your google maps altitue"

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
        for place in places:
            name = place['name']
            vicinity = place['vicinity']
            print(f'{name} - {vicinity}')
    else:
        print('Failed to retrieve data.')

if __name__ == '__main__':
    api_key = 'api key here'
    location = get_current_location()
    print("Your current location:", location)
    radius = float(input("Enter the maximum distance from your location to search for open food places (in kilometers): "))
    find_open_food_places(api_key, location, radius)
