#!/bin/bash

# Path variables
ALIAS_FILE="/mnt/c/Users/micha/Desktop/alias.txt"
ROOT_BASHRC="/root/.bashrc"
BACKUP_PATH="/mnt/c/backup/linux/wsl/alias.txt"
STUDY_PATH="/mnt/c/study/shells/bash/.bashrc"
UBUNTU_BASHRC="/home/ubuntu/.bashrc"

# Append alias file to root's .bashrc
cat "$ALIAS_FILE" >> "$ROOT_BASHRC"

# Reload .bashrc for the current session
source "$ROOT_BASHRC"

# Backup .bashrc to various locations
rsync -aP "$ROOT_BASHRC" "$BACKUP_PATH"
rsync -aP "$ROOT_BASHRC" "$STUDY_PATH"
rsync -aP "$ROOT_BASHRC" ~/.bashrc

# Update Ubuntu user's .bashrc and set ownership
sudo cp "$ROOT_BASHRC" "$UBUNTU_BASHRC"
sudo chown ubuntu:ubuntu "$UBUNTU_BASHRC"

# Source the Ubuntu user's .bashrc as the Ubuntu user
sudo -u ubuntu bash -c "source $UBUNTU_BASHRC"

# Clear the alias file
> "$ALIAS_FILE"
