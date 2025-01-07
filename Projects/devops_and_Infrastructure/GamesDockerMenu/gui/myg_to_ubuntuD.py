import os

# Define the source and target file paths
source_file_path = '/mnt/c/study/programming/python/apps/pyqt5Menus/GamesDockerMenu/gui/6.py'
target_file_path = '/mnt/c/study/programming/python/apps/pyqt5Menus/GamesDockerMenu/gui/UbuntuDesktop.py'

# Read the content from the source file
with open(source_file_path, 'r') as source_file:
    code = source_file.readlines()

# Function to replace Docker paths in the command
def update_docker_command(line):
    if 'docker run' in line:
        return line.replace('/mnt/c/games/', '/srv/samba/shared/')
    return line

# Update the Docker command paths
updated_code = [update_docker_command(line) for line in code]

# Write the updated code to the target file
with open(target_file_path, 'w') as target_file:
    target_file.writelines(updated_code)

print(f"Updated code has been written to {target_file_path}")
