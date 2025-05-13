#!/bin/bash

# Find the latest created file and display its full path
latest_file=$(ls -tp | grep -v '/$' | head -1)
if [ -n "$latest_file" ]; then
    realpath "$latest_file"
else
    echo "No files found in the current directory."
fi
