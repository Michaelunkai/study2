#!/bin/bash

# Update and install necessary packages
apt update && apt install -y libreoffice-writer default-jdk parallel || {
    echo "Failed to install dependencies. Please check your package manager."
    exit 1
}

# Directory to search for .docx files
SEARCH_DIR="/mnt/c/study"

# Log file for tracking conversion and errors
LOG_FILE="/tmp/docx2pdf_conversion.log"

# Function to convert a .docx file to .pdf
convert_to_pdf() {
    DOCX_FILE="$1"
    OUTPUT_DIR=$(dirname "$DOCX_FILE")
    echo "Converting: $DOCX_FILE" | tee -a "$LOG_FILE"
    lowriter --headless --convert-to pdf --outdir "$OUTPUT_DIR" "$DOCX_FILE" &>> "$LOG_FILE"
    if [ $? -eq 0 ]; then
        echo "Conversion successful: $DOCX_FILE" | tee -a "$LOG_FILE"
        rm -f "$DOCX_FILE" # Delete the original file upon success
    else
        echo "Conversion failed: $DOCX_FILE" | tee -a "$LOG_FILE"
    fi
}

# Export the function for use with parallel
export -f convert_to_pdf
export LOG_FILE

# Find all .docx files and process them in parallel
find "$SEARCH_DIR" -type f -name '*.docx' -print0 | parallel -0 convert_to_pdf

echo "All tasks completed. Check $LOG_FILE for details."

