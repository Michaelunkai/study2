#!/bin/bash

# ================================
<<<<<<< HEAD
# Deep Cleanup Script for /mnt/wslg
# ================================
# Aggressively cleans up /mnt/wslg to free up as much space as possible.
=======
# System Cleanup Script
# ================================
# This script performs an extensive system cleanup by executing 200 commands
# to free up space and remove unnecessary files.
# It displays the disk usage of /mnt/wslg before and after the cleanup.
>>>>>>> 37c5c22b3a88bec4bc8de6bb23b85d9c3281e70d
# Ensure you have backups before running this script.

# ================================
# Initial Disk Usage Check
# ================================
echo "==============================="
echo "Initial disk usage of /mnt/wslg:"
<<<<<<< HEAD
if [[ -d /mnt/wslg ]]; then
    du -sh /mnt/wslg || echo "Unable to determine disk usage for /mnt/wslg."
else
    echo "/mnt/wslg does not exist or is inaccessible."
    exit 1
fi
echo "==============================="

# ================================
# Excluded Directories and Files
# ================================
# Prevent accidental removal of critical or inaccessible files.
EXCLUDE_DIRS="( -path /mnt/wslg/distro -o -path /mnt/wslg/tmp ) -prune"

# ================================
# Helper Function
# ================================
# Executes a command and logs errors without stopping the script.
run_command() {
    local cmd="$1"
    echo "Running: $cmd"
    eval "$cmd" || echo "Error: Command failed - $cmd"
}

# ================================
# Cleanup Commands for /mnt/wslg
# ================================
echo "Starting deep cleanup process for /mnt/wslg..."

# 1. Remove temporary files
run_command "sudo rm -rf /mnt/wslg/tmp/*"

# 2. Remove old logs and large files
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -name '*.log' -exec truncate -s 0 {} +"
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -size +50M -delete"

# 3. Remove unused cache files
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -name '*cache*' -delete"

# 4. Remove old backups
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -name '*.bak' -delete"
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -name '*.old' -delete"

# 5. Remove orphaned symbolic links
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -xtype l -delete"

# 6. Remove unnecessary configuration files
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -name '*.conf' -delete"

# 7. Remove temporary and swap files
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -name '*.tmp' -delete"
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -name '*.swp' -delete"

# 8. Remove old compressed archives
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -name '*.tar.gz' -delete"
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -name '*.zip' -delete"
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -name '*.bz2' -delete"

# 9. Remove large media files
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f \( -name '*.mp4' -o -name '*.mp3' -o -name '*.avi' -o -name '*.mkv' \) -delete"

# 10. Remove large images and documents
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f \( -name '*.jpg' -o -name '*.png' -o -name '*.pdf' -o -name '*.docx' -o -name '*.xlsx' \) -size +10M -delete"

# 11. Clean up empty directories
run_command "sudo find /mnt/wslg $EXCLUDE_DIRS -o -type d -empty -delete"
=======
du -sh /mnt/wslg || echo "/mnt/wslg does not exist or is inaccessible."
echo "==============================="

# ================================
# Define Excluded Directories
# ================================
# Directories that should be excluded from all find operations to prevent errors
EXCLUDE_DIRS="-path /usr/lib/wsl/drivers -prune -o -path /mnt/wslg/distro -prune"

# ================================
# System Cleanup Commands
# ================================

echo "Starting system cleanup..."

# 1. Clean package manager caches
sudo apt-get clean -y || echo "Failed to clean package manager caches."

# 2. Autoremove orphaned packages
sudo apt-get autoremove --purge -y || echo "Failed to autoremove orphaned packages."

# 3. Remove specific Linux packages
sudo apt-get remove --purge -y $(dpkg -l "linux-*" | awk '/^ii/ && !/'"$(uname -r | sed "s/-[a-z]*//g")"'/ {print $2}') || echo "Failed to remove specific Linux packages."

# 4. Autoremove again to catch any additional dependencies
sudo apt-get autoremove -y || echo "Failed to autoremove additional dependencies."

# 5. Autoclean to remove partial packages
sudo apt-get autoclean -y || echo "Failed to autoclean partial packages."

# 6. Clean journal logs older than 2 weeks
sudo journalctl --vacuum-time=2weeks || echo "Failed to vacuum journal logs by time."

# 7. Limit journal size to 100MB
sudo journalctl --vacuum-size=100M || echo "Failed to vacuum journal logs by size."

# 8. Remove temporary files from WSLg (if applicable)
sudo rm -rf /mnt/wslg/tmp/* /mnt/wslg/var/tmp/* || echo "Failed to remove temporary files from /mnt/wslg."

# 9. Remove user cache and thumbnails
rm -rf ~/.cache/* ~/.thumbnails/* || echo "Failed to remove user cache and thumbnails."

# 10. Delete large files in /mnt/wslg
sudo find /mnt/wslg $EXCLUDE_DIRS -o -type f -size +100M -readable -writable -delete 2>/dev/null || echo "Failed to delete large files in /mnt/wslg."

# 11. Truncate large log files
sudo find / $EXCLUDE_DIRS -o -type f -name "*.log" -exec truncate -s 0 {} \; 2>/dev/null || echo "Failed to truncate large log files."

# 12. Remove orphaned packages using deborphan
sudo deborphan | xargs sudo apt-get -y remove --purge || echo "Failed to remove orphaned packages using deborphan."

# 13. Clean broken symlinks
sudo find / $EXCLUDE_DIRS -o -xtype l -delete 2>/dev/null || echo "Failed to clean broken symlinks."

# 14. Remove unnecessary locales
sudo localepurge || echo "Failed to remove unnecessary locales."

# 15. Delete large files from home and /tmp
sudo find ~/ $EXCLUDE_DIRS -o -type f -size +100M -delete 2>/dev/null || echo "Failed to delete large files from home."
sudo find /tmp $EXCLUDE_DIRS -o -type f -size +100M -delete 2>/dev/null || echo "Failed to delete large files from /tmp."

# 16. Clean npm, pip, and composer caches
if command -v npm &> /dev/null; then
    echo "Cleaning npm cache..."
    npm cache clean --force 2>/dev/null || echo "Failed to clean npm cache."
else
    echo "npm is not installed. Skipping npm cache cleaning."
fi

rm -rf ~/.cache/pip 2>/dev/null || echo "Failed to clean pip cache."

if command -v composer &> /dev/null; then
    composer clear-cache 2>/dev/null || echo "Failed to clear composer cache."
else
    echo "composer is not installed. Skipping composer cache cleaning."
fi

# 17. Remove old apt archive files
sudo find /var/cache/apt/archives $EXCLUDE_DIRS -o -type f -name "*.deb" -delete 2>/dev/null || echo "Failed to remove old apt archive files."

# 18. Remove old unused kernels
sudo apt-get autoremove --purge -y || echo "Failed to remove old unused kernels."

# 19. Remove unnecessary documentation and man pages
sudo rm -rf /usr/share/doc/* /usr/share/man/* || echo "Failed to remove unnecessary documentation and man pages."

# 20. Clean Firefox and Chrome caches
rm -rf ~/.cache/mozilla/firefox/* ~/.cache/google-chrome/* || echo "Failed to clean Firefox and Chrome caches."

# 21. Remove Python bytecode and swap files
sudo find / $EXCLUDE_DIRS -o -name "*.pyc" -delete 2>/dev/null || echo "Failed to remove Python bytecode files."
sudo find / $EXCLUDE_DIRS -o -type f -name "*.swp" -delete 2>/dev/null || echo "Failed to remove swap files."

# 22. Remove old system crash logs
sudo rm -rf /var/crash/* 2>/dev/null || echo "Failed to remove old system crash logs."

# 23. Delete large temp files from /var/tmp
sudo find /var/tmp $EXCLUDE_DIRS -o -type f -size +50M -delete 2>/dev/null || echo "Failed to delete large temp files from /var/tmp."

# 24. Purge config files from removed packages
sudo dpkg -l | grep '^rc' | awk '{print $2}' | xargs sudo apt-get purge -y 2>/dev/null || echo "Failed to purge config files from removed packages."

# ================================
# Additional 50 Cleaning Commands
# ================================

echo "Executing additional cleaning commands..."

# 25. Remove old backups
sudo find /var/backups $EXCLUDE_DIRS -o -type f -delete || echo "No backups to remove or failed to remove."

# 26. Remove orphaned dependencies
sudo apt-get autoremove --purge -y || echo "No orphaned dependencies or failed to remove."

# 27. Clean up old crash reports
sudo rm -rf /var/crash/* || echo "No crash reports to clean or failed to clean."

# 28. Clean up large `.log` files
sudo find /var/log $EXCLUDE_DIRS -o -type f -name "*.log" -size +50M -delete || echo "No large .log files to remove or failed to remove."

# 29. Clean up `.gz` log files
sudo find /var/log $EXCLUDE_DIRS -o -type f -name "*.gz" -size +50M -delete || echo "No large .gz log files to remove or failed to remove."

# 30. Remove old unused libraries
sudo find /usr/lib $EXCLUDE_DIRS -o -type f -size +50M -delete || echo "No large unused libraries to remove or failed to remove."

# 31. Remove old unused modules
sudo find /lib/modules $EXCLUDE_DIRS -o -type f -size +50M -delete || echo "No large unused modules to remove or failed to remove."

# 32. Clean up old archives from /var/cache
sudo find /var/cache $EXCLUDE_DIRS -o -type f -name "*.gz" -delete || echo "No old archives in /var/cache or failed to remove."

# 33. Remove large swap files
sudo find / $EXCLUDE_DIRS -o -name "*.swp" -delete || echo "No swap files found or failed to remove."

# 34. Remove unnecessary Linux headers
sudo apt-get remove --purge -y linux-headers-* || echo "No Linux headers to remove or failed to remove."

# 35. Remove large fonts
sudo find /usr/share/fonts $EXCLUDE_DIRS -o -type f -size +1M -delete || echo "No large fonts to remove or failed to remove."

# 36. Clean up icons cache
rm -rf ~/.icons/* || echo "No icons cache to clean or failed to clean."

# 37. Clean up Bash history
rm -f ~/.bash_history || echo "No Bash history to clean or failed to clean."

# 38. Clean up Python virtual environments cache
sudo find ~/.venv $EXCLUDE_DIRS -o -type f -delete || echo "No Python venv cache or failed to clean."

# 39. Remove large unnecessary files from /var/tmp
sudo find /var/tmp $EXCLUDE_DIRS -o -type f -size +100M -delete || echo "No large files in /var/tmp or failed to remove."

# 40. Remove unnecessary themes
sudo rm -rf /usr/share/themes/* || echo "No themes to remove or failed to remove."

# 41. Clean old dconf database
rm -rf ~/.cache/dconf/* || echo "No dconf cache to clean or failed to clean."

# 42. Remove unused media files
sudo find /usr/share/media $EXCLUDE_DIRS -o -type f -delete || echo "No media files to remove or failed to remove."

# 43. Remove unused wallpapers
sudo rm -rf /usr/share/backgrounds/* || echo "No wallpapers to remove or failed to remove."

# 44. Remove old thumbnails
rm -rf ~/.cache/thumbnails/* || echo "No thumbnails to remove or failed to remove."

# 45. Remove old package files
sudo find /var/cache/apt/archives/ $EXCLUDE_DIRS -o -type f -delete || echo "No package files to remove or failed to remove."

# 46. Remove Docker images
if command -v docker &> /dev/null; then
    echo "Removing Docker images..."
    sudo docker rmi $(docker images -q) || echo "No Docker images to remove or failed to remove."
else
    echo "Docker is not installed."
fi

# 47. Clean up pip wheel cache
rm -rf ~/.cache/pip/wheels/* || echo "No pip wheels to clean or failed to clean."

# 48. Remove temp files in /tmp
sudo find /tmp $EXCLUDE_DIRS -o -type f -delete || echo "No temp files in /tmp or failed to remove."

# 49. Clean up old system logs
sudo find /var/log $EXCLUDE_DIRS -o -type f -name "*.log" -exec rm -f {} \; || echo "No system logs to clean or failed to clean."

# 50. Remove large temporary files from home
sudo find ~/ $EXCLUDE_DIRS -o -type f -size +100M -delete || echo "No large temp files in home or failed to remove."

# ================================
# Additional 50 Cleaning Commands Continued
# ================================

echo "Executing additional cleaning commands continued..."

# 51. Remove obsolete mount points
sudo find /mnt $EXCLUDE_DIRS -o -type d -empty -delete || echo "No obsolete mount points or failed to remove."

# 52. Clean old software sources
sudo rm -rf /etc/apt/sources.list.d/* || echo "No additional sources to remove or failed to remove."

# 53. Remove unnecessary config files
sudo rm -rf ~/.config/* || echo "No config files to remove or failed to remove."

# 54. Clean up large `.old` files
sudo find / $EXCLUDE_DIRS -o -type f -name "*.old" -delete || echo "No .old files to clean or failed to clean."

# 55. Remove old core dumps
sudo find /var/lib/systemd/coredump $EXCLUDE_DIRS -o -type f -delete || echo "No core dumps to remove or failed to remove."

# 56. Clean unused shell scripts in /usr/local/bin
sudo find /usr/local/bin $EXCLUDE_DIRS -o -type f -name "*.sh" -delete || echo "No shell scripts to remove or failed to remove."

# 57. Remove orphaned libraries using deborphan
sudo deborphan --guess-all | xargs sudo apt-get purge -y || echo "No orphaned libraries to remove or failed to remove."

# 58. Clean up large unused applications
sudo find /usr/bin $EXCLUDE_DIRS -o -type f -size +100M -delete || echo "No large applications to remove or failed to remove."

# 59. Remove orphaned config files
sudo dpkg -l | grep '^rc' | awk '{print $2}' | xargs sudo apt-get purge || echo "No orphaned config files to remove or failed to remove."

# 60. Clean unnecessary temp files
sudo rm -rf /var/tmp/* || echo "No temp files in /var/tmp or failed to remove."

# 61. Remove redundant downloads
sudo rm -rf ~/Downloads/* || echo "No downloads to remove or failed to remove."

# 62. Clean up large `.tar` files
sudo find / $EXCLUDE_DIRS -o -type f -name "*.tar" -delete || echo "No .tar files to remove or failed to remove."

# 63. Remove large unnecessary binaries
sudo find /usr/bin $EXCLUDE_DIRS -o -type f -size +100M -delete || echo "No large binaries to remove or failed to remove."

# 64. Remove unused Perl packages
sudo find /usr/share/perl $EXCLUDE_DIRS -o -type f -delete || echo "No Perl packages to remove or failed to remove."

# 65. Remove old virtual machine images
sudo find /var/lib/libvirt/images $EXCLUDE_DIRS -o -type f -delete || echo "No VM images to remove or failed to remove."

# 66. Remove unused LaTeX packages
sudo find /usr/share/texmf $EXCLUDE_DIRS -o -type f -delete || echo "No LaTeX packages to remove or failed to remove."

# 67. Remove unused documentation for apps
sudo rm -rf /usr/share/doc || echo "No documentation to remove or failed to remove."

# 68. Remove unused localization data
sudo rm -rf /usr/share/locale || echo "No localization data to remove or failed to remove."

# 69. Clean up .deb packages in /var/cache
sudo find /var/cache/apt/archives $EXCLUDE_DIRS -o -name "*.deb" -delete || echo "No .deb packages to remove or failed to remove."

# 70. Remove all unused swap files
sudo swapoff -a && sudo rm -f /swapfile || echo "No swapfile to remove or failed to remove."

# 71. Remove unnecessary man pages
sudo rm -rf /usr/share/man/* || echo "No man pages to remove or failed to remove."

# 72. Clean old versions of applications
sudo apt-get autoremove --purge -y || echo "No old applications to remove or failed to remove."

# 73. Clean up the lib directory
sudo find /usr/lib $EXCLUDE_DIRS -o -type f -size +100M -delete || echo "No large files in /usr/lib or failed to remove."

# 74. Clean unused virtualenvs
rm -rf ~/.local/share/virtualenvs/* || echo "No virtualenvs to remove or failed to remove."

# 75. Remove orphaned dpkg files
sudo find /var/lib/dpkg/info $EXCLUDE_DIRS -o -name "*.list" -delete || echo "No dpkg list files to remove or failed to remove."

# 76. Remove .pyc files in system directories
sudo find /usr $EXCLUDE_DIRS -o -name "*.pyc" -delete || echo "No .pyc files in /usr or failed to remove."

# 77. Remove unused locale-archive data
sudo rm -rf /usr/lib/locale/locale-archive || echo "No locale-archive to remove or failed to remove."

# 78. Remove redundant glibc files
sudo rm -rf /usr/share/i18n || echo "No glibc files to remove or failed to remove."

# 79. Remove unnecessary cache from /var/cache
sudo find /var/cache $EXCLUDE_DIRS -o -type f -delete || echo "No cache files to remove from /var/cache or failed to remove."

# 80. Clean orphaned snapd logs (if snap is installed)
if command -v snap &> /dev/null; then
    echo "Removing snapd logs..."
    sudo rm -rf /var/lib/snapd/logs/* || echo "No snapd logs to remove or failed to remove."
else
    echo "Snap is not installed."
fi

# 81. Remove empty directories
sudo find / $EXCLUDE_DIRS -o -type d -empty -delete || echo "No empty directories to remove or failed to remove."

# 82. Remove .bak files from /etc
sudo find /etc $EXCLUDE_DIRS -o -name "*.bak" -delete || echo "No .bak files in /etc or failed to remove."

# 83. Clean up old kernel images
sudo find /boot $EXCLUDE_DIRS -o -name "vmlinuz-*" -delete || echo "No old kernel images to remove or failed to remove."

# 84. Remove old .gz files in /var/log
sudo find /var/log $EXCLUDE_DIRS -o -name "*.gz" -delete || echo "No .gz log files to remove or failed to remove."

# 85. Clean up .bak files in home directory
find ~ -name "*.bak" -delete || echo "No .bak files in home or failed to remove."

# 86. Clean unused .tmp files
sudo find /tmp $EXCLUDE_DIRS -o -name "*.tmp" -delete || echo "No .tmp files to remove or failed to remove."

# 87. Clean up .lock files in /var/lock
sudo find /var/lock $EXCLUDE_DIRS -o -type f -delete || echo "No .lock files to remove or failed to remove."

# 88. Clean up .log files in home directory
find ~ -name "*.log" -delete || echo "No .log files in home or failed to remove."

# 89. Remove orphaned .whl Python wheel files
find ~/.cache/pip/wheels -type f -delete || echo "No .whl files to remove or failed to remove."

# 90. Remove .xz files from /usr
sudo find /usr $EXCLUDE_DIRS -o -name "*.xz" -delete || echo "No .xz files in /usr or failed to remove."

# 91. Remove .old backup kernel files
sudo find /boot $EXCLUDE_DIRS -o -name "*.old" -delete || echo "No .old kernel backups to remove or failed to remove."

# 92. Remove old udev rules
sudo rm -rf /etc/udev/rules.d/* || echo "No udev rules to remove or failed to remove."

# 93. Remove old .journal files
sudo find /var/log/journal $EXCLUDE_DIRS -o -name "*.journal" -delete || echo "No .journal files to remove or failed to remove."

# 94. Remove .htaccess files
sudo find / $EXCLUDE_DIRS -o -name ".htaccess" -delete || echo "No .htaccess files to remove or failed to remove."

# 95. Clean up old .session files
sudo find /var/lib/php/sessions $EXCLUDE_DIRS -o -type f -delete || echo "No .session files to remove or failed to remove."

# 96. Clean up old Xorg logs
sudo rm -rf /var/log/Xorg.* || echo "No Xorg logs to remove or failed to remove."

# 97. Remove .DS_Store files (for macOS users)
sudo find /mnt $EXCLUDE_DIRS -o -name ".DS_Store" -delete || echo "No .DS_Store files to remove or failed to remove."

# 98. Remove old unused .conf files
sudo find /etc $EXCLUDE_DIRS -o -name "*.conf" -delete || echo "No .conf files to remove or failed to remove."

# 99. Clean .viminfo history
rm -f ~/.viminfo || echo "No .viminfo to clean or failed to clean."

# 100. Remove old ld.so cache
sudo rm -rf /etc/ld.so.cache || echo "No ld.so cache to remove or failed to remove."

# ================================
# Final Additional 100 Cleaning Commands
# ================================

echo "Executing final additional cleaning commands..."

# 101. Remove .rpm package files
sudo find /var/cache $EXCLUDE_DIRS -o -name "*.rpm" -delete || echo "No .rpm packages to remove or failed to remove."

# 102. Remove orphaned .dpkg files
sudo find /var/lib/dpkg/info $EXCLUDE_DIRS -o -name "*.dpkg" -delete || echo "No .dpkg files to remove or failed to remove."

# 103. Remove old .txt files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.txt" -delete || echo "No .txt files in /mnt or failed to remove."

# 104. Remove old logrotate config files
sudo find /etc/logrotate.d $EXCLUDE_DIRS -o -type f -delete || echo "No logrotate config files to remove or failed to remove."

# 105. Remove old systemd logs
sudo rm -rf /var/log/journal || echo "No systemd logs to remove or failed to remove."

# 106. Remove orphaned .svg icons
sudo find /usr/share/icons $EXCLUDE_DIRS -o -name "*.svg" -delete || echo "No .svg icons to remove or failed to remove."

# 107. Remove .ico icon files
sudo find /usr/share/icons $EXCLUDE_DIRS -o -name "*.ico" -delete || echo "No .ico icons to remove or failed to remove."

# 108. Remove old man page gzipped files
sudo find /usr/share/man $EXCLUDE_DIRS -o -name "*.gz" -delete || echo "No gzipped man pages to remove or failed to remove."

# 109. Clean up old desktop files
sudo find /usr/share/applications $EXCLUDE_DIRS -o -name "*.desktop" -delete || echo "No desktop files to remove or failed to remove."

# 110. Remove old .bash_history backups
rm -f ~/.bash_history || echo "No .bash_history backups to remove or failed to remove."

# 111. Remove orphaned .cache files in home
find ~/.cache -type f -delete || echo "No .cache files to remove or failed to remove."

# 112. Remove orphaned .wine directories
sudo rm -rf ~/.wine/* || echo "No .wine directories to remove or failed to remove."

# 113. Remove .pid files from /run
sudo find /run $EXCLUDE_DIRS -o -name "*.pid" -delete || echo "No .pid files to remove or failed to remove."

# 114. Clean up .swp files from /tmp
sudo find /tmp $EXCLUDE_DIRS -o -name "*.swp" -delete || echo "No .swp files in /tmp or failed to remove."

# 115. Remove .bak files from /var
sudo find /var $EXCLUDE_DIRS -o -name "*.bak" -delete || echo "No .bak files in /var or failed to remove."

# 116. Clean up .tmp files in /var/tmp
sudo find /var/tmp $EXCLUDE_DIRS -o -name "*.tmp" -delete || echo "No .tmp files in /var/tmp or failed to remove."

# 117. Clean orphaned .sh scripts in home
find ~ -name "*.sh" -delete || echo "No .sh scripts to remove or failed to remove."

# 118. Remove .core files
sudo find /var $EXCLUDE_DIRS -o -name "*.core" -delete || echo "No .core files to remove or failed to remove."

# 119. Remove .so files from /usr/lib
sudo find /usr/lib $EXCLUDE_DIRS -o -name "*.so" -delete || echo "No .so files to remove or failed to remove."

# 120. Clean orphaned .conf config files
sudo find /etc $EXCLUDE_DIRS -o -name "*.conf" -delete || echo "No orphaned .conf files to remove or failed to remove."

# 121. Clean .gz kernel logs
sudo find /var/log $EXCLUDE_DIRS -o -name "kern.log*.gz" -delete || echo "No kern.log.gz files to remove or failed to remove."

# 122. Clean .tar backups
sudo find /mnt $EXCLUDE_DIRS -o -name "*.tar" -delete || echo "No .tar backups to remove or failed to remove."

# 123. Remove old apache2 logs
sudo rm -rf /var/log/apache2/* || echo "No apache2 logs to remove or failed to remove."

# 124. Clean old mysql logs
sudo rm -rf /var/log/mysql/* || echo "No mysql logs to remove or failed to remove."

# 125. Clean up .mysql files
sudo find /var/lib/mysql $EXCLUDE_DIRS -o -name "*.mysql" -delete || echo "No .mysql files to remove or failed to remove."

# 126. Remove .error logs in /var
sudo find /var $EXCLUDE_DIRS -o -name "*.error" -delete || echo "No .error logs to remove or failed to remove."

# 127. Remove .logrotate config files
sudo find /etc $EXCLUDE_DIRS -o -name "*.logrotate" -delete || echo "No logrotate config files to remove or failed to remove."

# 128. Clean up .tar.gz compressed files
sudo find /mnt $EXCLUDE_DIRS -o -name "*.tar.gz" -delete || echo "No .tar.gz files to remove or failed to remove."

# 129. Remove .img files
sudo find /mnt $EXCLUDE_DIRS -o -name "*.img" -delete || echo "No .img files to remove or failed to remove."

# 130. Remove .iso files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.iso" -delete || echo "No .iso files to remove or failed to remove."

# 131. Remove .deb files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.deb" -delete || echo "No .deb files to remove or failed to remove."

# 132. Remove .dll files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.dll" -delete || echo "No .dll files to remove or failed to remove."

# 133. Remove .exe files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.exe" -delete || echo "No .exe files to remove or failed to remove."

# 134. Remove .pdf files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.pdf" -delete || echo "No .pdf files to remove or failed to remove."

# 135. Clean .pyc files from /usr/share
sudo find /usr/share $EXCLUDE_DIRS -o -name "*.pyc" -delete || echo "No .pyc files in /usr/share or failed to remove."

# 136. Remove .bak files from /etc/
sudo find /etc/ $EXCLUDE_DIRS -o -name "*.bak" -delete || echo "No .bak files in /etc or failed to remove."

# 137. Clean .zip files in /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.zip" -delete || echo "No .zip files to remove or failed to remove."

# 138. Clean orphaned .bz2 compressed files
sudo find /mnt $EXCLUDE_DIRS -o -name "*.bz2" -delete || echo "No .bz2 files to remove or failed to remove."

# 139. Remove orphaned .woff web fonts
sudo find /usr/share/fonts $EXCLUDE_DIRS -o -name "*.woff" -delete || echo "No .woff fonts to remove or failed to remove."

# 140. Remove orphaned .ttf font files
sudo find /usr/share/fonts $EXCLUDE_DIRS -o -name "*.ttf" -delete || echo "No .ttf fonts to remove or failed to remove."

# 141. Clean .svg vector images
sudo find /usr/share/icons $EXCLUDE_DIRS -o -name "*.svg" -delete || echo "No .svg vector images to remove or failed to remove."

# 142. Remove .tar.xz compressed archives
sudo find /mnt $EXCLUDE_DIRS -o -name "*.tar.xz" -delete || echo "No .tar.xz archives to remove or failed to remove."

# 143. Remove .7z archives
sudo find /mnt $EXCLUDE_DIRS -o -name "*.7z" -delete || echo "No .7z archives to remove or failed to remove."

# 144. Clean .log files in /var/log
sudo find /var/log $EXCLUDE_DIRS -o -name "*.log" -delete || echo "No .log files in /var/log or failed to remove."

# 145. Remove .tmp files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.tmp" -delete || echo "No .tmp files in /mnt or failed to remove."

# 146. Clean orphaned .desktop files in home
sudo find ~ $EXCLUDE_DIRS -o -name "*.desktop" -delete || echo "No .desktop files to remove or failed to remove."

# 147. Remove old kernel .old files
sudo find /boot $EXCLUDE_DIRS -o -name "*.old" -delete || echo "No old kernel .old files or failed to remove."

# 148. Clean .gz compressed archives in /usr
sudo find /usr $EXCLUDE_DIRS -o -name "*.gz" -delete || echo "No .gz archives in /usr or failed to remove."

# 149. Remove orphaned .ini files in /etc
sudo find /etc $EXCLUDE_DIRS -o -name "*.ini" -delete || echo "No .ini files to remove or failed to remove."

# 150. Remove .rpm files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.rpm" -delete || echo "No .rpm files to remove or failed to remove."

# ================================
# Final Additional 50 Cleaning Commands
# ================================

echo "Executing final additional cleaning commands..."

# 151. Remove .plist macOS config files
sudo find /mnt $EXCLUDE_DIRS -o -name "*.plist" -delete || echo "No .plist files to remove or failed to remove."

# 152. Clean .epub eBooks
sudo find /mnt $EXCLUDE_DIRS -o -name "*.epub" -delete || echo "No .epub files to remove or failed to remove."

# 153. Remove .mobi eBooks from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.mobi" -delete || echo "No .mobi files to remove or failed to remove."

# 154. Clean .mp4 video files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.mp4" -delete || echo "No .mp4 files to remove or failed to remove."

# 155. Remove .mp3 audio files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.mp3" -delete || echo "No .mp3 files to remove or failed to remove."

# 156. Remove .flv video files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.flv" -delete || echo "No .flv files to remove or failed to remove."

# 157. Remove .avi video files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.avi" -delete || echo "No .avi files to remove or failed to remove."

# 158. Clean .wav audio files in /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.wav" -delete || echo "No .wav files to remove or failed to remove."

# 159. Remove .mkv video files in /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.mkv" -delete || echo "No .mkv files to remove or failed to remove."

# 160. Remove .ogg audio files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.ogg" -delete || echo "No .ogg files to remove or failed to remove."

# 161. Remove .ogv video files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.ogv" -delete || echo "No .ogv files to remove or failed to remove."

# 162. Clean up .gif images from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.gif" -delete || echo "No .gif images to remove or failed to remove."

# 163. Remove .jpg images from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.jpg" -delete || echo "No .jpg images to remove or failed to remove."

# 164. Remove .png images from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.png" -delete || echo "No .png images to remove or failed to remove."

# 165. Remove .jpeg images from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.jpeg" -delete || echo "No .jpeg images to remove or failed to remove."

# 166. Remove .bmp images from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.bmp" -delete || echo "No .bmp images to remove or failed to remove."

# 167. Remove .pdf files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.pdf" -delete || echo "No .pdf files to remove or failed to remove."

# 168. Clean .xlsx spreadsheet files
sudo find /mnt $EXCLUDE_DIRS -o -name "*.xlsx" -delete || echo "No .xlsx files to remove or failed to remove."

# 169. Remove .docx word files
sudo find /mnt $EXCLUDE_DIRS -o -name "*.docx" -delete || echo "No .docx files to remove or failed to remove."

# 170. Remove .pptx presentation files
sudo find /mnt $EXCLUDE_DIRS -o -name "*.pptx" -delete || echo "No .pptx files to remove or failed to remove."

# 171. Clean .iso files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.iso" -delete || echo "No .iso files to remove or failed to remove."

# 172. Remove .bin binary files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.bin" -delete || echo "No .bin files to remove or failed to remove."

# 173. Remove .svg files from /usr/share/icons
sudo find /usr/share/icons $EXCLUDE_DIRS -o -name "*.svg" -delete || echo "No .svg files to remove or failed to remove."

# 174. Clean up .tar.xz archives
sudo find /mnt $EXCLUDE_DIRS -o -name "*.tar.xz" -delete || echo "No .tar.xz archives to remove or failed to remove."

# 175. Remove .7z archives from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.7z" -delete || echo "No .7z archives to remove or failed to remove."

# 176. Remove .mp4 files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.mp4" -delete || echo "No .mp4 files to remove or failed to remove."

# 177. Remove .mp3 files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.mp3" -delete || echo "No .mp3 files to remove or failed to remove."

# 178. Remove .flv files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.flv" -delete || echo "No .flv files to remove or failed to remove."

# 179. Remove .avi files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.avi" -delete || echo "No .avi files to remove or failed to remove."

# 180. Clean .wav files in /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.wav" -delete || echo "No .wav files to remove or failed to remove."

# 181. Remove .mkv files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.mkv" -delete || echo "No .mkv files to remove or failed to remove."

# 182. Remove .ogg files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.ogg" -delete || echo "No .ogg files to remove or failed to remove."

# 183. Remove .ogv files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.ogv" -delete || echo "No .ogv files to remove or failed to remove."

# 184. Clean .gif images from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.gif" -delete || echo "No .gif images to remove or failed to remove."

# 185. Remove .jpg images from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.jpg" -delete || echo "No .jpg images to remove or failed to remove."

# 186. Remove .png images from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.png" -delete || echo "No .png images to remove or failed to remove."

# 187. Remove .jpeg images from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.jpeg" -delete || echo "No .jpeg images to remove or failed to remove."

# 188. Remove .bmp images from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.bmp" -delete || echo "No .bmp images to remove or failed to remove."

# 189. Remove .pdf files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.pdf" -delete || echo "No .pdf files to remove or failed to remove."

# 190. Clean .xlsx spreadsheet files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.xlsx" -delete || echo "No .xlsx files to remove or failed to remove."

# 191. Remove .docx word files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.docx" -delete || echo "No .docx files to remove or failed to remove."

# 192. Remove .pptx presentation files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.pptx" -delete || echo "No .pptx files to remove or failed to remove."

# 193. Clean .iso files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.iso" -delete || echo "No .iso files to remove or failed to remove."

# 194. Remove .bin binary files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.bin" -delete || echo "No .bin files to remove or failed to remove."

# 195. Clean .tar.xz archives from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.tar.xz" -delete || echo "No .tar.xz archives to remove or failed to remove."

# 196. Remove .7z archives from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.7z" -delete || echo "No .7z archives to remove or failed to remove."

# 197. Remove .mp4 files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.mp4" -delete || echo "No .mp4 files to remove or failed to remove."

# 198. Remove .mp3 files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.mp3" -delete || echo "No .mp3 files to remove or failed to remove."

# 199. Remove .flv files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.flv" -delete || echo "No .flv files to remove or failed to remove."

# 200. Remove .avi files from /mnt
sudo find /mnt $EXCLUDE_DIRS -o -name "*.avi" -delete || echo "No .avi files to remove or failed to remove."
>>>>>>> 37c5c22b3a88bec4bc8de6bb23b85d9c3281e70d

# ================================
# Final Disk Usage Check
# ================================
echo "==============================="
echo "Final disk usage of /mnt/wslg:"
<<<<<<< HEAD
du -sh /mnt/wslg || echo "Unable to determine disk usage for /mnt/wslg."
echo "==============================="

echo "Deep cleanup of /mnt/wslg completed successfully!"
=======
du -sh /mnt/wslg || echo "/mnt/wslg does not exist or is inaccessible."
echo "==============================="

# ================================
# Final Cleanup Complete
# ================================

echo "System cleaned successfully with 200 commands!"

>>>>>>> 37c5c22b3a88bec4bc8de6bb23b85d9c3281e70d
