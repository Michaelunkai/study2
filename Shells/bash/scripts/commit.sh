#!/bin/bash

# Iterate over all containers (both running and stopped)
docker ps -a --format '{{.Names}}' | while read -r container_name; do
  # Replace invalid characters in container name to create a valid tag
  tag=$(echo "$container_name" | tr -cd '[:alnum:]' | tr '[:upper:]' '[:lower:]')

  # Commit the container with the generated tag
  echo "Committing container: $container_name"
  docker commit "$container_name" "michadockermisha/backup:$tag"
  echo "Committed container: $container_name"
done
