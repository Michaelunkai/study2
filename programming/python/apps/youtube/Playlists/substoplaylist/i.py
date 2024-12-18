import os
import pickle
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from datetime import datetime, timedelta, timezone
import time
import webbrowser

# Client ID and Client Secret
CLIENT_ID = "1001369627930-j4lk7ct310l604of916k4oiv8nc95tqh.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# OAuth 2.0 scopes for YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Replace with your Playlist ID
PLAYLIST_ID = "PLY8Bm7EI5jJXynRQUem7v27jE4Jva9UDW"

# List of channel names
CHANNEL_NAMES = [
    "Patrick Cc:", "Visual Venture", "Johnny Harris", "moon-real", "Alex Meyers",
    "Karsten Runquist", "SunnyV2", "penguinz0", "JRE Clips",
    "Kurzgesagt - In a Nutshell", "SpookyRice", "Fireship", "Cr1tiKaL Stream",
    "DuduFaruk", "YMS", "Eddy Burback", "ralphthemoviemaker", "Tell Us More",
    "videogamedunkey", "MagnatesMedia", "PowerfulJRE", "Ghost Gum",
    "Nox Jackson", "Everything Critical", "PodSip", "ClipCove", "Louis C.K.",
    "NakeyJakey", "Trip", "JRExtra", "gvinatibatsibur", "cycasmotivationclips",
    "BestPodcastShorts", "Satori Sounds", "James Jani", "exurb1a", "972Vape",
    "EmpLemon", "Super Eyepatch Wolf", "Sideways", "Jenny Nicholson",
    "Budders Cannabis", "Cheeky S.O.B", "Atomic", "Modern Cannabists",
    "NotBLD", "Drew Gooden", "RPCS3", "Jacob Geller", "Razbuten", "Nina Drama"
]

# Path to the file storing watched video IDs
WATCHED_VIDEOS_FILE = "watched_videos.txt"

# Quota cost constants
QUOTA_COST_SEARCH = 10
QUOTA_COST_PLAYLIST_ITEMS = 50

# Maximum number of videos to fetch and add to the playlist
MAX_VIDEOS = 1000

# Credentials file to store OAuth tokens
CREDENTIALS_FILE = "youtube_credentials.json"

# Time delay in seconds to avoid quota overrun
TIME_DELAY = 1

def get_authenticated_service():
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
                        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                    }
                },
                SCOPES
            )

            auth_url, _ = flow.authorization_url()
            os.system(f"cmd.exe /c start chrome {auth_url}")

            credentials = flow.run_local_server(port=0)

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
        time.sleep(TIME_DELAY)

        if response["items"]:
            return response["items"][0]["id"]["channelId"]
        else:
            print(f"No channel found for name: {channel_name}")
            return None
    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")
        return None

def get_videos_by_channel(youtube, channel_id):
    videos = []
    published_after = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        publishedAfter=published_after,
        type="video",
        maxResults=50,
        fields="items(id(videoId),snippet(title))"
    )
    while request:
        response = request.execute()
        time.sleep(TIME_DELAY)

        for item in response["items"]:
            videos.append({
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"]
            })

        request = youtube.search().list_next(request, response)
    return videos

def load_watched_videos(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(file.read().splitlines())
    return set()

def save_watched_videos(file_path, watched_videos):
    with open(file_path, 'w') as file:
        file.write("\n".join(watched_videos))

def add_videos_to_playlist(youtube, playlist_id, video_ids, watched_videos):
    new_watched_videos = set()
    for video in video_ids:
        if video["videoId"] not in watched_videos:
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
            try:
                request.execute()
                print(f"Added video: {video['title']} (ID: {video['videoId']})")
                new_watched_videos.add(video["videoId"])
                time.sleep(TIME_DELAY)
            except googleapiclient.errors.HttpError as e:
                print(f"An error occurred while adding video: {e}")
                continue
    return new_watched_videos

def main():
    youtube = get_authenticated_service()

    watched_videos = load_watched_videos(WATCHED_VIDEOS_FILE)

    for channel_name in CHANNEL_NAMES:
        channel_id = get_channel_id(youtube, channel_name)
        if channel_id:
            videos = get_videos_by_channel(youtube, channel_id)
            new_watched_videos = add_videos_to_playlist(youtube, PLAYLIST_ID, videos, watched_videos)
            watched_videos.update(new_watched_videos)

    save_watched_videos(WATCHED_VIDEOS_FILE, watched_videos)
    print(f"Total videos added: {len(watched_videos)}")

if __name__ == "__main__":
    main()
