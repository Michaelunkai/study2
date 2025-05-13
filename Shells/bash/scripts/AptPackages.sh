#!/bin/bash

# List of packages to exclude
EXCLUDED_PACKAGES=(
    docker
    tar
    tree
    python3-pip
    python3
    python-is-python3
    containerd.io
    gedit
    gzip
    mount
    sysvinit-utils
    sudo
    libdebconfclient0
    docker-ce
    docker-ce-cli
    docker-buildx-plugin
    docker-compose-plugin
    apt
    nano
    git
    sshpass
    apt-utils
    passwd
    adduser
    build-essential
    rsync
    file
    bash-completion
    curl
)

# Convert the exclusion list into a grep pattern
EXCLUDE_PATTERN=$(printf "|%s" "${EXCLUDED_PACKAGES[@]}")
EXCLUDE_PATTERN=${EXCLUDE_PATTERN:1} # Remove the leading '|'

# Execute the command
apt-mark showmanual \
| grep -Evx "($EXCLUDE_PATTERN)" \
| xargs -r dpkg-query -Wf='${Package} ${Installed-Size} ${Essential}\n' \
| awk '$3 != "yes" {printf "%-40s %.2f MB\n", $1, $2/1024}'
