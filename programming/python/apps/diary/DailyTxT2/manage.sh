#!/bin/bash

# DailyTxT Migration Script
# This script facilitates migration between servers while ensuring data persistence

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root${NC}"
  exit 1
fi

# Default values
BACKUP_DIR="/opt/dailytxt-backups"
INSTALL_DIR="/opt/dailytxt"
ACTION=""

# Create necessary directories
mkdir -p "${BACKUP_DIR}"
mkdir -p "${INSTALL_DIR}"

# Function to display help
show_help() {
  echo -e "${BLUE}DailyTxT Migration Tool${NC}"
  echo -e "Usage: $0 [options] ACTION"
  echo
  echo -e "Actions:"
  echo -e "  install      Install DailyTxT on a new server"
  echo -e "  backup       Create a backup of DailyTxT data"
  echo -e "  restore      Restore data from backup"
  echo -e "  start        Start DailyTxT"
  echo -e "  stop         Stop DailyTxT"
  echo -e "  status       Check DailyTxT status"
  echo
  echo -e "Options:"
  echo -e "  -b DIR       Backup directory (default: /opt/dailytxt-backups)"
  echo -e "  -i DIR       Installation directory (default: /opt/dailytxt)"
  echo -e "  -h           Show this help"
}

# Parse command line arguments
while getopts "b:i:h" opt; do
  case ${opt} in
    b)
      BACKUP_DIR=$OPTARG
      ;;
    i)
      INSTALL_DIR=$OPTARG
      ;;
    h)
      show_help
      exit 0
      ;;
    \?)
      echo -e "${RED}Invalid option: $OPTARG${NC}" 1>&2
      show_help
      exit 1
      ;;
  esac
done

# Shift arguments to get the ACTION
shift $((OPTIND -1))
ACTION=$1

# Function to install Docker and Docker Compose if not present
ensure_docker_installed() {
  echo -e "${BLUE}Checking Docker installation...${NC}"
  
  if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker not found, installing...${NC}"
    apt-get update
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt-get update
    apt-get install -y docker-ce
  else
    echo -e "${GREEN}Docker is already installed.${NC}"
  fi
  
  if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose not found, installing...${NC}"
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
  else
    echo -e "${GREEN}Docker Compose is already installed.${NC}"
  fi
}

# Function to create or update docker-compose.yml
create_docker_compose() {
  local compose_file="${INSTALL_DIR}/docker-compose.yml"
  
  # Generate a secure key once and store it
  local secret_key_file="${INSTALL_DIR}/.secret_key"
  if [ ! -f "${secret_key_file}" ]; then
    openssl rand -base64 32 > "${secret_key_file}"
  fi
  local SECRET_KEY=$(cat "${secret_key_file}")
  
  echo -e "${BLUE}Creating docker-compose.yml...${NC}"
  cat > "${compose_file}" << EOF
version: '3.8'

services:
  dailytxt:
    image: phitux/dailytxt:latest
    container_name: dailytxt
    restart: always
    environment:
      # Internal container port
      - PORT=8765
      # Fixed SECRET_KEY for consistent sessions across restarts
      - SECRET_KEY=${SECRET_KEY}
      # Allow registration of new users
      - ALLOW_REGISTRATION=True
      # Indent JSON log file
      - DATA_INDENT=2
      # JWT token expiration - extended for reliability
      - JWT_EXP_DAYS=90
      # Enable auto-update check
      - ENABLE_UPDATE_CHECK=True
      # Admin user credentials
      - INITIAL_ADMIN_USER=michaelovsky5
      - INITIAL_ADMIN_PASSWORD=Blackablacka3!
      # Additional sync settings
      - SYNC_INTERVAL=60
      - DATA_CONSISTENCY_CHECK=True
    ports:
      # Changed to allow access
      - "8888:8765"
    volumes:
      # Named volume for better persistence and migration
      - dailytxt_data:/app/data
    # Ensure proper shutdown to save data
    stop_grace_period: 30s

volumes:
  dailytxt_data:
    name: dailytxt_data
    # Ensures volume remains when containers are removed
    external: false
EOF
  
  echo -e "${GREEN}docker-compose.yml created at ${compose_file}${NC}"
}

# Function to backup data
backup_data() {
  local timestamp=$(date +"%Y%m%d_%H%M%S")
  local backup_file="${BACKUP_DIR}/dailytxt_backup_${timestamp}.tar.gz"
  
  echo -e "${BLUE}Backing up DailyTxT data...${NC}"
  
  # Stop container if running
  if docker ps | grep -q dailytxt; then
    echo -e "${YELLOW}Stopping DailyTxT to ensure data consistency...${NC}"
    cd "${INSTALL_DIR}" && docker-compose stop
    sleep 5
  fi
  
  # Create backup directory if it doesn't exist
  mkdir -p "${BACKUP_DIR}"
  
  # Find volume directory
  VOLUME_DIR=$(docker volume inspect dailytxt_data | grep Mountpoint | awk '{print $2}' | tr -d '",')
  
  if [ -z "${VOLUME_DIR}" ]; then
    echo -e "${RED}Could not find the volume directory. Is DailyTxT installed?${NC}"
    return 1
  fi
  
  # Backup data
  echo -e "${YELLOW}Creating backup archive...${NC}"
  tar -czf "${backup_file}" -C "${VOLUME_DIR}" .
  
  # Copy docker-compose.yml
  cp "${INSTALL_DIR}/docker-compose.yml" "${BACKUP_DIR}/docker-compose_${timestamp}.yml"
  
  # Copy secret key
  if [ -f "${INSTALL_DIR}/.secret_key" ]; then
    cp "${INSTALL_DIR}/.secret_key" "${BACKUP_DIR}/.secret_key_${timestamp}"
  fi
  
  echo -e "${GREEN}Backup complete: ${backup_file}${NC}"
  
  # Restart container if it was running
  if docker ps -a | grep -q dailytxt; then
    echo -e "${YELLOW}Restarting DailyTxT...${NC}"
    cd "${INSTALL_DIR}" && docker-compose start
  fi
}

# Function to restore data
restore_data() {
  local backup_file=""
  
  # List available backups
  echo -e "${BLUE}Available backups:${NC}"
  ls -1 "${BACKUP_DIR}" | grep "dailytxt_backup_" | cat -n
  
  # Prompt for backup selection
  echo -e "${YELLOW}Enter the number of the backup to restore:${NC}"
  read backup_num
  
  # Get the selected backup file
  backup_file=$(ls -1 "${BACKUP_DIR}" | grep "dailytxt_backup_" | sed -n "${backup_num}p")
  
  if [ -z "${backup_file}" ]; then
    echo -e "${RED}Invalid backup selection${NC}"
    return 1
  fi
  
  backup_file="${BACKUP_DIR}/${backup_file}"
  
  # Stop container if running
  if docker ps | grep -q dailytxt; then
    echo -e "${YELLOW}Stopping DailyTxT...${NC}"
    cd "${INSTALL_DIR}" && docker-compose down
    sleep 5
  fi
  
  # Extract timestamp from backup filename
  local timestamp=$(echo "${backup_file}" | grep -o "[0-9]\{8\}_[0-9]\{6\}")
  
  # Copy corresponding docker-compose.yml if it exists
  if [ -f "${BACKUP_DIR}/docker-compose_${timestamp}.yml" ]; then
    cp "${BACKUP_DIR}/docker-compose_${timestamp}.yml" "${INSTALL_DIR}/docker-compose.yml"
  else
    # Create new docker-compose.yml
    create_docker_compose
  fi
  
  # Copy corresponding secret key if it exists
  if [ -f "${BACKUP_DIR}/.secret_key_${timestamp}" ]; then
    cp "${BACKUP_DIR}/.secret_key_${timestamp}" "${INSTALL_DIR}/.secret_key"
  fi
  
  # Find volume directory
  echo -e "${YELLOW}Creating volume if it doesn't exist...${NC}"
  docker volume create dailytxt_data
  
  VOLUME_DIR=$(docker volume inspect dailytxt_data | grep Mountpoint | awk '{print $2}' | tr -d '",')
  
  if [ -z "${VOLUME_DIR}" ]; then
    echo -e "${RED}Could not find the volume directory${NC}"
    return 1
  fi
  
  # Restore data
  echo -e "${YELLOW}Restoring data from backup...${NC}"
  mkdir -p "${VOLUME_DIR}"
  tar -xzf "${backup_file}" -C "${VOLUME_DIR}"
  
  # Fix permissions
  chmod -R 755 "${VOLUME_DIR}"
  
  echo -e "${GREEN}Data restored successfully${NC}"
  
  # Start container
  cd "${INSTALL_DIR}" && docker-compose up -d
  
  echo -e "${GREEN}DailyTxT has been restored and started${NC}"
}

# Function to install DailyTxT
install_dailytxt() {
  ensure_docker_installed
  
  echo -e "${BLUE}Installing DailyTxT...${NC}"
  
  # Create installation directory
  mkdir -p "${INSTALL_DIR}"
  
  # Create docker-compose.yml
  create_docker_compose
  
  # Start DailyTxT
  cd "${INSTALL_DIR}" && docker-compose up -d
  
  echo -e "${GREEN}DailyTxT installed successfully${NC}"
  echo -e "${GREEN}Access it at http://your-server-ip:8888${NC}"
  
  # Create system service for automatic startup
  cat > /etc/systemd/system/dailytxt.service << EOF
[Unit]
Description=DailyTxT Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=${INSTALL_DIR}
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reload
  systemctl enable dailytxt.service
  
  echo -e "${GREEN}DailyTxT service created and enabled${NC}"
}

# Function to check status
check_status() {
  echo -e "${BLUE}DailyTxT Status:${NC}"
  
  # Check if Docker is running
  if ! systemctl is-active --quiet docker; then
    echo -e "${RED}Docker is not running${NC}"
    return 1
  fi
  
  # Check container status
  if docker ps | grep -q dailytxt; then
    echo -e "${GREEN}DailyTxT is running${NC}"
    docker ps | grep dailytxt
  elif docker ps -a | grep -q dailytxt; then
    echo -e "${YELLOW}DailyTxT is stopped${NC}"
    docker ps -a | grep dailytxt
  else
    echo -e "${RED}DailyTxT is not installed${NC}"
  fi
  
  # Show volume info
  if docker volume ls | grep -q dailytxt_data; then
    echo -e "${BLUE}Volume information:${NC}"
    docker volume inspect dailytxt_data
    
    # Show size of data
    VOLUME_DIR=$(docker volume inspect dailytxt_data | grep Mountpoint | awk '{print $2}' | tr -d '",')
    if [ -n "${VOLUME_DIR}" ]; then
      echo -e "${BLUE}Data size:${NC}"
      du -sh "${VOLUME_DIR}"
    fi
  fi
}

# Main script logic based on ACTION
case "${ACTION}" in
  install)
    install_dailytxt
    ;;
  backup)
    backup_data
    ;;
  restore)
    restore_data
    ;;
  start)
    echo -e "${BLUE}Starting DailyTxT...${NC}"
    cd "${INSTALL_DIR}" && docker-compose up -d
    echo -e "${GREEN}DailyTxT started${NC}"
    ;;
  stop)
    echo -e "${BLUE}Stopping DailyTxT...${NC}"
    cd "${INSTALL_DIR}" && docker-compose down
    echo -e "${GREEN}DailyTxT stopped${NC}"
    ;;
  status)
    check_status
    ;;
  *)
    echo -e "${RED}Invalid action: ${ACTION}${NC}"
    show_help
    exit 1
    ;;
esac

exit 0
