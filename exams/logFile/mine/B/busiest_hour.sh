#!/bin/bash

# Define the log file path
LOG_FILE="exam.log"

# Check if the log file exists
if [[ ! -f "$LOG_FILE" ]]; then
  echo "Error: Log file '$LOG_FILE' not found."
  exit 1
fi

# Extract the hour part from each timestamp and count occurrences
awk -F'[:[]' '{ print $3 }' "$LOG_FILE" | sort | uniq -c | sort -nr | head -1 > busiest_hour.txt

# Check if busiest_hour.txt has content
if [[ -s "busiest_hour.txt" ]]; then
  echo "The busiest hour has been extracted to 'busiest_hour.txt':"
  cat busiest_hour.txt
else
  echo "No requests were found. Please check the log file format."
fi
