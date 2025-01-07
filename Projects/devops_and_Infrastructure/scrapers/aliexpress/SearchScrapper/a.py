from crawlbase import CrawlingAPI
import json

# Initialize the Crawlbase API with your API token
api_token = 'Xo4che8q0dxuygu80FqwaA'
api = CrawlingAPI({'token': api_token})

# Define the URL of the AliExpress search page you want to scrape
aliexpress_search_url = 'https://www.aliexpress.com/wholesale?SearchText=smoking+papers'

try:
    # Make an HTTP GET request to the specified URL using the 'aliexpress-serp' scraper
    response = api.get(aliexpress_search_url, {'scraper': 'aliexpress-serp', 'numResults': 20})

    # Check if the request was successful
    if response['status_code'] == 200:
        # Loading JSON from response body after decoding byte data
        response_json = json.loads(response['body'].decode('latin1'))

        # Getting Scraper Results
        scraper_result = response_json['body']

        # Extracting full title and URL for each product
        product_info = [(product.get('title', 'Title Not Found'), product.get('url', 'N/A')) for product in scraper_result.get('products', [])]

        # Print scraped product titles and URL links
        for title, url in product_info:
            print(f"Product Title: {title}")
            print(f"Product URL: {url}\n")

    else:
        print(f"Failed to fetch data from {aliexpress_search_url}. Status code: {response['status_code']}")
except Exception as e:
    print(f"An error occurred: {e}")
