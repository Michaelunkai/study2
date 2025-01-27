#!/bin/bash

PASSWORD="123"

find . -type f \( -name "*.zip" -o -name "*.tar" -o -name "*.tar.gz" -o -name "*.tgz" -o -name "*.rar" -o -name "*.7z" \) -exec sh -c '
for file; do
    echo "Processing: $file"
    case "$file" in
        *.zip)
            # Try unzip first, then fallback to 7z
            unzip -P "$PASSWORD" -d "${file%.*}" "$file" 2>/dev/null || \
            7z x -p"$PASSWORD" "$file" -o"${file%.*}" 2>/dev/null || \
            echo "Failed to extract (possibly wrong password): $file"
            ;;
        *.tar)
            mkdir -p "${file%.*}" && tar -xf "$file" -C "${file%.*}" || echo "Failed to extract: $file"
            ;;
        *.tar.gz|*.tgz)
            mkdir -p "${file%.*}" && tar -xzf "$file" -C "${file%.*}" || echo "Failed to extract: $file"
            ;;
        *.rar)
            mkdir -p "${file%.*}" && unrar x -p"$PASSWORD" "$file" "${file%.*}" 2>/dev/null || echo "Failed to extract: $file"
            ;;
        *.7z)
            mkdir -p "${file%.*}" && 7z x -p"$PASSWORD" "$file" -o"${file%.*}" 2>/dev/null || echo "Failed to extract: $file"
            ;;
        *)
            echo "Unsupported file type: $file"
            ;;
    esac
done' sh {} +
