#!/bin/bash

# Calculate the total number of bytes transferred in all requests in the file located in the current directory
file="exam.log"
if [ -f "$file" ]; then
    total_bytes=$(awk '{sum += $10} END {print sum}' "$file")
    echo "Total bytes transferred: $total_bytes"
else
    echo "File $file not found in the current directory."
fi
