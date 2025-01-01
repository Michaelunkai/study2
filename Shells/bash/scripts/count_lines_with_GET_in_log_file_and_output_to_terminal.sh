#!/bin/bash

# Count the number of lines containing 'GET' in the file located in the current directory
file="exam.log"
if [ -f "$file" ]; then
    count=$(grep -c 'GET' "$file")
    echo "Number of lines containing 'GET': $count"
else
    echo "File $file not found in the current directory."
fi
