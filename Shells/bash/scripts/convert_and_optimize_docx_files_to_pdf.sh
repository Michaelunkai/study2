#!/bin/ 

# Ask for the path to the folder with DOCX files
read -p "Enter the path to the folder containing the DOCX files: " docx_folder

# Check if the path is valid
if [ ! -d "$docx_folder" ]; then
    echo "Invalid path. Please enter a valid directory."
    exit 1
fi

# Convert all DOCX files in the specified directory to PDF
for file in "$docx_folder"/*.docx; do
    if [ -f "$file" ]; then
        lowriter --convert-to pdf --outdir "$docx_folder" "$file"
    fi
done

# Optimize all PDF files in the specified directory
for pdf in "$docx_folder"/*.pdf; do
    if [ -f "$pdf" ]; then
        gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -sOutputFile="${pdf%.pdf}_optimized.pdf" "$pdf"
    fi
done
