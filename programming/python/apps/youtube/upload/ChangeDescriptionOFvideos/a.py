import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# This scope allows for full read/write access to the authenticated user's YouTube account.
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_client_secrets_path():
    # Determine the correct credentials path based on the operating system.
    if os.name == "nt":
        # Windows
        return r"C:\backup\windowsapps\Credentials\youtube\client_secret.json"
    else:
        # Linux (adjust if needed)
        return "/mnt/c/backup/windowsapps/Credentials/youtube/client_secret.json"

def main():
    # Allow insecure transport for testing (remove this in production)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    client_secrets_file = get_client_secrets_path()
    
    # Set up the OAuth 2.0 flow and create the API client
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
    # Use run_local_server instead of run_console
    credentials = flow.run_local_server(port=0)
    youtube = build("youtube", "v3", credentials=credentials)

    # Retrieve the channel's uploads playlist ID
    channels_response = youtube.channels().list(
        part="contentDetails",
        mine=True
    ).execute()

    uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    print("Uploads playlist ID:", uploads_playlist_id)

    # Get all video IDs from the uploads playlist
    video_ids = []
    next_page_token = None
    while True:
        playlist_response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in playlist_response.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    print(f"Found {len(video_ids)} videos.")

    # Define the new description text
    new_description = "hope you enjoy the content. please like and subscribe for more! :)"

    # Iterate over each video and update its description
    for video_id in video_ids:
        # Retrieve the current snippet for the video
        video_response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        if not video_response.get("items"):
            continue

        video = video_response["items"][0]
        snippet = video["snippet"]
        # Update the description
        snippet["description"] = new_description

        # Send the update request
        update_response = youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": snippet
            }
        ).execute()

        print(f"Updated video {video_id}")

if __name__ == "__main__":
    main()
