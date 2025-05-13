#!/bin/bash
# Script to display sizes of files and folders in the current working directory, ranked from largest to smallest,
# and then display a tree structure of the current directory.

# Display sizes of files and folders ranked from largest to smallest
du -h --max-depth=1 "$PWD" | sort -hr | awk '{sub(/^ +/,""); size=$1; $1=""; print size "\t" $0}'

# Display tree structure of the current directory
echo -e "\nDirectory Tree:"
tree "$PWD"
