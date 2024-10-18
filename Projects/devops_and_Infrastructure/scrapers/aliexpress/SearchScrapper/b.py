# file path: c:/study/python/apps/scrapers/aliexpress/SearchScrapper/b.py

from crawlbase import CrawlingAPI
import json

# Currency conversion function
def convert_currency(price, currency):
    currency_symbols = {'USD': '$', 'ILS': '₪'}
    return f"{currency_symbols.get(currency, '')}{price}"

# Initialize the Crawlbase API with your API token
api_token = 'your-api-key'
api = CrawlingAPI({'token': api_token})

# Define the URL of the AliExpress search page you want to scrape
aliexpress_search_url = 'https://www.aliexpress.com/wholesale?SearchText=papers'

try:
    # Make an HTTP GET request to the specified URL using the 'aliexpress-serp' scraper
    response = api.get(aliexpress_search_url, {'scraper': 'aliexpress-serp', 'numResults': 20})

    print("Response Status Code:", response['status_code'])

    # Check if the request was successful
    if response['status_code'] == 200:
        response_json = json.loads(response['body'].decode('utf-8'))
        scraper_result = response_json['body']

        print("Scraper Result:", scraper_result)

        products = scraper_result.get('products', [])
        if not products:
            print("No products found.")
        else:
            product_info = [
                (product.get('title', 'Title Not Found'),
                 product.get('url', 'N/A'),
                 convert_currency(product.get('price', {}).get('current', 'Price Not Found'), product.get('price', {}).get('currency', '')))
                for product in products
            ]

            for title, url, price in product_info:
                print(f"Product Title: {title}")
                print(f"Product Price: {price}")
                print(f"Product URL: {url}\n")

    else:
        print(f"Failed to fetch data from {aliexpress_search_url}. Status code: {response['status_code']}")
except Exception as e:
    print(f"An error occurred: {e}")
