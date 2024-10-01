import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime
from google.auth.transport.requests import Request

# Replace with your Playlist ID
PLAYLIST_ID = "ID"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Path to the OAuth client credentials file
OAUTH_CLIENT_FILE = r"C:\study\Credentials\youtube\OAuthclient.txt"

def read_client_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        client_id = None
        client_secret = None
        for line in lines:
            if line.startswith("CLIENT_ID="):
                client_id = line.strip().split("=")[1]
            elif line.startswith("CLIENT_SECRET="):
                client_secret = line.strip().split("=")[1]
        if not client_id or not client_secret:
            raise ValueError("CLIENT_ID or CLIENT_SECRET not found in the file.")
        return client_id, client_secret

def get_authenticated_service(client_id, client_secret):
    credentials = None
    # Check if token.pickle file exists
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, request the user to log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
                {
                    "installed": {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                    }
                },
                SCOPES
            )
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def get_channel_id(youtube, channel_name):
    request = youtube.search().list(
        q=channel_name,
        part="snippet",
        type="channel"
    )
    response = request.execute()
    if response["items"]:
        return response["items"][0]["snippet"]["channelId"]
    return None

def get_videos_by_channel(youtube, channel_id, start_date):
    videos = []
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        publishedAfter=start_date,
        type="video",
        maxResults=50
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            videos.append(item["id"]["videoId"])
        request = youtube.search().list_next(request, response)
    return videos

def add_videos_to_playlist(youtube, playlist_id, video_ids):
    for video_id in video_ids:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        response = request.execute()
        print(f"Added video ID: {video_id}")

def main():
    client_id, client_secret = read_client_credentials(OAUTH_CLIENT_FILE)
    youtube = get_authenticated_service(client_id, client_secret)

    channel_name = input("Enter YouTube channel name: ")
    date_str = input("Enter the start date (YYYY-MM-DD): ")

    # Validate and format the date
    try:
        start_date = datetime.strptime(date_str, "%Y-%m-%d").isoformat("T") + "Z"
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    channel_id = get_channel_id(youtube, channel_name)
    if not channel_id:
        print(f"Channel {channel_name} not found.")
        return

    videos = get_videos_by_channel(youtube, channel_id, start_date)
    if not videos:
        print(f"No videos found for channel {channel_name} since {date_str}.")
        return

    add_videos_to_playlist(youtube, PLAYLIST_ID, videos)
    print("All videos have been added to the playlist.")

if __name__ == "__main__":
    main()
