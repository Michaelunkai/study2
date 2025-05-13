#!/bin/bash
logfile="/mnt/c/Users/micha/Downloads/exam.log"

while IFS= read -r line
do
  if [[ -n "$line" ]]; then
    echo "$line"
    break
  fi
done < "$logfile"
