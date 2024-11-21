#!/bin/ 
sudo du -am /mnt/c 2>/dev/null | /usr/bin/sort -n | tail -100 | awk '{printf "%.2f MB %s\n", $1, $2}'
