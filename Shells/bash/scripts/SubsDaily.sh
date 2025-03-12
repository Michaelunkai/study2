#!/bin/bash
cd /mnt/c/backup/windowsapps
sudo apt install python3.10-venv -y
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
cd /mnt/c/study/programming/python/apps/youtube/Playlists/substoplaylist
python3 h.py
exec bash
