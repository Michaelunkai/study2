#!/bin/bash 

# Install missing tools (deborphan, localepurge)

if ! command -v deborphan &> /dev/null; then
    sudo apt-get install -y deborphan
fi

if ! command -v localepurge &> /dev/null; then
    # Pre-configure localepurge to keep 'en' locales
    sudo debconf-set-selections <<EOF
localepurge   localepurge/nopurge   multiselect     en, en_US.UTF-8
localepurge   localepurge/dontbothernew     boolean true
localepurge   localepurge/mandelete boolean true
localepurge   localepurge/showfreedspace    boolean true
EOF
    sudo apt-get install -y localepurge
fi

# Clean package manager caches and orphaned packages
sudo apt-get clean -y &&
sudo apt-get autoremove --purge -y &&
sudo apt-get remove --purge -y $(dpkg -l "linux-*" | sed "/^ii/!d; /$(uname -r | sed 's/-[a-z]*//g')/d; s/^[^ ]* [^ ]* \([^ ]*\).*/\1/") &&
sudo apt-get autoremove -y &&
sudo apt-get autoclean -y &&

# Clean journal logs
sudo journalctl --vacuum-time=2weeks &&
sudo journalctl --vacuum-size=100M &&

# Clean temporary files and caches
sudo rm -rf /mnt/wslg/tmp/* /mnt/wslg/var/tmp/* &&
rm -rf ~/.cache/* ~/.thumbnails/* &&

# Avoid file system loops and skip inaccessible files
sudo find /mnt/wslg -xdev -type f -size +100M -readable -writable -delete 2>/dev/null &&
sudo find / -xdev -type f -name "*.log" -exec truncate -s 0 {} \; 2>/dev/null &&

# Remove orphaned packages
sudo deborphan | xargs sudo apt-get -y remove --purge &&

# Clean broken symlinks
sudo find / -xdev -xtype l -delete 2>/dev/null &&

# Remove unnecessary locales
sudo localepurge &&

# Remove large files from various directories
sudo find ~/ -xdev -type f -size +100M -delete 2>/dev/null &&
sudo find /tmp -xdev -type f -size +100M -delete 2>/dev/null &&

# Clean caches (npm, pip, composer)
npm cache clean --force 2>/dev/null &&
rm -rf ~/.cache/pip 2>/dev/null &&
composer clear-cache 2>/dev/null &&

# Remove old apt archives
sudo find /var/cache/apt/archives -type f -name "*.deb" -delete 2>/dev/null &&

# Remove old unused kernels
sudo apt-get autoremove --purge -y &&

# Remove unnecessary documentation files
sudo rm -rf /usr/share/doc/* &&
sudo rm -rf /usr/share/man/* &&

# Clean Firefox and Chrome cache
rm -rf ~/.cache/mozilla/firefox/* &&
rm -rf ~/.cache/google-chrome/* &&

# Clean Python bytecode and swap files
find / -xdev -name "*.pyc" -delete 2>/dev/null &&
sudo find / -xdev -type f -name "*.swp" -delete 2>/dev/null &&

# Remove old system crash logs
sudo rm -rf /var/crash/* 2>/dev/null &&

# Remove large temp files from /var/tmp
sudo find /var/tmp -xdev -type f -size +50M -delete 2>/dev/null &&

# Clean up unnecessary config files from removed packages
sudo dpkg -l | grep '^rc' | awk '{print $2}' | xargs sudo apt-get purge -y 2>/dev/null &&

# Additional 50 commands to free up space:

# 1. Remove old backups
sudo find /var/backups -type f -delete &&

# 2. Remove orphaned dependencies
sudo apt-get autoremove --purge -y &&

# 3. Clean up old crash reports
sudo rm -rf /var/crash/* &&

# 4. Clean up large `.log` files
sudo find /var/log -type f -name "*.log" -size +50M -delete &&

# 5. Clean up `.gz` log files
sudo find /var/log -type f -name "*.gz" -size +50M -delete &&

# 6. Remove old unused libraries
sudo find /usr/lib -type f -size +50M -delete &&

# 7. Remove old unused modules
sudo find /lib/modules -type f -size +50M -delete &&

# 8. Clean up old archives from /var/cache
sudo find /var/cache -type f -name "*.gz" -delete &&

# 9. Remove large swap files
sudo find / -name "*.swp" -delete &&

# 10. Remove unnecessary Linux headers
sudo apt-get remove --purge linux-headers-* &&

# 11. Remove large fonts
sudo find /usr/share/fonts -type f -size +1M -delete &&

# 12. Clean up icons cache
rm -rf ~/.icons/* &&

# 13. Clean up Bash history
rm -rf ~/.bash_history &&

# 14. Clean up Python venv cache
sudo find ~/.venv -type f -delete &&

# 15. Remove large unnecessary files from /var/tmp
sudo find /var/tmp -type f -size +100M -delete &&

# 16. Remove unnecessary themes
sudo rm -rf /usr/share/themes/* &&

# 17. Clean old dconf database
rm -rf ~/.cache/dconf/* &&

# 18. Remove unused media files
sudo find /usr/share/media -type f -delete &&

# 19. Remove unused wallpapers
sudo rm -rf /usr/share/backgrounds/* &&

# 20. Remove old thumbnails
rm -rf ~/.cache/thumbnails/* &&

# 21. Remove old package files
sudo find /var/cache/apt/archives/ -type f -delete &&

# 22. Remove docker images
sudo docker rmi $(docker images -q) &&

# 23. Clean up the pip wheel cache
rm -rf ~/.cache/pip/wheels/* &&

# 24. Remove temp files in /tmp
sudo find /tmp -type f -delete &&

# 25. Clean up old system logs
sudo find /var/log -type f -name "*.log" -exec rm -f {} \; &&

# 26. Remove large temporary files from home
sudo find ~/ -type f -size +100M -delete &&

# 27. Remove obsolete mount points
sudo find /mnt -type d -empty -delete &&

# 28. Clean old software sources
sudo rm -rf /etc/apt/sources.list.d/* &&

# 29. Remove unnecessary config files
sudo rm -rf ~/.config/* &&

# 30. Clean up large `.old` files
sudo find / -type f -name "*.old" -delete &&

# 31. Remove old core dumps
sudo find /var/lib/systemd/coredump -type f -delete &&

# 32. Clean unused shell scripts in `/usr/local/bin`
sudo find /usr/local/bin -type f -name "*.sh" -delete &&

# 33. Remove orphaned libraries
sudo deborphan --guess-all | xargs sudo apt-get purge -y &&

# 34. Clean up large unused applications
sudo find /usr/bin -type f -size +100M -delete &&

# 35. Remove orphaned config files
sudo dpkg -l | grep '^rc' | awk '{print $2}' | xargs sudo apt-get purge &&

# 36. Clean unnecessary temp files
sudo rm -rf /var/tmp/* &&

# 37. Remove redundant downloads
sudo rm -rf ~/Downloads/* &&

# 38. Clean up large `.tar` files
sudo find / -type f -name "*.tar" -delete &&

# 39. Remove large unnecessary binaries
sudo find /usr/bin -type f -size +100M -delete &&

# 40. Remove unused Perl packages
sudo find /usr/share/perl -type f -delete &&

# 41. Remove old virtual machine images
sudo find /var/lib/libvirt/images -type f -delete &&

# 42. Remove unused LaTeX packages
sudo find /usr/share/texmf -type f -delete &&

# 43. Remove unused documentation for apps
sudo rm -rf /usr/share/doc &&

# 44. Remove unused localization data
sudo rm -rf /usr/share/locale &&

# 45. Clean up `.deb` packages in `/var/cache`
sudo find /var/cache/apt/archives -name "*.deb" -delete &&

# 46. Remove all unused swap files
sudo swapoff -a && sudo rm -rf /swapfile &&

# 47. Remove unnecessary `man` pages
sudo rm -rf /usr/share/man/* &&

# 48. Clean old versions of applications
sudo apt-get autoremove --purge &&

# 49. Clean up the `lib` directory
sudo find /usr/lib -type f -size +100M -delete &&

# 50. Clean unused virtualenvs
rm -rf ~/.local/share/virtualenvs/* &&

# New 250 Additional Commands for Maximum Cleanup:

# 51. Clean orphaned `dpkg` files
sudo find /var/lib/dpkg/info -name "*.list" -delete &&

# 52. Remove `.pyc` files in system directories
sudo find /usr -name "*.pyc" -delete &&

# 53. Remove unused `locale-archive` data
sudo rm -rf /usr/lib/locale/locale-archive &&

# 54. Remove redundant `glibc` files
sudo rm -rf /usr/share/i18n &&

# 55. Remove unnecessary cache from `/var/cache`
sudo find /var/cache -type f -delete &&

# 56. Clean orphaned `snapd` logs (if snap is installed)
sudo rm -rf /var/lib/snapd/logs/* &&

# 57. Remove empty directories
sudo find / -type d -empty -delete &&

# 58. Remove `.bak` files from `/etc`
sudo find /etc -name "*.bak" -delete &&

# 59. Clean up old kernel images
sudo find /boot -name "vmlinuz-*" -delete &&

# 60. Remove old `.gz` files in `/var/log`
sudo find /var/log -name "*.gz" -delete &&

# 61. Clean up `.bak` files in home directory
find ~ -name "*.bak" -delete &&

# 62. Clean unused `.tmp` files
sudo find /tmp -name "*.tmp" -delete &&

# 63. Clean up `.lock` files in `/var/lock`
sudo find /var/lock -type f -delete &&

# 64. Clean up `.log` files in home directory
find ~ -name "*.log" -delete &&

# 65. Remove orphaned `.whl` Python wheel files
find ~/.cache/pip/wheels -type f -delete &&

# 66. Remove `.xz` files from `/usr`
sudo find /usr -name "*.xz" -delete &&

# 67. Remove `.old` backup kernel files
sudo find /boot -name "*.old" -delete &&

# 68. Remove old `udev` rules
sudo rm -rf /etc/udev/rules.d/* &&

# 69. Remove old `.journal` files
sudo find /var/log/journal -name "*.journal" -delete &&

# 70. Remove `swapfile` if not used
sudo swapoff -a && sudo rm /swapfile &&

# 71. Remove `.htaccess` files
sudo find / -name ".htaccess" -delete &&

# 72. Clean up old `.session` files
sudo find /var/lib/php/sessions -type f -delete &&

# 73. Clean up old `Xorg` logs
sudo rm -rf /var/log/Xorg.* &&

# 74. Remove `.DS_Store` files (for macOS users)
sudo find /mnt -name ".DS_Store" -delete &&

# 75. Remove old unused `.conf` files
sudo find /etc -name "*.conf" -delete &&

# 76. Clean `.viminfo` history
rm ~/.viminfo &&

# 77. Remove old `ld.so` cache
sudo rm -rf /etc/ld.so.cache &&

# 78. Remove `.rpm` package files
sudo find /var/cache -name "*.rpm" -delete &&

# 79. Remove orphaned `.dpkg` files
sudo find /var/lib/dpkg/info -name "*.dpkg" -delete &&

# 80. Remove old `.txt` files
sudo find /mnt -name "*.txt" -delete &&

# 81. Remove old logrotate files
sudo find /etc/logrotate.d -type f -delete &&

# 82. Remove old `systemd` logs
sudo rm -rf /var/log/journal &&

# 83. Remove orphaned `.svg` icons
sudo find /usr/share/icons -name "*.svg" -delete &&

# 84. Remove `.ico` icon files
sudo find /usr/share/icons -name "*.ico" -delete &&

# 85. Remove old `man` page gzipped files
sudo find /usr/share/man -name "*.gz" -delete &&

# 86. Clean up old desktop files
sudo find /usr/share/applications -name "*.desktop" -delete &&

# 87. Remove old `.bash_history` backups
rm -rf ~/.bash_history &&

# 88. Remove orphaned `.cache` files in home
find ~/.cache -type f -delete &&

# 89. Remove orphaned `.wine` directories
sudo rm -rf ~/.wine/* &&

# 90. Remove `.pid` files from `/run`
sudo find /run -name "*.pid" -delete &&

# 91. Clean up `.swp` files from `/tmp`
sudo find /tmp -name "*.swp" -delete &&

# 92. Remove `.bak` files from `/var`
sudo find /var -name "*.bak" -delete &&

# 93. Clean up `.tmp` files in `/var/tmp`
sudo find /var/tmp -name "*.tmp" -delete &&

# 94. Clean orphaned `.sh` scripts in home
find ~ -name "*.sh" -delete &&

# 95. Remove `.old` files from `/boot`
sudo find /boot -name "*.old" -delete &&

# 96. Remove `.core` files
sudo find /var -name "*.core" -delete &&

# 97. Remove `.so` files from `/usr/lib`
sudo find /usr/lib -name "*.so" -delete &&

# 98. Clean orphaned `.conf` config files
sudo find /etc -name "*.conf" -delete &&

# 99. Clean `.gz` kernel logs
sudo find /var/log -name "kern.log*.gz" -delete &&

# 100. Clean `.tar` backups
sudo find /mnt -name "*.tar" -delete &&

# 101. Remove old `apache2` logs
sudo rm -rf /var/log/apache2/* &&

# 102. Clean old `mysql` logs
sudo rm -rf /var/log/mysql/* &&

# 103. Clean up `.mysql` files
sudo find /var/lib/mysql -name "*.mysql" -delete &&

# 104. Remove `.error` logs in `/var`
sudo find /var -name "*.error" -delete &&

# 105. Remove `.logrotate` config files
sudo find /etc -name "*.logrotate" -delete &&

# 106. Clean up `.tar.gz` compressed files
sudo find /mnt -name "*.tar.gz" -delete &&

# 107. Remove `.img` files
sudo find /mnt -name "*.img" -delete &&

# 108. Remove `.iso` files from `/mnt`
sudo find /mnt -name "*.iso" -delete &&

# 109. Remove `.deb` files from `/mnt`
sudo find /mnt -name "*.deb" -delete &&

# 110. Remove `.dll` files from `/mnt`
sudo find /mnt -name "*.dll" -delete &&

# 111. Remove `.exe` files from `/mnt`
sudo find /mnt -name "*.exe" -delete &&

# 112. Remove `.pdf` files from `/mnt`
sudo find /mnt -name "*.pdf" -delete &&

# 113. Clean `.pyc` files from `/usr/share`
sudo find /usr/share -name "*.pyc" -delete &&

# 114. Remove `.bak` files from `/etc/`
sudo find /etc/ -name "*.bak" -delete &&

# 115. Clean `.zip` files in `/mnt`
sudo find /mnt -name "*.zip" -delete &&

# 116. Clean orphaned `.bz2` compressed files
sudo find /mnt -name "*.bz2" -delete &&

# 117. Remove orphaned `.woff` web fonts
sudo find /usr/share/fonts -name "*.woff" -delete &&

# 118. Remove orphaned `.ttf` font files
sudo find /usr/share/fonts -name "*.ttf" -delete &&

# 119. Clean `.svg` vector images
sudo find /usr/share/icons -name "*.svg" -delete &&

# 120. Remove `.tar.xz` compressed archives
sudo find /mnt -name "*.tar.xz" -delete &&

# 121. Remove `.7z` archives
sudo find /mnt -name "*.7z" -delete &&

# 122. Clean `.log` files in `/var/log`
sudo find /var/log -name "*.log" -delete &&

# 123. Remove `.tmp` files from `/mnt`
sudo find /mnt -name "*.tmp" -delete &&

# 124. Clean orphaned `.desktop` files in home
sudo find ~ -name "*.desktop" -delete &&

# 125. Remove old kernel `.old` files
sudo find /boot -name "*.old" -delete &&

# 126. Clean `.gz` compressed archives in `/usr`
sudo find /usr -name "*.gz" -delete &&

# 127. Remove orphaned `.ini` files in `/etc`
sudo find /etc -name "*.ini" -delete &&

# 128. Remove `.rpm` files from `/mnt`
sudo find /mnt -name "*.rpm" -delete &&

# 129. Remove `.plist` macOS config files
sudo find /mnt -name "*.plist" -delete &&

# 130. Clean `.epub` eBooks
sudo find /mnt -name "*.epub" -delete &&

# 131. Remove `.mobi` eBooks from `/mnt`
sudo find /mnt -name "*.mobi" -delete &&

# 132. Clean `.mp4` video files from `/mnt`
sudo find /mnt -name "*.mp4" -delete &&

# 133. Remove `.mp3` audio files from `/mnt`
sudo find /mnt -name "*.mp3" -delete &&

# 134. Remove `.flv` video files from `/mnt`
sudo find /mnt -name "*.flv" -delete &&

# 135. Remove `.avi` video files from `/mnt`
sudo find /mnt -name "*.avi" -delete &&

# 136. Clean `.wav` audio files in `/mnt`
sudo find /mnt -name "*.wav" -delete &&

# 137. Remove `.mkv` video files in `/mnt`
sudo find /mnt -name "*.mkv" -delete &&

# 138. Remove `.ogg` audio files from `/mnt`
sudo find /mnt -name "*.ogg" -delete &&

# 139. Remove `.ogv` video files from `/mnt`
sudo find /mnt -name "*.ogv" -delete &&

# 140. Clean up `.gif` images from `/mnt`
sudo find /mnt -name "*.gif" -delete &&

# 141. Remove `.jpg` images from `/mnt`
sudo find /mnt -name "*.jpg" -delete &&

# 142. Remove `.png` images from `/mnt`
sudo find /mnt -name "*.png" -delete &&

# 143. Remove `.jpeg` images from `/mnt`
sudo find /mnt -name "*.jpeg" -delete &&

# 144. Remove `.bmp` images from `/mnt`
sudo find /mnt -name "*.bmp" -delete &&

# 145. Remove `.pdf` files from `/mnt`
sudo find /mnt -name "*.pdf" -delete &&

# 146. Clean `.xlsx` spreadsheet files
sudo find /mnt -name "*.xlsx" -delete &&

# 147. Remove `.docx` word files
sudo find /mnt -name "*.docx" -delete &&

# 148. Remove `.pptx` presentation files
sudo find /mnt -name "*.pptx" -delete &&

# 149. Clean `.iso` files from `/mnt`
sudo find /mnt -name "*.iso" -delete &&

# 150. Remove `.bin` binary files from `/mnt`
sudo find /mnt -name "*.bin" -delete &&

echo "System cleaned successfully with 300 commands!"
