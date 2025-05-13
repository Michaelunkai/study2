# File: youtube_gta_iv_playlist.py
import os
import pickle
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
    
    # If credentials are not valid, refresh or log in.
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

def add_videos_to_playlist_with_keyword(youtube, playlist_id, keyword):
    uploads_playlist_id = get_uploads_playlist_id(youtube)
    next_page_token = None
    keyword_lower = keyword.lower()
    
    while True:
        playlist_response = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        
        for item in playlist_response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            title = item["snippet"]["title"]
            if keyword_lower in title.lower():
                print(f"Adding video {video_id} with title '{title}' to playlist.")
                add_video_to_playlist(youtube, playlist_id, video_id)
        
        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

if __name__ == '__main__':
    try:
        # Authenticate and build the YouTube API service.
        youtube_service = get_authenticated_service()
        
        # Create a new public playlist named "GTA IV".
        playlist_title = "GTA IV"
        playlist_description = "All published videos with 'GTA IV' in the title."
        new_playlist_id = create_playlist(youtube_service, playlist_title, playlist_description, "public")
        print(f"Created new playlist '{playlist_title}' with ID: {new_playlist_id}")
        
        # Add every published video with "GTA IV" in its title to the new playlist.
        add_videos_to_playlist_with_keyword(youtube_service, new_playlist_id, "GTA IV")
    except Exception as e:
        print(f"An error occurred: {e}")
