import os
import pickle
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from datetime import datetime

# Client ID and Client Secret
CLIENT_ID = "878245964235-g606cv2pp4oe647bebtu7tj7vjk0esq4.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# OAuth 2.0 scopes for YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Replace with your Playlist ID
PLAYLIST_ID = "PLY8Bm7EI5jJXynRQUem7v27jE4Jva9UDW"

# List of channel names
CHANNEL_NAMES = [
    "Patrick Cc:", "Visual Venture", "Johnny Harris", "moon-real", "Alex Meyers",
    "Karsten Runquist", "SunnyV2", "penguinz0", "JRE Clips",
    "Kurzgesagt â€“ In a Nutshell", "SpookyRice", "Fireship", "Cr1tiKaL Stream",
    "DuduFaruk", "YMS", "Eddy Burback", "ralphthemoviemaker", "Tell Us More",
    "videogamedunkey", "MagnatesMedia", "PowerfulJRE", "Ghost Gum",
    "Nox Jackson", "Everything Critical", "PodSip", "ClipCove", "Louis C.K.",
    "NakeyJakey", "Trip", "JRExtra", "gvinatibatsibur", "cycasmotivationclips",
    "BestPodcastShorts", "Satori Sounds", "James Jani", "exurb1a", "972Vape",
    "EmpLemon", "Super Eyepatch Wolf", "Sideways", "Jenny Nicholson",
    "Budders Cannabis", "Cheeky S.O.B", "Atomic", "Modern Cannabists",
    "NotBLD", "Drew Gooden", "RPCS3", "Jacob Geller", "Razbuten",
    "Vapelife X (WakeAndVape)", "The Vape Critic", "I Hate Everything"
]

# Path to the file storing watched video IDs
WATCHED_VIDEOS_FILE = "watched_videos.txt"

# Estimated quota cost per request
QUOTA_COST_SEARCH = 10  # Reduced to 10 units per search request by limiting fields
QUOTA_COST_PLAYLIST_ITEMS = 50

# Maximum quota limit per run
MAX_QUOTA = 10000

# Maximum number of videos to fetch and add to the playlist
MAX_VIDEOS = 1000

# Credentials file to store OAuth tokens
CREDENTIALS_FILE = "youtube_credentials.json"

def get_authenticated_service():
    credentials = None
    
    # Check if there are saved credentials
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'rb') as token:
            credentials = pickle.load(token)

    # If no valid credentials, refresh or initiate OAuth flow
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
                        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                    }
                },
                SCOPES
            )
            credentials = flow.run_local_server(port=0)

        # Save credentials to file
        with open(CREDENTIALS_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)


def get_channel_id(youtube, channel_name):
    try:
        request = youtube.search().list(
            part="id",
            q=channel_name,
            type="channel",
            maxResults=1,
            fields="items(id(channelId))"
        )
        response = request.execute()

        if response["items"]:
            return response["items"][0]["id"]["channelId"]
        else:
            print(f"No channel found for name: {channel_name}")
            return None
    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")
        return None


def get_videos_by_channel(youtube, channel_id, start_date, max_results):
    videos = []
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        publishedAfter=start_date,
        type="video",
        maxResults=50,
        fields="items(id(videoId),snippet(title))"
    )
    while request and len(videos) < max_results:
        response = request.execute()

        for item in response["items"]:
            videos.append({
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"]
            })

        request = youtube.search().list_next(request, response)
    return videos[:max_results]


def load_watched_videos(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(file.read().splitlines())
    return set()


def save_watched_videos(file_path, watched_videos):
    with open(file_path, 'w') as file:
        file.write("\n".join(watched_videos))


def add_videos_to_playlist(youtube, playlist_id, video_ids, watched_videos, current_quota, max_quota):
    new_watched_videos = set()
    for video in video_ids:
        if video["videoId"] not in watched_videos:
            if current_quota + QUOTA_COST_PLAYLIST_ITEMS > max_quota:
                print("Quota limit reached. Cannot perform further API calls.")
                break

            request = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video["videoId"]
                        }
                    }
                }
            )
            request.execute()
            current_quota += QUOTA_COST_PLAYLIST_ITEMS
            print(f"Added video: {video['title']} (ID: {video['videoId']})")
            new_watched_videos.add(video["videoId"])
    return new_watched_videos, current_quota


def main():
    youtube = get_authenticated_service()

    date_str = input("Enter the start date (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(date_str, "%Y-%m-%d").isoformat("T") + "Z"
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    watched_videos = load_watched_videos(WATCHED_VIDEOS_FILE)

    current_quota = 0
    all_videos = []
    video_limit = MAX_VIDEOS

    for channel_name in CHANNEL_NAMES:
        if video_limit <= 0:
            break

        channel_id = get_channel_id(youtube, channel_name)
        if channel_id:
            videos = get_videos_by_channel(youtube, channel_id, start_date, video_limit)
            all_videos.extend(videos)
            video_limit -= len(videos)

        if current_quota + len(all_videos) * QUOTA_COST_PLAYLIST_ITEMS > MAX_QUOTA:
            print("Quota limit reached. Stopping.")
            break

    new_watched_videos, current_quota = add_videos_to_playlist(youtube, PLAYLIST_ID, all_videos, watched_videos, current_quota, MAX_QUOTA)
    watched_videos.update(new_watched_videos)
    save_watched_videos(WATCHED_VIDEOS_FILE, watched_videos)

    print(f"Total videos added: {len(new_watched_videos)}")


if __name__ == "__main__":
    main()

