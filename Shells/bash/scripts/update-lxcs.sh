#!/usr/bin/env bash

# LXC Updater Script - Automatically Updates All LXC Containers
# Author: tteck (tteckster)
# License: MIT
# Repository: https://github.com/community-scripts/ProxmoxVE/raw/main/LICENSE

function header_info {
  clear
  cat <<"EOF"
   __  __          __      __          __   _  ________
  / / / /___  ____/ /___ _/ /____     / /  | |/ / ____/
 / / / / __ \/ __  / __ `/ __/ _ \   / /   |   / /     
/ /_/ / /_/ / /_/ / /_/ / /_/  __/  / /___/   / /___   
\____/ .___/\__,_/\__,_/\__/\___/  /_____/_/|_\____/   
    /_/                                               

EOF
}
set -eEuo pipefail

YW=$(echo "\033[33m")
BL=$(echo "\033[36m")
RD=$(echo "\033[01;31m")
GN=$(echo "\033[1;92m")
CL=$(echo "\033[m")

header_info
echo "Loading..."

# Automatically confirm update prompt
echo -e "${BL}[Info]${GN} Automatically confirming update prompt.${CL}"
NODE=$(hostname)

EXCLUDE_MENU=()
MSG_MAX_LENGTH=0
while read -r TAG ITEM; do
  OFFSET=2
  ((${#ITEM} + OFFSET > MSG_MAX_LENGTH)) && MSG_MAX_LENGTH=${#ITEM}+OFFSET
  EXCLUDE_MENU+=("$TAG" "$ITEM " "OFF")
done < <(pct list | awk 'NR>1')

excluded_containers=""

function update_container() {
  container=$1
  header_info
  name=$(pct exec "$container" hostname)
  os=$(pct config "$container" | awk '/^ostype/ {print $2}')
  echo -e "${BL}[Info]${GN} Updating ${BL}$container${CL} : ${GN}$name${CL}\n"
  case "$os" in
  alpine) pct exec "$container" -- ash -c "apk update && apk upgrade" ;;
  archlinux) pct exec "$container" -- bash -c "pacman -Syyu --noconfirm" ;;
  fedora | rocky | centos | alma) pct exec "$container" -- bash -c "dnf -y update && dnf -y upgrade" ;;
  ubuntu | debian | devuan) pct exec "$container" -- bash -c "apt-get update && apt-get -yq dist-upgrade" ;;
  opensuse) pct exec "$container" -- bash -c "zypper ref && zypper --non-interactive dup" ;;
  *) echo -e "${RD}[Error] Unknown OS type for container $container.${CL}" ;;
  esac
}

header_info
for container in $(pct list | awk '{if(NR>1) print $1}'); do
  if [[ " ${excluded_containers[@]} " =~ " $container " ]]; then
    echo -e "${BL}[Info]${GN} Skipping ${BL}$container${CL}"
  else
    status=$(pct status "$container")
    if [ "$status" == "status: stopped" ]; then
      echo -e "${BL}[Info]${GN} Starting ${BL}$container${CL}"
      pct start "$container"
      sleep 5
      update_container "$container"
      echo -e "${BL}[Info]${GN} Shutting down ${BL}$container${CL}"
      pct shutdown "$container" &
    elif [ "$status" == "status: running" ]; then
      update_container "$container"
    fi
  fi
done

wait
header_info
echo -e "${GN}All containers have been successfully updated.${CL}\n"
