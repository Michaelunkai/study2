import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery
import googleapiclient.errors

# Define the scope for the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_authenticated_service():
    credentials = None
    current_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(current_dir, "token.pickle")
    
    # Check if token.pickle exists for saved credentials.
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            credentials = pickle.load(token)
    
    # If no valid credentials are available, perform the OAuth flow.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # Use "client_secret.json" (ensure it exists in the same directory)
            client_secrets_path = os.path.join(current_dir, "client_secret.json")
            if not os.path.exists(client_secrets_path):
                raise FileNotFoundError(f"{client_secrets_path} does not exist. Please ensure the file is in the same directory as the script.")
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, SCOPES)
            # Use run_local_server instead of run_console.
            credentials = flow.run_local_server(port=8080, open_browser=True)
        # Save the credentials for future runs.
        with open(token_path, "wb") as token:
            pickle.dump(credentials, token)
    
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def publish_for_kids(youtube):
    # Retrieve channel details to get the uploads playlist ID.
    channels_response = youtube.channels().list(
        part="contentDetails",
        mine=True
    ).execute()
    
    if "items" not in channels_response or not channels_response["items"]:
        print("No channel found.")
        return

    uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    
    next_page_token = None
    while True:
        # Retrieve videos from the uploads playlist.
        playlist_response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        
        for item in playlist_response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            video_response = youtube.videos().list(
                part="status",
                id=video_id
            ).execute()
            
            if not video_response.get("items"):
                continue  # Skip if video details are not found
            
            video = video_response["items"][0]
            # Check if the video is set to "private" (assumed to be your draft)
            if video["status"]["privacyStatus"] == "private":
                # Update the status: set to public and mark as made for kids.
                video_status = video["status"]
                video_status["privacyStatus"] = "public"
                video_status["selfDeclaredMadeForKids"] = True

                update_response = youtube.videos().update(
                    part="status",
                    body={
                        "id": video_id,
                        "status": video_status
                    }
                ).execute()
                print(f"Updated video {video_id} to public and marked as for kids.")
        
        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

if __name__ == '__main__':
    try:
        # Authenticate and build the YouTube API service
        youtube_service = get_authenticated_service()
        # Process and update videos accordingly
        publish_for_kids(youtube_service)
    except Exception as e:
        print(f"An error occurred: {e}")
