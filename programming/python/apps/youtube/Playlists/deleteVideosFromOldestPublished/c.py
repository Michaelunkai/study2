# -*- coding: utf-8 -*-
import os
import pickle
import time
import logging
import re
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Define file paths and scopes
CLIENT_SECRETS_FILE = r"C:\backup\windowsapps\Credentials\youtube\dsubs\client_secret_1081565985519-s1s8lj1li4h01uf1qldsksm2s6t6soki.apps.googleusercontent.com.json"
TOKEN_PICKLE_FILE = "token.pickle"  # This file will store your credentials after authentication
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Playlist ID to clean up (replace with your specific playlist)
PLAYLIST_ID = "PLY8Bm7EI5jJXynRQUem7v27jE4Jva9UDW"

# Time delay in seconds to avoid hitting quota too fast
TIME_DELAY = 2

def get_authenticated_service():
    """Authenticate and return the YouTube API client."""
    try:
        credentials = None
        # Load credentials from token file if it exists
        if os.path.exists(TOKEN_PICKLE_FILE):
            with open(TOKEN_PICKLE_FILE, 'rb') as token:
                credentials = pickle.load(token)

        # If no valid credentials, run the OAuth flow
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRETS_FILE,
                    SCOPES
                )
                credentials = flow.run_local_server(port=0)

            # Save the credentials for future use
            with open(TOKEN_PICKLE_FILE, 'wb') as token:
                pickle.dump(credentials, token)

        return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise

def get_comprehensive_playlist_items(youtube, playlist_id):
    """
    Fetch ALL videos in the playlist with comprehensive pagination handling.
    """
    items = []
    next_page_token = None
    total_fetched = 0

    try:
        while True:
            request_params = {
                'part': 'snippet',
                'playlistId': playlist_id,
                'maxResults': 50
            }
            if next_page_token:
                request_params['pageToken'] = next_page_token

            response = youtube.playlistItems().list(**request_params).execute()
            current_items = response.get('items', [])
            items.extend(current_items)
            total_fetched += len(current_items)
            logger.info(f"Fetched {len(current_items)} items. Total fetched: {total_fetched}")
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
            time.sleep(TIME_DELAY)

    except Exception as e:
        logger.error(f"Error fetching playlist items: {e}")
        raise

    return items

def is_video_watched(video_title):
    """
    Comprehensive check to determine if a video is considered watched.
    """
    title_lower = video_title.lower()
    watched_indicators = [
        'watched', 'seen', 'viewed', 
        'completed', 'finished', 'done', 
        'already watched', 'watched already',
        "\u2713",  # Unicode check mark
        '(done)', '[done]', 
        '(completed)', '[completed]',
        '(watched)', '[watched]',
        'resume', 'next', 'continue',
        r'\d+%\s*watched',  
        r'\(.*\d+:\d+.*\)',  
    ]
    for indicator in watched_indicators:
        if re.search(indicator, title_lower):
            return True
    return False

def remove_watched_videos(youtube, playlist_items, limit_remaining):
    """
    Remove watched videos up to the limit specified.
    """
    removed_count = 0
    for item in playlist_items:
        if removed_count >= limit_remaining:
            break

        try:
            video_title = item['snippet']['title']
            if is_video_watched(video_title):
                youtube.playlistItems().delete(id=item['id']).execute()
                logger.info(f"REMOVED: {video_title}")
                removed_count += 1
                time.sleep(TIME_DELAY)
        except googleapiclient.errors.HttpError as e:
            logger.error(f"Error removing video '{video_title}': {e}")
        except Exception as e:
            logger.warning(f"Unexpected error processing video: {e}")

    return removed_count

def main():
    """
    Main function to clean up watched videos from a playlist with a deletion limit.
    """
    try:
        youtube = get_authenticated_service()
        
        # Ask user for the number of videos to delete
        try:
            target = int(input("Enter the number of videos to delete: "))
        except ValueError:
            logger.error("Invalid input. Please enter an integer value.")
            return
        
        total_removed = 0
        iteration = 1
        
        while total_removed < target:
            logger.info(f"\n--- Playlist Cleanup Iteration {iteration} ---")
            playlist_items = get_comprehensive_playlist_items(youtube, PLAYLIST_ID)
            if not playlist_items:
                logger.info("Playlist is empty. No videos to remove.")
                break

            remaining = target - total_removed
            removed_this_iteration = remove_watched_videos(youtube, playlist_items, remaining)
            total_removed += removed_this_iteration

            logger.info(f"Removed {removed_this_iteration} watched video(s) in this iteration.")
            logger.info(f"Total videos removed so far: {total_removed}")

            if removed_this_iteration == 0:
                logger.info("No more watched videos found. Cleanup complete.")
                break

            iteration += 1
            time.sleep(TIME_DELAY)
        
        logger.info(f"Cleanup finished. Total videos removed: {total_removed}")

    except Exception as e:
        logger.error(f"Unexpected error in main cleanup process: {e}")

if __name__ == "__main__":
    main()
