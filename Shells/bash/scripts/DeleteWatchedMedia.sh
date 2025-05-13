#!/usr/bin/env python3
import os
import sys
import requests
from plexapi.server import PlexServer
from datetime import datetime

# Plex server details
PLEX_URL = 'http://localhost:32400'  # Adjust if needed
PLEX_TOKEN = '5x4gmbyF9L27UaAswD6z'  # You'll need to fill this in

def get_plex_token():
    """Get Plex token from the default location in the container"""
    token_file = '/config/Plex Media Server/Preferences.xml'
    try:
        with open(token_file, 'r') as f:
            content = f.read()
            import re
            match = re.search('PlexOnlineToken="([^"]+)"', content)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error reading Plex token: {e}")
    return None

def connect_to_plex():
    """Establish connection to Plex server"""
    token = PLEX_TOKEN or get_plex_token()
    if not token:
        print("Error: Could not find Plex token. Please set PLEX_TOKEN manually.")
        sys.exit(1)

    try:
        return PlexServer(PLEX_URL, token)
    except Exception as e:
        print(f"Error connecting to Plex: {e}")
        sys.exit(1)

def log_deletion(file_path):
    """Log deleted files with timestamp"""
    with open('deleted_media.log', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - Deleted: {file_path}\n")

def delete_media_file(file_path):
    """Safely delete media file and associated files"""
    try:
        # Delete main media file
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
            log_deletion(file_path)

        # Delete associated subtitle files
        base_path = os.path.splitext(file_path)[0]
        for ext in ['.srt', '.sub', '.idx', '.smi', '.ssa', '.ass']:
            sub_file = base_path + ext
            if os.path.exists(sub_file):
                os.remove(sub_file)
                print(f"Deleted subtitle: {sub_file}")
                log_deletion(sub_file)

        # Delete empty parent directory if it exists
        parent_dir = os.path.dirname(file_path)
        if os.path.exists(parent_dir) and not os.listdir(parent_dir):
            os.rmdir(parent_dir)
            print(f"Deleted empty directory: {parent_dir}")
            log_deletion(parent_dir)

    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

def cleanup_watched_media():
    """Main function to clean up watched media"""
    plex = connect_to_plex()
    deleted_count = 0
    total_space_freed = 0

    # Process each library section
    for section in plex.library.sections():
        if section.type in ['movie', 'show']:
            print(f"\nProcessing {section.title}...")

            if section.type == 'movie':
                # Handle movies
                for movie in section.search(unwatched=False):
                    if movie.viewCount > 0:
                        for media_part in movie.media[0].parts:
                            file_size = os.path.getsize(media_part.file)
                            delete_media_file(media_part.file)
                            total_space_freed += file_size
                            deleted_count += 1

            elif section.type == 'show':
                # Handle TV shows
                for episode in section.searchEpisodes(unwatched=False):
                    if episode.viewCount > 0:
                        for media_part in episode.media[0].parts:
                            file_size = os.path.getsize(media_part.file)
                            delete_media_file(media_part.file)
                            total_space_freed += file_size
                            deleted_count += 1

    # Print summary
    print("\nCleanup Summary:")
    print(f"Total files deleted: {deleted_count}")
    print(f"Total space freed: {total_space_freed / (1024*1024*1024):.2f} GB")

if __name__ == "__main__":
    print("Starting Plex media cleanup...")
    cleanup_watched_media()
    print("Cleanup completed!")
