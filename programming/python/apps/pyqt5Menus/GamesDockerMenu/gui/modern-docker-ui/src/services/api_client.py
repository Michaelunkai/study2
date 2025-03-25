import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        self._handle_response(response)
        return response.json()

    def post(self, endpoint, data=None):
        response = requests.post(f"{self.base_url}/{endpoint}", json=data)
        self._handle_response(response)
        return response.json()

    def put(self, endpoint, data=None):
        response = requests.put(f"{self.base_url}/{endpoint}", json=data)
        self._handle_response(response)
        return response.json()

    def delete(self, endpoint):
        response = requests.delete(f"{self.base_url}/{endpoint}")
        self._handle_response(response)
        return response.status_code

    def _handle_response(self, response):
        if response.status_code not in range(200, 300):
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")