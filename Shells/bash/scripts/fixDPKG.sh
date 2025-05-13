#!/bin/bash
#
# fix-package-dependencies.sh
# 
# This script specifically fixes the dependency chain:
# libpaper1 -> libgs9 -> ghostscript -> gimp

# Ensure script is run as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 
   exit 1
fi

# Function to print section headers
print_header() {
    echo -e "\n=== $1 ===\n"
}

print_header "Starting dependency fix"

# Stop any running package managers
killall apt apt-get dpkg 2>/dev/null || true
sleep 2

# Remove locks
print_header "Removing package locks"
rm -f /var/lib/dpkg/lock*
rm -f /var/lib/apt/lists/lock
rm -f /var/cache/apt/archives/lock

# Remove the problematic packages completely
print_header "Removing problematic packages"
apt-get purge -y libpaper1 libgs9 libpaper-utils ghostscript gimp
dpkg --remove --force-remove-reinstreq libpaper1 libgs9 libpaper-utils ghostscript gimp

# Clean up package database
print_header "Cleaning package database"
rm -rf /var/lib/dpkg/info/libpaper1*
rm -rf /var/lib/dpkg/info/libgs9*
rm -rf /var/lib/dpkg/info/libpaper-utils*
rm -rf /var/lib/dpkg/info/ghostscript*
rm -rf /var/lib/dpkg/info/gimp*

# Update package lists
print_header "Updating package lists"
apt-get clean
rm -rf /var/lib/apt/lists/*
apt-get update

# Fix package system
print_header "Fixing package system"
dpkg --configure -a
apt-get install -f -y

# Install packages in correct order
print_header "Installing packages in dependency order"

# First, install libpaper1 alone
apt-get install -y --no-install-recommends libpaper1
dpkg --configure -a
apt-get install -f -y

# Then install libgs9
apt-get install -y --no-install-recommends libgs9
dpkg --configure -a
apt-get install -f -y

# Install libpaper-utils
apt-get install -y --no-install-recommends libpaper-utils
dpkg --configure -a
apt-get install -f -y

# Install ghostscript
apt-get install -y --no-install-recommends ghostscript
dpkg --configure -a
apt-get install -f -y

# Finally install GIMP
apt-get install -y gimp
dpkg --configure -a
apt-get install -f -y

# Verify installations
print_header "Verifying package states"
dpkg -l | grep -E "libpaper1|libgs9|libpaper-utils|ghostscript|gimp"

print_header "Script completed"
echo "If you still see errors, please check:"
echo "1. /var/log/dpkg.log"
echo "2. /var/log/apt/term.log"
echo "3. Try running 'apt-get install -f' again"
