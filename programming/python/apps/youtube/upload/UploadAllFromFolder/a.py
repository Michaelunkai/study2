#!/usr/bin/env python
import os
import time
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http
import googleapiclient.errors
from google.auth.transport.requests import Request
from concurrent.futures import ThreadPoolExecutor
import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# YouTube API constants
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "client_secret.json"  # You'll need to create this - see instructions
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_PICKLE_FILE = "token.pickle"

# Number of concurrent uploads (adjust based on your internet speed)
MAX_CONCURRENT_UPLOADS = 3

# Video directory to upload from
VIDEO_DIR = "F:/yt"

# Supported video file extensions
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.3gp', '.webm']

def get_authenticated_service():
    """Get an authenticated YouTube service instance."""
    credentials = None
    
    # Load credentials from file if it exists
    if os.path.exists(TOKEN_PICKLE_FILE):
        logger.info("Loading credentials from file...")
        with open(TOKEN_PICKLE_FILE, "rb") as token:
            credentials = pickle.load(token)
    
    # If credentials don't exist or are expired, refresh or get new ones
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            logger.info("Refreshing access token...")
            credentials.refresh(Request())
        else:
            logger.info("Fetching new credentials...")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, "wb") as token:
            pickle.dump(credentials, token)
    
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

def natural_sort_key(s):
    """Sort strings with embedded numbers naturally."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def get_all_videos():
    """Get all videos from the directory, including subdirectories."""
    all_videos = []
    
    for root, _, files in os.walk(VIDEO_DIR):
        for file in files:
            if any(file.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
                full_path = os.path.join(root, file)
                all_videos.append(full_path)
    
    # Sort naturally by filename
    return sorted(all_videos, key=natural_sort_key)

def initialize_upload(youtube, video_path):
    """Initialize and perform the upload process for a single video."""
    file_name = os.path.basename(video_path)
    # Use filename (without extension) as title
    title = os.path.splitext(file_name)[0]
    
    body = {
        "snippet": {
            "title": title,
            "description": f"Uploaded by automatic script on {time.strftime('%Y-%m-%d')}",
            "tags": ["auto-upload"],
            "categoryId": "22"  # People & Blogs category
        },
        "status": {
            "privacyStatus": "private"  # Set to 'private', 'unlisted', or 'public'
        }
    }
    
    # Call the API's videos.insert method to create and upload the video
    media_file = googleapiclient.http.MediaFileUpload(
        video_path, 
        chunksize=1024*1024,
        resumable=True
    )
    
    try:
        logger.info(f"Starting upload for: {file_name}")
        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media_file
        )
        
        # Upload with progress tracking
        response = None
        last_progress = 0
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                # Only log if progress changes by at least 5%
                if progress >= last_progress + 5:
                    logger.info(f"Uploaded {progress}% of {file_name}")
                    last_progress = progress
        
        logger.info(f"Upload Complete! Video ID: {response['id']} - {file_name}")
        
        # Delete video after successful upload
        os.remove(video_path)
        logger.info(f"Deleted file: {file_name}")
        
        return True, file_name
    
    except googleapiclient.errors.HttpError as e:
        logger.error(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return False, file_name
    except Exception as e:
        logger.error(f"An error occurred during upload of {file_name}: {str(e)}")
        return False, file_name

def upload_videos_concurrently(youtube, video_paths):
    """Upload multiple videos concurrently using a thread pool."""
    successful = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_UPLOADS) as executor:
        futures = [executor.submit(initialize_upload, youtube, video_path) for video_path in video_paths]
        
        for future in futures:
            success, file_name = future.result()
            if success:
                successful += 1
            else:
                failed += 1
    
    return successful, failed

def main():
    """Main function to run the YouTube uploader."""
    logger.info("YouTube Batch Video Uploader Starting...")
    
    # Check if client secrets file exists
    if not os.path.exists(CLIENT_SECRETS_FILE):
        logger.error(f"Client secrets file '{CLIENT_SECRETS_FILE}' not found.")
        logger.error("Please download it from the Google API Console and place it in the same directory as this script.")
        return
    
    # Get all video files
    video_paths = get_all_videos()
    
    if not video_paths:
        logger.warning(f"No video files found in {VIDEO_DIR}")
        return
    
    logger.info(f"Found {len(video_paths)} videos to upload")
    
    # Get the YouTube API service
    youtube = get_authenticated_service()
    
    # Upload videos concurrently
    start_time = time.time()
    successful, failed = upload_videos_concurrently(youtube, video_paths)
    end_time = time.time()
    
    # Calculate statistics
    total_time = end_time - start_time
    total_videos = successful + failed
    
    logger.info("=" * 50)
    logger.info("Upload process completed!")
    logger.info(f"Total videos processed: {total_videos}")
    logger.info(f"Successfully uploaded: {successful}")
    logger.info(f"Failed uploads: {failed}")
    logger.info(f"Total time: {total_time:.2f} seconds")
    if successful > 0:
        logger.info(f"Average time per successful upload: {total_time/successful:.2f} seconds")
    logger.info("=" * 50)

if __name__ == "__main__":
    main()
