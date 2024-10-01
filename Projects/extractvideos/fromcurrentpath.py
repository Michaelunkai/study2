import os
import shutil

# Define the video file extensions you want to look for
video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv']

# Function to extract video files
def extract_videos_to_current_path():
    current_path = os.getcwd()

    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(current_path):
        for file in files:
            # Check if the file is a video file
            if any(file.lower().endswith(ext) for ext in video_extensions):
                file_path = os.path.join(root, file)
                # Copy the file to the current directory
                shutil.copy(file_path, current_path)
                print(f"Copied {file} to {current_path}")

if __name__ == "__main__":
    extract_videos_to_current_path()
