#!/bin/bash

# Find the 5 latest created files and display their full paths
latest_files=$(ls -tp | grep -v '/$' | head -5)

if [ -n "$latest_files" ]; then
    while IFS= read -r file; do
        # Only process if file is not empty (handles case where there are fewer than 5 files)
        if [ -n "$file" ]; then
            realpath "$file"
        fi
    done <<< "$latest_files"
else
    echo "No files found in the current directory."
fi

