import requests

# URL of the API endpoint
url = 'https://api.example.com/data'

# Headers (if needed, for example, for authentication)
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json'
}

# Data to be sent with the request (for POST or PUT requests)
data = {
    'key1': 'value1',
    'key2': 'value2'
}

# Making a GET request
response = requests.get(url, headers=headers)

# Making a POST request
response = requests.post(url, headers=headers, json=data)

# Checking the response status code
if response.status_code == 200:
    # Successful response
    print('Success:', response.json())
else:
    # Handle error
    print('Error:', response.status_code, response.text)

