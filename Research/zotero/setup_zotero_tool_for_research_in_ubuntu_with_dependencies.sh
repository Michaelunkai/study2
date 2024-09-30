#!/bin/ 

# Step 1: Install Dependencies
sudo apt install -y libgtk-3-0 libdbus-glib-1-2 wget tar

# Step 2: Download Zotero
wget https://download.zotero.org/client/release/6.0.26/Zotero-6.0.26_linux-x86_64.tar.bz2

# Step 3: Extract the Zotero Archive
tar -xvjf Zotero-6.0.26_linux-x86_64.tar.bz2

# Step 4: Move Zotero to /opt directory
sudo mv Zotero_linux-x86_64 /opt/zotero

# Step 5: Create a symbolic link to run Zotero from anywhere
sudo ln -s /opt/zotero/zotero /usr/bin/zotero

# Step 6: Create a desktop entry to make Zotero accessible from the application menu
echo "[Desktop Entry]
Name=Zotero
Exec=/opt/zotero/zotero
Icon=/opt/zotero/chrome/icons/default/default256.png
Type=Application
Categories=Office;Education;" > ~/.local/share/applications/zotero.desktop

# Step 7: Run Zotero
zotero
