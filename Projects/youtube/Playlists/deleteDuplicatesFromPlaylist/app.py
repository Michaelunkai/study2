import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request

# Replace with your Playlist ID
PLAYLIST_ID = "PLR3nd3FqtxEPs2fNcFtg2OBo0xeul5O0W"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Path to the OAuth client credentials file
OAUTH_CLIENT_FILE = r"C:\study\Credentials\youtube\OAuthclient.txt"

# Estimated quota cost per request
QUOTA_COST_PLAYLIST_ITEMS = 50

# Maximum quota limit (You can set this based on your quota limits)
MAX_QUOTA = 10000

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

def get_playlist_items(youtube, playlist_id):
    items = []
    next_page_token = None
    current_quota = 0

    while True:
        if current_quota + QUOTA_COST_PLAYLIST_ITEMS > MAX_QUOTA:
            print("Quota limit reached. Cannot perform further API calls.")
            break

        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        current_quota += QUOTA_COST_PLAYLIST_ITEMS

        items.extend(response.get("items", []))
        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return items, current_quota

def remove_playlist_item(youtube, playlist_item_id, current_quota):
    if current_quota + QUOTA_COST_PLAYLIST_ITEMS > MAX_QUOTA:
        print("Quota limit reached. Cannot perform further API calls.")
        return current_quota

    request = youtube.playlistItems().delete(id=playlist_item_id)
    response = request.execute()
    current_quota += QUOTA_COST_PLAYLIST_ITEMS
    return current_quota

def main():
    client_id, client_secret = read_client_credentials(OAUTH_CLIENT_FILE)
    youtube = get_authenticated_service(client_id, client_secret)

    items, current_quota = get_playlist_items(youtube, PLAYLIST_ID)
    video_counts = {}
    duplicate_items = []

    for item in items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        if video_id in video_counts:
            video_counts[video_id] += 1
            duplicate_items.append(item)
        else:
            video_counts[video_id] = 1

    for item in duplicate_items:
        playlist_item_id = item["id"]
        current_quota = remove_playlist_item(youtube, playlist_item_id, current_quota)
        if current_quota >= MAX_QUOTA:
            break

    print("Duplicates removed from the playlist or quota limit reached.")

if __name__ == "__main__":
    main()
