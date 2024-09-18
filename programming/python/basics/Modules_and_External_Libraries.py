#  Using modules
import math

radius = float(input("Enter the radius of a circle: "))
area = math.pi * (radius ** 2)
print("Area of the circle:", area)

# External Libraries - Installing and using requests
# Uncomment the next two lines if requests is not installed
# !pip install requests
# import requests

# Make a simple API request
# response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
# data = response.json()
# print("API Response:", data)