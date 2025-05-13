#!/bin/bash

PASSWORD="123"

find . -type f \( -name "*.zip" -o -name "*.tar" -o -name "*.tar.gz" -o -name "*.tgz" -o -name "*.rar" -o -name "*.7z" \) -exec sh -c '
for file; do
    echo "Processing: $file"
    case "$file" in
        *.zip)
            unzip -P "$PASSWORD" -d "${file%.*}" "$file" -o >/dev/null 2>&1 || \
            7z x -p"$PASSWORD" "$file" -o"${file%.*}" -y >/dev/null 2>&1 || \
            echo "Failed to extract (possibly wrong password): $file"
            ;;
        *.tar)
            mkdir -p "${file%.*}" && tar -xf "$file" -C "${file%.*}" || echo "Failed to extract: $file"
            ;;
        *.tar.gz|*.tgz)
            mkdir -p "${file%.*}" && tar -xzf "$file" -C "${file%.*}" || echo "Failed to extract: $file"
            ;;
        *.rar)
            mkdir -p "${file%.*}" && unrar x -p"$PASSWORD" "$file" "${file%.*}" -o+ >/dev/null 2>&1 || echo "Failed to extract: $file"
            ;;
        *.7z)
            mkdir -p "${file%.*}" && 7z x -p"$PASSWORD" "$file" -o"${file%.*}" -y >/dev/null 2>&1 || echo "Failed to extract: $file"
            ;;
        *)
            echo "Unsupported file type: $file"
            ;;
    esac
done' sh {} +
