#!/bin/bash

# -----------------------------------
# Script: create_tool_dir.sh
# Description:
#   - Creates a directory named after the latest tool used in the last tool-related install command.
#   - Places it in the previous directory (from `cd -`).
#   - Navigates to the newly created directory.
#   - Creates a file named "liner to setup and run in ubuntu <tool_name>" containing the install command.
# Usage:
#   source ~/create_tool_dir.sh
#   or
#   . ~/create_tool_dir.sh
# -----------------------------------

# Function to extract the tool name from a command
extract_tool_name() {
    local cmd="$1"

    # Extract the part after 'install' keyword
    local install_part
    install_part=$(echo "$cmd" | sed -n 's/.*install[[:space:]]\+\(.*\)/\1/p')

    if [[ -z "$install_part" ]]; then
        echo ""
        return
    fi

    # Split install_part by spaces, exclude options starting with '-'
    local tools=()
    for word in $install_part; do
        if [[ "$word" != -* ]]; then
            tools+=("$word")
        fi
    done

    # Return the first tool name
    if [[ ${#tools[@]} -ge 1 ]]; then
        echo "${tools[0]}"
    else
        echo ""
    fi
}

# Function to find the last tool-related install command in history
find_last_tool_command() {
    # Define tool-related install command patterns
    local patterns=("apt install" "apt-get install" "yum install" "dnf install" "brew install")

    for pattern in "${patterns[@]}"; do
        # Search history for the pattern
        local cmd=$(history | grep -E "$pattern" | tail -n1 | sed -E 's/^[ ]*[0-9]+\s+//')
        if [[ -n "$cmd" ]]; then
            echo "$cmd"
            return
        fi
    done

    # If no tool install command found, return empty
    echo ""
}

# Function to ensure the script is being sourced
ensure_sourced() {
    # Check if the script is being sourced
    # BASH_SOURCE[0] != $0 means it's being sourced
    if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        echo "Error: This script must be sourced to affect the current shell."
        echo "Usage: source ~/create_tool_dir.sh"
        exit 1
    fi
}

# Ensure the script is being sourced
ensure_sourced

# Step 0: Append current session history to history file
history -a

# Step 1: Find the last tool-related install command
last_tool_command=$(find_last_tool_command)

# Debug: Uncomment the following line to see the last tool install command
# echo "Last tool install command: $last_tool_command"

# Check if a tool command was found
if [[ -z "$last_tool_command" ]]; then
    echo "Error: No tool installation command found in history."
    return 1
fi

# Step 2: Extract the tool name
tool_name=$(extract_tool_name "$last_tool_command")

# Check if tool_name is not empty
if [[ -z "$tool_name" ]]; then
    echo "Error: Could not determine the tool name from the last tool command."
    return 1
fi

# Step 3: Get the previous directory from OLDPWD
previous_dir="$OLDPWD"

# If OLDPWD is not set, attempt to extract it from history
if [[ -z "$previous_dir" ]]; then
    # Find the last 'cd' command in history
    cd_command=$(history | grep -E '^\s*[0-9]+\s+cd\s+' | tail -n 1 | sed -E 's/^[ ]*[0-9]+\s+cd\s+//')
    previous_dir="$cd_command"
fi

# Validate previous_dir
if [[ -z "$previous_dir" ]]; then
    echo "Error: Could not determine the previous directory."
    return 1
fi

if [[ ! -d "$previous_dir" ]]; then
    echo "Error: The previous directory '$previous_dir' does not exist."
    return 1
fi

# Step 4: Create the new directory
new_dir="$previous_dir/$tool_name"

if [[ -d "$new_dir" ]]; then
    echo "Directory '$new_dir' already exists."
else
    mkdir -p "$new_dir"
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to create directory '$new_dir'."
        return 1
    fi
    echo "Created directory: $new_dir"
fi

# Step 5: Change to the new directory
cd "$new_dir" || { echo "Error: Failed to navigate to '$new_dir'."; return 1; }

# Confirmation message
echo "Navigated to: $(pwd)"

# Step 6: Create the setup one-liner file
# Define the filename
file_name="liner to setup and run in ubuntu $tool_name"

# Create the file and add the install command
echo "$last_tool_command" > "$file_name"

# Check if the file was created successfully
if [[ $? -eq 0 ]]; then
    echo "Created file: $file_name"
else
    echo "Error: Failed to create file '$file_name'."
    return 1
fi
