import os
import pickle
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime
from google.auth.transport.requests import Request

# Replace with your Playlist ID
PLAYLIST_ID = "PLY8Bm7EI5jJXynRQUem7v27jE4Jva9UDW"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Path to the OAuth client credentials file
OAUTH_CLIENT_FILE = r"C:\backup\windowsapps\Credentials\youtube\OAuthclient.txt"

# Path to the file storing channel IDs
CHANNEL_IDS_FILE = "channel_ids.json"

# List of channel names
CHANNEL_NAMES = [
    "Patrick Cc:", "Visual Venture", "Johnny Harris","moon-real", "Alex Meyers",
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
QUOTA_COST_SEARCH = 100
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
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

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

        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def load_cached_channel_ids():
    if os.path.exists(CHANNEL_IDS_FILE):
        with open(CHANNEL_IDS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_cached_channel_ids(channel_ids):
    with open(CHANNEL_IDS_FILE, 'w') as file:
        json.dump(channel_ids, file)

def get_channel_id(youtube, channel_name, cached_channel_ids):
    if channel_name in cached_channel_ids:
        return cached_channel_ids[channel_name]

    try:
        request = youtube.search().list(
            q=channel_name,
            part="snippet",
            type="channel",
            fields="items(snippet(channelId))"
        )
        response = request.execute()

        if response["items"]:
            channel_id = response["items"][0]["snippet"]["channelId"]
            cached_channel_ids[channel_name] = channel_id
            save_cached_channel_ids(cached_channel_ids)
            return channel_id
    except googleapiclient.errors.HttpError as e:
        if e.resp.status == 403 and 'quotaExceeded' in str(e):
            print("Quota exceeded. Exiting.")
            exit()
    return None

def get_videos_by_channel(youtube, channel_id, start_date):
    videos = []
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        publishedAfter=start_date,
        type="video",
        maxResults=50,
        fields="items(id(videoId),snippet(title))"
    )
    while request:
        response = request.execute()

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

def add_videos_to_playlist(youtube, playlist_id, video_ids, watched_videos, current_quota):
    new_watched_videos = set()
    for video in video_ids:
        if video["videoId"] not in watched_videos:
            if current_quota + QUOTA_COST_PLAYLIST_ITEMS > MAX_QUOTA:
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
    client_id, client_secret = read_client_credentials(OAUTH_CLIENT_FILE)
    youtube = get_authenticated_service(client_id, client_secret)

    date_str = input("Enter the start date (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(date_str, "%Y-%m-%d").isoformat("T") + "Z"
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    watched_videos = load_watched_videos(WATCHED_VIDEOS_FILE)
    cached_channel_ids = load_cached_channel_ids()

    current_quota = 0
    all_videos = []
    for channel_name in CHANNEL_NAMES:
        channel_id = get_channel_id(youtube, channel_name, cached_channel_ids)
        if channel_id:
            videos = get_videos_by_channel(youtube, channel_id, start_date)
            all_videos.extend(videos)

    new_watched_videos, current_quota = add_videos_to_playlist(youtube, PLAYLIST_ID, all_videos, watched_videos, current_quota)
    watched_videos.update(new_watched_videos)
    save_watched_videos(WATCHED_VIDEOS_FILE, watched_videos)

    print("All available videos have been added to the playlist.")

if __name__ == "__main__":
    main()
