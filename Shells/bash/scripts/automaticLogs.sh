#!/bin/ 

# Get the latest created file in /home/micha/study
latestFile=$(find /home/micha/study -type f -printf "%T@ %p\n" | sort -n | tail -1 | awk '{print $2}')
latestFileName=$(basename "$latestFile")

# Prepare the inputs for the Python script
inputs=(
    "$latestFileName"    # Input for "Enter the subject:"
    "30"                 # Default duration in minutes
    "No additional notes" # Default notes (optional)
)

# Combine the inputs into a single string with newlines
inputString=$(printf "%s\n" "${inputs[@]}")

# Start the Python process with redirected input/output
output=$(echo -e "$inputString" | python3 /home/micha/study/programming/python/apps/study_tracker/terminal/c.py 2>&1)

# Check if there's an EOFError and handle it by retrying with defaults
if echo "$output" | grep -q "EOF when reading a line"; then
    echo "Error: EOF encountered during input. Retrying with safe default inputs..."
    
    # Retry with safe default inputs for all prompts
    defaultInputs=(
        "$latestFileName"    # Default subject
        "30"                 # Default duration in minutes
        "No additional notes" # Default notes (optional)
    )
    
    defaultInputString=$(printf "%s\n" "${defaultInputs[@]}")
    
    # Retry the Python process with default inputs
    output=$(echo -e "$defaultInputString" | python3 /home/micha/study/programming/python/apps/study_tracker/terminal/c.py 2>&1)
fi

# Display the output
echo "$output"
