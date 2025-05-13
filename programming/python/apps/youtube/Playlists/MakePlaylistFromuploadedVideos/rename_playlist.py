# File: rename_playlist.py
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

def find_playlist_by_title(youtube, title):
    # Retrieve all playlists owned by the authenticated user.
    playlists = []
    next_page_token = None
    while True:
        request = youtube.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        playlists.extend(response.get("items", []))
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    # Find the playlist with the specified title (case insensitive).
    for playlist in playlists:
        if playlist["snippet"]["title"].lower() == title.lower():
            return playlist
    return None

def rename_playlist(youtube, playlist_id, new_title):
    # First, retrieve the existing playlist snippet.
    playlist_response = youtube.playlists().list(
        part="snippet",
        id=playlist_id
    ).execute()

    if not playlist_response.get("items"):
        raise Exception("Playlist not found.")

    playlist = playlist_response["items"][0]
    # Update the title.
    playlist["snippet"]["title"] = new_title

    # Update the playlist resource.
    update_response = youtube.playlists().update(
        part="snippet",
        body={
            "id": playlist_id,
            "snippet": playlist["snippet"]
        }
    ).execute()
    return update_response

if __name__ == '__main__':
    try:
        # Authenticate and build the YouTube API service.
        youtube = get_authenticated_service()
        
        # Look for the playlist titled "mirage".
        old_title = "mirage"
        new_title = "Assassin's Creed mirage"
        playlist = find_playlist_by_title(youtube, old_title)
        
        if playlist is None:
            print(f"No playlist found with the title '{old_title}'.")
        else:
            playlist_id = playlist["id"]
            print(f"Found playlist '{old_title}' with ID: {playlist_id}. Renaming it to '{new_title}'.")
            updated_playlist = rename_playlist(youtube, playlist_id, new_title)
            print(f"Playlist renamed successfully. New title: {updated_playlist['snippet']['title']}")
    except Exception as e:
        print(f"An error occurred: {e}")

