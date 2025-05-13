#!/bin/bash
# Change to the target directory
cd /mnt/c/study || { echo "Directory /mnt/c/study not found"; exit 1; }

echo "Listing changes from the oldest modification date to now..."

# Get a sorted, unique list of files with modification timestamps.
# Format: YYYY-MM-DD HH:MM:SS <filepath>
find_output=$(find . -type f -printf '%TY-%Tm-%Td %TH:%TM:%.2TS %p\n' 2>/dev/null | sort | uniq)

# Define an array of ANSI color codes (red, green, yellow, blue, magenta, cyan).
colors=( "\e[31m" "\e[32m" "\e[33m" "\e[34m" "\e[35m" "\e[36m" )
reset="\e[0m"

current_date=""
color_index=0
day_counter=0

# Process each line of the find output.
echo "$find_output" | while IFS= read -r line; do
    # Extract the date (first 10 characters: YYYY-MM-DD)
    line_date="${line:0:10}"
    
    # When encountering a new date group:
    if [ "$line_date" != "$current_date" ]; then
        # If this is not the very first group, print a separator line.
        if [ -n "$current_date" ]; then
            echo -e "${reset}_____________________________________________"
        fi
        current_date="$line_date"
        color_index=$(( (color_index + 1) % ${#colors[@]} ))
        day_counter=1
        # Optionally, print a header for the new date.
        echo -e "${colors[$color_index]}$current_date:${reset}"
    fi
    # Print the current file line with a per-day number.
    echo -e "${colors[$color_index]}${day_counter}) $line${reset}"
    day_counter=$((day_counter + 1))
done
