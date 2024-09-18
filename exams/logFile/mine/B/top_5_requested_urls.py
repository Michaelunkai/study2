#!/usr/bin/env python3

import re
from collections import Counter

# Define the log file path
LOG_FILE = 'exam.log'
OUTPUT_FILE = 'top5_urls.txt'

# Regular expression pattern to extract the request line
# This pattern assumes the request line is enclosed in double quotes
request_pattern = re.compile(r'"(?:GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)\s+(\S+)\s+HTTP/\d\.\d"')

def extract_urls(log_file):
    urls = []
    try:
        with open(log_file, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                match = request_pattern.search(line)
                if match:
                    url = match.group(1).split('?')[0]  # Remove query parameters
                    urls.append(url)
                else:
                    # Debug: Print lines that don't match the pattern
                    print(f"Line {line_number} does not contain a valid request.")
    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found.")
        exit(1)
    return urls

def find_top5(urls):
    counter = Counter(urls)
    return counter.most_common(5)

def write_output(top5, output_file):
    try:
        with open(output_file, 'w') as f:
            for count, url in top5:
                f.write(f"{count} {url}\n")
        print(f"Top 5 URLs have been extracted to '{output_file}':")
        for count, url in top5:
            print(f"{count} {url}")
    except IOError as e:
        print(f"Error writing to file '{output_file}': {e}")

def main():
    urls = extract_urls(LOG_FILE)
    if not urls:
        print("No URLs were extracted. Please check the log file format.")
        exit(1)
    top5 = find_top5(urls)
    write_output(top5, OUTPUT_FILE)

if __name__ == "__main__":
    main()
