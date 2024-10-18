#!/bin/bash
sudo du -am /mnt/wslg 2>/dev/null | /usr/bin/sort -n | tail -100 | awk '{printf "%.2f MB %s\n", $1, $2}'
