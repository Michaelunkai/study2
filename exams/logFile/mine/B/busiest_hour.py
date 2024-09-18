#!/usr/bin/env python3

import re
from collections import Counter

# Define the log file path
LOG_FILE = 'exam.log'
OUTPUT_FILE = 'busiest_hour.txt'

# Regular expression pattern to extract the timestamp
timestamp_pattern = re.compile(r'\[(\d{2}/\w+/\d{4}):(\d{2}):\d{2}:\d{2}')

def extract_hours(log_file):
    hours = []
    try:
        with open(log_file, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                match = timestamp_pattern.search(line)
                if match:
                    hour = match.group(2)  # Extract the hour part
                    hours.append(hour)
                else:
                    # Debug: Print lines that don't match the pattern
                    print(f"Line {line_number} does not contain a valid timestamp.")
    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found.")
        exit(1)
    return hours

def find_busiest_hour(hours):
    counter = Counter(hours)
    return counter.most_common(1)

def write_output(busiest_hour, output_file):
    try:
        with open(output_file, 'w') as f:
            for hour, count in busiest_hour:
                f.write(f"{count} requests during hour {hour}:00\n")
        print(f"The busiest hour has been extracted to '{output_file}':")
        for hour, count in busiest_hour:
            print(f"{count} requests during hour {hour}:00")
    except IOError as e:
        print(f"Error writing to file '{output_file}': {e}")

def main():
    hours = extract_hours(LOG_FILE)
    if not hours:
        print("No requests were found. Please check the log file format.")
        exit(1)
    busiest_hour = find_busiest_hour(hours)
    write_output(busiest_hour, OUTPUT_FILE)

if __name__ == "__main__":
    main()
