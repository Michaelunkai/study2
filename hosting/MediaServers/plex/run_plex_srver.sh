#!/bin/bash

echo "deb https://downloads.plex.tv/repo/deb public main" | sudo tee /etc/apt/sources.list.d/plexmediaserver.list
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -
sudo apt update
sudo apt install plexmediaserver -y
sudo systemctl enable plexmediaserver
sudo systemctl start plexmediaserver
firefox http://87.70.162.212:32400/web/

