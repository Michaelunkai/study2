# File: youtube_mirage_playlist.py
import os
import pickle
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery
import googleapiclient.errors

# Define the scope for the YouTube Data API.
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_authenticated_service():
    credentials = None
    current_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(current_dir, "token.pickle")
    
    # Load saved credentials if available.
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            credentials = pickle.load(token)
    
    # If credentials are not valid, refresh or perform OAuth flow.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            client_secrets_path = os.path.join(current_dir, "client_secret.json")
            if not os.path.exists(client_secrets_path):
                raise FileNotFoundError(f"{client_secrets_path} not found. Ensure it is in the same directory as the script.")
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, SCOPES)
            credentials = flow.run_local_server(port=8080, open_browser=True)
        # Save the credentials for future runs.
        with open(token_path, "wb") as token:
            pickle.dump(credentials, token)
    
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def create_playlist(youtube, title, description="", privacy_status="public"):
    request_body = {
        "snippet": {
            "title": title,
            "description": description
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }
    response = youtube.playlists().insert(
        part="snippet,status",
        body=request_body
    ).execute()
    return response["id"]

def add_video_to_playlist(youtube, playlist_id, video_id):
    request_body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }
    response = youtube.playlistItems().insert(
        part="snippet",
        body=request_body
    ).execute()
    return response

def get_uploads_playlist_id(youtube):
    channels_response = youtube.channels().list(
        part="contentDetails",
        mine=True
    ).execute()
    if not channels_response.get("items"):
        raise Exception("No channel found.")
    uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    return uploads_playlist_id

def get_videos_with_keyword(youtube, keyword):
    """
    Collects all published videos from your uploads that contain the keyword in their title.
    """
    uploads_playlist_id = get_uploads_playlist_id(youtube)
    next_page_token = None
    matching_videos = []
    keyword_lower = keyword.lower()

    while True:
        playlist_response = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        
        for item in playlist_response.get("items", []):
            title = item["snippet"]["title"]
            if keyword_lower in title.lower():
                video_id = item["contentDetails"]["videoId"]
                published_at = item["snippet"]["publishedAt"]
                matching_videos.append({
                    "video_id": video_id,
                    "title": title,
                    "published_at": published_at
                })
        
        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    # Sort videos by published date (oldest first).
    matching_videos.sort(key=lambda x: datetime.strptime(x["published_at"], "%Y-%m-%dT%H:%M:%SZ"))
    return matching_videos

def add_videos_to_playlist_sorted(youtube, playlist_id, keyword):
    matching_videos = get_videos_with_keyword(youtube, keyword)
    print(f"Found {len(matching_videos)} videos with '{keyword}' in the title.")
    for video in matching_videos:
        print(f"Adding video {video['video_id']} titled '{video['title']}' (Uploaded: {video['published_at']}).")
        add_video_to_playlist(youtube, playlist_id, video["video_id"])

if __name__ == '__main__':
    try:
        # Authenticate and build the YouTube API service.
        youtube_service = get_authenticated_service()
        
        # Create a new public playlist named "mirage".
        playlist_title = "mirage"
        playlist_description = "All published videos with 'mirage' in the title, from oldest to newest."
        new_playlist_id = create_playlist(youtube_service, playlist_title, playlist_description, "public")
        print(f"Created new playlist '{playlist_title}' with ID: {new_playlist_id}")
        
        # Add every video with "mirage" in its title to the new playlist in order from oldest to newest.
        add_videos_to_playlist_sorted(youtube_service, new_playlist_id, "mirage")
    except Exception as e:
        print(f"An error occurred: {e}")
