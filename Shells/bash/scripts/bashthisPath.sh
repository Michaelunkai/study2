#!/bin/bash

# Description:
# This script finds the latest created or modified file in the current directory
# and outputs an alias command that runs bash with the file's full path.

# Function to generate the alias name based on the current directory's basename
generate_alias_name() {
    # Extract the basename of the current directory
    dir_basename=$(basename "$(pwd)")

    # Use awk to split the basename by spaces and take the first two characters of each word
    alias_suffix=$(echo "$dir_basename" | awk '{
        split($0, a, " ");
        for (i=1; i<=length(a); i++) {
            # To handle multiple words, take first two letters of each
            for(j=1; j<=NF; j++) {
                if(length(a[j]) >=2){
                    printf substr(a[j],1,2)
                } else {
                    printf substr(a[j],1,1)
                }
            }
        }
    }')

    # Prepend 's' to form the alias name
    echo "s${alias_suffix}"
}

# Function to find the latest created or modified file in the current directory
find_latest_file() {
    # Use 'find' to list files, sort them by modification time, and select the latest one
    latest_file=$(find "$(pwd)" -maxdepth 1 -type f -printf '%T@ %p\n' | sort -nr | head -n1 | awk '{print $2}')

    echo "$latest_file"
}

# Main Execution

# Generate the alias name
alias_name=$(generate_alias_name)

# Find the latest file
latest_file=$(find_latest_file)

# Check if a file was found
if [ -n "$latest_file" ]; then
    # Get the absolute path of the latest file
    full_path=$(realpath "$latest_file")

    # Output the alias command
    echo "alias ${alias_name}=\"bash '${full_path}'\""
else
    echo "No files found in the current directory."
fi
