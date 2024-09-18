#!/bin/bash

# Find the most common status code in the file located in the current directory
file="exam.log"
if [ -f "$file" ]; then
    most_common_status=$(awk '{print $9}' "$file" | sort | uniq -c | sort -nr | head -n 1)
    echo "Most common status code: $most_common_status"
else
    echo "File $file not found in the current directory."
fi

