import requests

api_key = 'your-api-key'
user_input = input("Enter city: ")

weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&APPID={api_key}")

if weather_data.status_code == 200:
    weather = weather_data.json()['weather'][0]['main']
    temp = round(weather_data.json()['main']['temp'])
    print(f"The weather in {user_input} is: {weather}")
    print(f"The temperature in {user_input} is: {temp}°C")
else:
    print("Failed to retrieve weather data. Please check your input or try again later.")
