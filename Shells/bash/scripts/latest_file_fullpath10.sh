#!/bin/bash

# Description:
# This script finds the latest 10 modified files in the current directory
# and outputs their full absolute paths.

# Enable null character as the internal field separator to handle filenames with spaces
IFS=$'\n'

# Use 'find' to list files in the current directory, get their modification times, sort them, and select the top 10
latest_files=$(find "$(pwd)" -maxdepth 1 -type f -printf '%T@ %p\n' | sort -nr | head -10 | awk '{print $2}')

# Check if any files were found
if [ -n "$latest_files" ]; then
    # Loop through each file and print its absolute path
    while IFS= read -r file; do
        # realpath converts the file path to an absolute path
        realpath "$file"
    done <<< "$latest_files"
else
    echo "No files found in the current directory."
fi
