#!/bin/bash
sudo find . -type f -exec du -am {} + 2>/dev/null | /usr/bin/sort -n | tail -100 | awk '{printf "%.2f MB %s\n", $1, $2}'
