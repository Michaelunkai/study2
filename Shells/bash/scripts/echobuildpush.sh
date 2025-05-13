#!/bin/bash
# docker_persistent_pause.sh
#
# This script first writes a Dockerfile with predetermined content to the current directory.
# Then it builds and pushes a Docker image using the current folder name as the tag.
#
# You can interactively pause/resume the docker build or push commands:
#   - Press Shift+A (uppercase "A") to pause (SIGSTOP) the running command.
#   - Press Shift+S (uppercase "S") to resume (SIGCONT) it.
#
# A checkpoint file (.docker_checkpoint) is used to record completed steps so that if the terminal
# is closed or the PC is rebooted, re‑running the script will resume from the last finished step.
#
# NOTE: Docker build does not support live process checkpointing across reboots.
#       If a build is interrupted mid‑layer, that layer must be rebuilt.
#       Docker’s cache will ensure that completed layers are not rebuilt.

CHECKPOINT_FILE=".docker_checkpoint"
TAG=$(basename "$PWD")
REPO="michadockermisha/backup"

# Utility functions for checkpoint management.
save_checkpoint() {
    echo "$1" > "$CHECKPOINT_FILE"
}

clear_checkpoint() {
    rm -f "$CHECKPOINT_FILE"
}

# Function: run_with_key_pause_resume
# Runs a command in its own process group while monitoring for keystrokes:
#   Shift+A pauses the process group (SIGSTOP)
#   Shift+S resumes it (SIGCONT)
run_with_key_pause_resume() {
    local cmd="$1"
    old_stty=$(stty -g)
    stty -icanon -echo

    echo "Running command: $cmd"
    echo "Press Shift+A to pause, Shift+S to resume."

    # Start the command in a new session so it gets its own process group.
    setsid bash -c "$cmd" &
    child_pid=$!
    child_pg=$child_pid
    paused=0

    while kill -0 "$child_pid" 2>/dev/null; do
        if read -t 0.1 -n 1 key; then
            if [[ "$key" == "A" ]] && [ $paused -eq 0 ]; then
                echo "Pausing process group $child_pg..."
                kill -STOP -"$child_pg"
                paused=1
            elif [[ "$key" == "S" ]] && [ $paused -eq 1 ]; then
                echo "Resuming process group $child_pg..."
                kill -CONT -"$child_pg"
                paused=0
            fi
        fi
    done

    wait "$child_pid"
    ret=$?
    stty "$old_stty"
    echo "Command finished with exit code $ret."
    return $ret
}

# Function: re-read checkpoint status from file.
get_checkpoint() {
    if [ -f "$CHECKPOINT_FILE" ]; then
        cat "$CHECKPOINT_FILE"
    else
        echo "none"
    fi
}

#############################
# Step 1: Write Dockerfile  #
#############################
STEP=$(get_checkpoint)
if [ "$STEP" != "dockerfile_done" ] && [ "$STEP" != "build_done" ] && [ "$STEP" != "push_done" ]; then
    echo "Writing Dockerfile..."
    cat <<'EOF' > Dockerfile
# Use a base image
FROM alpine:latest

# Install rsync
RUN apk --no-cache add rsync

# Set the working directory
WORKDIR /app

# Copy everything within the current path to /home/
COPY . /home/

# Default runtime options
CMD ["rsync", "-aP", "/home/", "/home/"]
EOF
    if [ $? -ne 0 ]; then
        echo "Failed to write Dockerfile."
        exit 1
    fi
    save_checkpoint "dockerfile_done"
else
    echo "Dockerfile already written. Skipping Dockerfile creation step."
fi

#############################
# Step 2: Docker Build      #
#############################
STEP=$(get_checkpoint)
if [ "$STEP" != "build_done" ] && [ "$STEP" != "push_done" ]; then
    echo "Starting docker build with tag: $TAG..."
    run_with_key_pause_resume "docker build -t $REPO:$TAG ."
    build_ret=$?
    if [ $build_ret -ne 0 ]; then
        echo "Docker build failed with exit code $build_ret"
        exit $build_ret
    fi
    save_checkpoint "build_done"
else
    echo "Docker build already completed. Skipping build step."
fi

#############################
# Step 3: Docker Push       #
#############################
STEP=$(get_checkpoint)
if [ "$STEP" != "push_done" ]; then
    echo "Starting docker push with tag: $TAG..."
    run_with_key_pause_resume "docker push $REPO:$TAG"
    push_ret=$?
    if [ $push_ret -ne 0 ]; then
        echo "Docker push failed with exit code $push_ret"
        exit $push_ret
    fi
    save_checkpoint "push_done"
    clear_checkpoint
else
    echo "Docker push already completed. Skipping push step."
fi

echo "All steps completed."
