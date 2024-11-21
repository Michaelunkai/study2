#!/bin/ 
# Script to display sizes of files and folders in the current working directory, ranked from largest to smallest.

du -h --max-depth=1 "$PWD" | sort -hr | awk '{sub(/^ +/,""); size=$1; $1=""; print size "\t" $0}'
