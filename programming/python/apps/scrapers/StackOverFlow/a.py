import requests

def get_stackoverflow_results(query):
    url = "https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error: Unable to fetch results (status code {response.status_code})")
        return []

def main():
    query = input("Enter your search query: ")
    results = get_stackoverflow_results(query)

    if not results:
        print("No results found.")
        return

    for result in results:
        title = result.get('title')
        link = result.get('link')
        print(f"Title: {title}")
        print(f"Link: {link}")
        print()

if __name__ == "__main__":
    main()
