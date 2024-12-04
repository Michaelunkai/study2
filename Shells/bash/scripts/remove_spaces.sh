#!/bin/bash
# Script to replace spaces with underscores in file names in the current directory.
# If a file with the target name already exists, the original file is deleted.

for file in *; do
  if [[ -f "$file" ]]; then
    new_name=$(echo "$file" | tr ' ' '_')
    if [[ "$file" != "$new_name" ]]; then
      if [[ -e "$new_name" ]]; then
        echo "File '$new_name' already exists. Removing '$file'."
        rm "$file"
      else
        mv "$file" "$new_name"
      fi
    fi
  fi
done
