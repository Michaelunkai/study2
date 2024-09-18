#!/bin/bash

# Define the base repository name
base_repo="michadockermisha/backup"

# Get a list of images with the base repository name
image_list=$(docker images --format '{{.Repository}}:{{.Tag}}' | grep "^$base_repo" | grep -E ':<.*>$')

# Iterate through the images
for image in $image_list; do
  # Extract container name from image name
  container_name=$(echo $image | cut -d/ -f3 | cut -d: -f2 | tr -d '>')

  # Define the target repository name
  target_repo="$base_repo:$container_name"

  # Tag the image with the target repository name
  docker tag $image $target_repo

  # Push the image to the target repository
  docker push $target_repo

  # Optionally, remove the local image if needed
  # docker rmi $image
done
