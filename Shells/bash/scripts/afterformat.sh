#!/bin/ 

# Set the path to the directory containing executable files
install_path="/mnt/d/backup/windowsapps/install/afterformat/"

# Change to the specified directory
cd "$install_path" || exit

# Array of executable files
executables=(*.exe)

# Function to install executables
install_executables() {
  for exe in "$@"; do
    ./"$exe" &
  done
  wait
}

# Number of installations to run concurrently
concurrent_installations=4

# Loop through the executables in batches
for ((i = 0; i < ${#executables[@]}; i += concurrent_installations)); do
  batch=("${executables[@]:i:concurrent_installations}")
  install_executables "${batch[@]}"
done
