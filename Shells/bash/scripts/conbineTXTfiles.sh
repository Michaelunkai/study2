for file in *.txt; do echo -e "\n\n\n$(basename "$file" .txt | tr '[:lower:]' '[:upper:]')\n" >> combined.txt; cat "$file" >> combined.txt; done
