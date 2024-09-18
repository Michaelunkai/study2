#!/bin/bash
logfile="/mnt/c/Users/micha/Downloads/exam.log"

start_count=$(grep -c "Transaction.*started" "$logfile")
end_count=$(grep -c "Transaction.*ended" "$logfile")

if [[ "$start_count" -eq "$end_count" ]]; then
  echo "$start_count"
else
  echo "Unmatched transactions"
fi
