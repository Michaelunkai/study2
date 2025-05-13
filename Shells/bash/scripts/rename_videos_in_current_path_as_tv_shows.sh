#!/bin/ 

# Initialize episode counter
counter=1

# Find all video files in the current directory, handle special characters safely
find . -maxdepth 1 -type f \( -iname "*.mp4" -o -iname "*.mkv" -o -iname "*.avi" \) -print0 | sort -z | while IFS= read -r -d '' file; do
    # Extract the filename without the leading './'
    filename="${file#./}"

    # Determine the file extension
    extension="${filename##*.}"

    # Generate the new filename with zero-padded episode number
    newname="s01e$(printf "%02d" "$counter").${extension}"

    # Rename the file safely
    mv -- "$filename" "$newname"

    # Increment the counter
    counter=$((counter + 1))
done
