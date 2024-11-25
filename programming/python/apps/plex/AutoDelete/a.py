#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from plexapi.server import PlexServer

# Plex server details
PLEX_URL = 'http://localhost:32400'
PLEX_TOKEN = '5x4gmbyF9L27UaAswD6z'

# Directories containing media files
MEDIA_DIRECTORIES = ['/home/anime', '/home/movies', '/home/TV']

# Initialize Plex server connection
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# Iterate through each library section
for section in plex.library.sections():
    # Process only movie, show, and anime sections
    if section.type in ['movie', 'show']:
        # Iterate through all items in the section
        for item in section.all():
            # Handle movies and shows
            try:
                # Check if the item has been watched
                if item.isWatched:
                    # Retrieve and delete the file paths of the media item
                    for media in item.media:
                        for part in media.parts:
                            file_path = part.file
                            if any(file_path.startswith(dir) for dir in MEDIA_DIRECTORIES):
                                os.remove(file_path)
                                print(f"Deleted: {file_path}")

                # Check if the item has episodes and if any are watched
                if section.type == 'show':
                    for episode in item.episodes():
                        if episode.isWatched:
                            for media in episode.media:
                                for part in media.parts:
                                    file_path = part.file
                                    if any(file_path.startswith(dir) for dir in MEDIA_DIRECTORIES):
                                        os.remove(file_path)
                                        print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error processing {item.title}: {e}")
