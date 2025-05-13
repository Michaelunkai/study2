#!/bin/bash

set -e
set -u
set -o pipefail

echo "Starting deep system cleanup for Ubuntu WSL2..."

# 1. Update & Upgrade System
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# 2. Install deborphan for orphaned package cleanup
echo "Installing deborphan..."
sudo apt install deborphan -y

# 3. Remove orphaned, unused, and unnecessary packages
echo "Removing unused packages and dependencies..."
sudo apt autoremove --purge -y
sudo apt autoclean -y
sudo apt clean -y

# 4. Purge residual package configurations
echo "Purging residual package configurations..."
export DEBIAN_FRONTEND=noninteractive
sudo dpkg --configure -a
sudo dpkg -l | awk '/^rc/ {print $2}' | xargs -r sudo apt purge -y

# 5. Remove system logs, cache, and temporary files
echo "Clearing logs, cache, and temporary files..."
sudo find /var/log -type f -exec truncate -s 0 {} +
sudo find /var/log -name "*.gz" -exec rm -f {} +
sudo find /var/log -regex ".*\.[0-9]+" -exec rm -f {} +
sudo rm -rf /var/cache/*
sudo rm -rf ~/.cache/*
sudo rm -rf ~/.local/share/Trash/*
sudo rm -rf ~/.cache/thumbnails/*
sudo rm -rf /tmp/* /var/tmp/*

# 6. Remove old kernels (safe in WSL)
echo "Removing old kernels..."
sudo apt remove --purge -y $(dpkg --list | awk '/^ii  linux-image-[0-9]/{print $2}' | grep -v $(uname -r)) || true

# 7. Remove orphaned libraries using deborphan
echo "Removing orphaned libraries..."
sudo deborphan | xargs -r sudo apt-get -y remove --purge

# 8. Remove non-essential system services
echo "Disabling and removing unnecessary services..."
sudo systemctl disable --now apport.service || true
sudo systemctl disable --now whoopsie || true
sudo systemctl disable --now motd-news.timer || true
sudo systemctl disable --now unattended-upgrades || true

# 9. Remove unnecessary fonts and language packs
echo "Removing unused fonts and language packs..."
sudo apt remove --purge -y fonts-* 
sudo apt remove --purge -y language-pack-*

# 10. Remove documentation, manuals, and info pages
echo "Removing manuals, docs, and info pages..."
sudo rm -rf /usr/share/man/*
sudo rm -rf /usr/share/doc/*
sudo rm -rf /usr/share/info/*
sudo rm -rf /usr/share/lintian/*
sudo rm -rf /usr/share/linda/*

# 11. Remove Snap and crash reporting
echo "Removing Snap and whoopsie..."
sudo systemctl stop snapd || true
sudo apt-get remove --purge -y snapd whoopsie

# 12. Remove large orphaned files and logs
echo "Cleaning orphaned logs and crash reports..."
sudo rm -rf /var/crash/*
sudo rm -rf /var/lib/systemd/coredump/*
sudo rm -rf /var/lib/apport/coredump/*
sudo rm -rf ~/.xsession-errors*
sudo journalctl --vacuum-time=1d

# 13. Remove temporary SSH host keys (safe in WSL)
echo "Removing temporary SSH host keys..."
sudo rm -rf /etc/ssh/ssh_host_*

# 14. Remove broken symbolic links
echo "Cleaning up broken symlinks..."
sudo find / -xdev -xtype l -delete

# 15. Remove system thumbnail cache (gnome, kde)
echo "Clearing system-wide thumbnail cache..."
sudo rm -rf ~/.thumbnails ~/.cache/thumbnails

# 16. Remove unused locale data
echo "Removing unused locales..."
sudo locale-gen --purge en_US.UTF-8

# 17. Identify and remove large files (interactive)
echo "Finding large unused files..."
sudo find / -xdev -type f -size +50M ! -path "/proc/*" ! -path "/sys/*" ! -path "/dev/*" -exec ls -lh {} +
read -p "Delete these large files? (y/n): " CONFIRM
if [[ "$CONFIRM" == "y" ]]; then
    sudo find / -xdev -type f -size +50M ! -path "/proc/*" ! -path "/sys/*" ! -path "/dev/*" -exec rm -f {} +
fi

# 18. Remove unnecessary icon cache
echo "Clearing icon cache..."
rm -rf ~/.icons ~/.local/share/icons ~/.cache/icon-cache.kcache

# 19. Remove old system snapshots (timeshift, etc.)
echo "Cleaning old system snapshots..."
sudo rm -rf /var/lib/snapshots/* || true

# 20. Zero-fill free disk space for WSL2 compaction
echo "Zero-filling disk space for WSL2 optimization..."
sudo dd if=/dev/zero of=/EMPTY bs=1M || true
sudo rm -f /EMPTY

# 21. Defragment system files (safe in WSL)
if command -v e4defrag &> /dev/null; then
    echo "Defragmenting filesystem..."
    sudo e4defrag /
fi

# 22. Optimize apt package lists
echo "Rebuilding package lists..."
sudo rm -rf /var/lib/apt/lists/*
sudo apt update

# 23. Final disk space usage check
echo "Final disk space usage:"
df -h

# 24. Remove leftover dpkg files
echo "Clearing residual dpkg files..."
sudo rm -rf /var/lib/dpkg/info/*
sudo rm -rf /var/lib/apt/lists/*
sudo rm -rf /var/lib/polkit-1/*
sudo rm -rf /var/log/alternatives.log
sudo rm -rf /usr/lib/x86_64-linux-gnu/dri/*
sudo rm -rf /usr/share/python-wheels/*
sudo rm -rf /var/cache/apt/pkgcache.bin
sudo rm -rf /var/cache/apt/srcpkgcache.bin

# 25. Purge deborphan
echo "Purging deborphan..."
sudo apt purge -y deborphan

echo "Deep WSL2 cleanup completed successfully!"
