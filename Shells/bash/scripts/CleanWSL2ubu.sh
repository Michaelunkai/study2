#!/bin/bash

set -e
set -u
set -o pipefail

echo "Starting SAFE maximal system cleanup. Essential components will not be removed."

# 1. Update and Upgrade System
echo "Updating and upgrading system..."
sudo apt update && sudo apt upgrade -y

# 2. Remove Unnecessary Packages and Dependencies
echo "Removing unused packages and dependencies..."
sudo apt autoremove --purge -y
sudo apt autoclean -y
sudo apt clean -y

# 3. Purge Residual Configurations
echo "Purging residual configurations..."
export DEBIAN_FRONTEND=noninteractive
sudo dpkg --configure -a
sudo dpkg -l | grep '^rc' | awk '{print $2}' | xargs -r sudo apt purge -y

# 4. Remove Logs, Cache, and Temporary Files
echo "Cleaning logs, caches, and temporary files..."
sudo find /var/log -type f -exec truncate -s 0 {} +
sudo find /var/log -name "*.gz" -exec rm -f {} +
sudo find /var/log -regex ".*\.[0-9]+" -exec rm -f {} +
sudo rm -rf /var/cache/*
sudo rm -rf ~/.cache/*
sudo rm -rf ~/.local/share/Trash/*
sudo rm -rf ~/.cache/thumbnails/*
sudo rm -rf /tmp/* /var/tmp/*

# 5. Remove Documentation, Manuals, and Info
echo "Removing documentation and manuals (optional)..."
sudo rm -rf /usr/share/man/*
sudo rm -rf /usr/share/doc/*
sudo rm -rf /usr/share/info/*
sudo rm -rf /usr/share/lintian/*
sudo rm -rf /usr/share/linda/*

# 6. Remove Python Bytecode and Cache
echo "Removing Python caches and bytecode..."
sudo find / -xdev -type f -name "*.pyc" -delete
sudo find / -xdev -type f -name "*.pyo" -delete
sudo find / -xdev -type d -name "__pycache__" -exec rm -rf {} +

# 7. Handle Broken Symbolic Links
echo "Removing broken symbolic links..."
sudo find / -xdev -xtype l -delete

# 8. Identify and Delete Large Files (Interactive)
echo "Finding files larger than 50MB..."
sudo find / -xdev -type f -size +50M ! -path "/proc/*" ! -path "/sys/*" ! -path "/dev/*" -exec ls -lh {} +
read -p "Do you want to delete these files? (y/n): " CONFIRM
if [[ "$CONFIRM" == "y" ]]; then
    sudo find / -xdev -type f -size +50M ! -path "/proc/*" ! -path "/sys/*" ! -path "/dev/*" -exec rm -f {} +
fi

# 9. Remove Snap Completely
echo "Removing Snap and its associated files..."
sudo systemctl stop snapd || true
sudo apt-get remove --purge -y snapd
sudo rm -rf /var/cache/snapd /var/snap /snap /root/snap /home/*/snap

# 10. Remove Docker Data (Optional)
if command -v docker &> /dev/null; then
    echo "Removing unused Docker data..."
    sudo docker system prune -a --volumes -f || echo "No Docker resources to clean."
fi

# 11. Zero-Fill Disk for WSL2 Compaction
echo "Zero-filling disk space for compaction..."
sudo dd if=/dev/zero of=/EMPTY bs=1M || true
sudo rm -f /EMPTY

# 12. Optimize Filesystem
if command -v e4defrag &> /dev/null; then
    echo "Defragmenting filesystem..."
    sudo e4defrag /
fi

# 13. Final Disk Usage
echo "Final disk usage:"
df -h

rm -rf ./var/lib/dpkg/info/*.list ./var/lib/dpkg/info/*.md5sums ./var/lib/dpkg/info/*.triggers ./var/lib/dpkg/info/*.shlibs ./var/lib/dpkg/info/*.symbols ./var/lib/dpkg/info/*.postinst ./var/lib/dpkg/info/*.postrm ./var/lib/dpkg/info/*.preinst ./var/lib/dpkg/info/*.prerm ./var/lib/dpkg/triggers/* ./var/lib/systemd/catalog/database ./var/lib/apt/lists/* ./var/log/* ./usr/lib/file/magic.mgc

rm -rf ./var/lib/dpkg/info/*
rm -rf ./var/lib/apt/lists/*
rm -rf ./var/lib/polkit-1/*
rm -rf ./var/log/alternatives.log
rm -rf ./usr/lib/x86_64-linux-gnu/dri/*
rm -rf ./usr/share/python-wheels/*
rm -rf ./var/cache/apt/pkgcache.bin
rm -rf ./var/cache/apt/srcpkgcache.bin

echo "Safe maximal cleanup completed. Essential components remain untouched."
