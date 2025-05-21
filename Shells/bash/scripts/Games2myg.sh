for d in /mnt/f/games/*/; do fn=$(basename "$d"); [[ "$fn" == "eldenrings" ]] && continue; cd "$d" && echo '# Use a base image
FROM alpine:latest

# Install rsync
RUN apk --no-cache add rsync

# Set the working directory
WORKDIR /app

# Copy everything within the current path to /home/
COPY . /home/

# Default runtime options
CMD ["rsync", "-aP", "/home/", "/home/"]' > Dockerfile && docker build -t michadockermisha/backup:"$fn" . && docker push michadockermisha/backup:"$fn" && cd ..; done
