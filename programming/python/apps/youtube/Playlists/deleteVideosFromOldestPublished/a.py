import os
import pickle
import time
import logging
import re
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Load sensitive information from environment variables
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CREDENTIALS_FILE = "youtube_credentials.json"

# Playlist ID to clean up (replace with your specific playlist)
PLAYLIST_ID = "PLY8Bm7EI5jJXynRQUem7v27jE4Jva9UDW"

# Time delay in seconds to avoid hitting quota too fast
TIME_DELAY = 2

def get_authenticated_service():
    """Authenticate and return the YouTube API client."""
    try:
        credentials = None
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": CLIENT_ID,
                            "client_secret": CLIENT_SECRET,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": [
                                "urn:ietf:wg:oauth:2.0:oob",
                                "http://localhost"
                            ]
                        }
                    },
                    SCOPES
                )
                credentials = flow.run_local_server(port=0)

            with open(CREDENTIALS_FILE, 'wb') as token:
                pickle.dump(credentials, token)

        return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise

def get_comprehensive_playlist_items(youtube, playlist_id):
    """
    Fetch ALL videos in the playlist with comprehensive pagination handling.
    
    This method ensures we get every single item in the playlist, 
    regardless of how many there are.
    """
    items = []
    next_page_token = None
    total_fetched = 0

    try:
        while True:
            # Prepare request parameters
            request_params = {
                'part': 'snippet',
                'playlistId': playlist_id,
                'maxResults': 50  # YouTube API max per request
            }
            
            # Add page token for pagination if available
            if next_page_token:
                request_params['pageToken'] = next_page_token

            # Execute the request
            response = youtube.playlistItems().list(**request_params).execute()
            
            # Extend items list and log progress
            current_items = response.get('items', [])
            items.extend(current_items)
            total_fetched += len(current_items)
            
            logger.info(f"Fetched {len(current_items)} items. Total fetched: {total_fetched}")
            
            # Get next page token
            next_page_token = response.get('nextPageToken')
            
            # If no more pages, we're done
            if not next_page_token:
                break
            
            # Slight delay to respect API quotas
            time.sleep(TIME_DELAY)

    except Exception as e:
        logger.error(f"Error fetching playlist items: {e}")
        raise

    return items

def is_video_watched(video_title):
    """
    Comprehensive check to determine if a video is considered watched.
    Uses multiple strategies to identify watched videos.
    """
    # Convert title to lowercase for case-insensitive matching
    title_lower = video_title.lower()

    # Comprehensive list of watched indicators
    watched_indicators = [
        # Explicit watched markers
        'watched', 'seen', 'viewed', 
        'completed', 'finished', 'done', 
        'already watched', 'watched already',
        
        # Symbol-based markers
        '✓', '(done)', '[done]', 
        '(completed)', '[completed]',
        '(watched)', '[watched]',
        
        # Additional semantic indicators
        'resume', 'next', 'continue',
        
        # Timestamp or progress indicators
        r'\d+%\s*watched',  # e.g., "50% watched"
        r'\(.*\d+:\d+.*\)',  # timestamps
    ]

    # Use regex for more flexible matching
    for indicator in watched_indicators:
        if re.search(indicator, title_lower):
            return True
    
    return False

def remove_watched_videos(youtube, playlist_items):
    """
    Aggressively remove videos marked as watched from the playlist.
    """
    removed_count = 0
    
    for item in playlist_items:
        try:
            video_title = item['snippet']['title']
            
            # Check if video is watched
            if is_video_watched(video_title):
                # Delete the playlist item
                youtube.playlistItems().delete(id=item['id']).execute()
                
                logger.info(f"REMOVED: {video_title}")
                removed_count += 1
                
                # Small delay to respect API quotas
                time.sleep(TIME_DELAY)
        
        except googleapiclient.errors.HttpError as e:
            logger.error(f"Error removing video '{video_title}': {e}")
        except Exception as e:
            logger.warning(f"Unexpected error processing video: {e}")
    
    return removed_count

def main():
    """
    Main function to comprehensively clean up watched videos from a playlist.
    
    Strategy:
    1. Authenticate with YouTube
    2. Fetch ALL playlist items
    3. Remove all watched videos
    4. Repeat until no more watched videos are found
    """
    try:
        # Authenticate YouTube service
        youtube = get_authenticated_service()
        
        total_removed = 0
        iteration = 1
        
        while True:
            logger.info(f"\n--- Playlist Cleanup Iteration {iteration} ---")
            
            # Fetch ALL playlist items
            playlist_items = get_comprehensive_playlist_items(youtube, PLAYLIST_ID)
            
            # Check if playlist is empty
            if not playlist_items:
                logger.info("Playlist is empty. No videos to remove.")
                break
            
            # Remove watched videos
            removed_this_iteration = remove_watched_videos(youtube, playlist_items)
            total_removed += removed_this_iteration
            
            # Log results
            logger.info(f"Removed {removed_this_iteration} watched video(s) in this iteration.")
            logger.info(f"Total videos removed so far: {total_removed}")
            
            # Stop if no more videos were removed
            if removed_this_iteration == 0:
                logger.info("No more watched videos found. Cleanup complete.")
                break
            
            iteration += 1
            time.sleep(TIME_DELAY)
    
    except Exception as e:
        logger.error(f"Unexpected error in main cleanup process: {e}")

if __name__ == "__main__":
    main()
