#!/usr/bin/env python3

import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import time

CLIENT_ID = "878245964235-g606cv2pp4oe647bebtu7tj7vjk0esq4.apps.googleusercontent.com"
CLIENT_SECRET = "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"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
PLAYLIST_ID = "PLY8Bm7EI5jJXynRQUem7v27jE4Jva9UDW"
WATCHED_VIDEOS_FILE = "watched_videos.txt"
CREDENTIALS_FILE = "youtube_credentials.json"
TIME_DELAY = 5

CHANNEL_NAMES = [
    "Patrick Cc:", "Visual Venture", "Johnny Harris", "moon-real", "Alex Meyers",
    "Karsten Runquist", "SunnyV2", "penguinz0", "JRE Clips",
    "Kurzgesagt – In a Nutshell", "SpookyRice", "Fireship", "Cr1tiKaL Stream",
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
                        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"]
                    }
                },
                SCOPES
            )
            auth_url, _ = flow.authorization_url(prompt='consent')
            print("Please visit this URL to authorize the application:")
            print(auth_url)
            code = input("Enter the authorization code: ")
            credentials = flow.fetch_token(code=code)

        with open(CREDENTIALS_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def load_watched_videos(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(file.read().splitlines())
    return set()

def save_watched_videos(file_path, watched_videos):
    with open(file_path, 'w') as file:
        file.write("\n".join(watched_videos))

def get_channel_id(youtube, channel_name):
    request = youtube.search().list(
        part="id",
        q=channel_name,
        type="channel",
        maxResults=1
    )
    response = request.execute()
    if response.get("items"):
        return response["items"][0]["id"]["channelId"]
    else:
        print(f"Channel not found: {channel_name}")
        return None

def get_videos_by_channel(youtube, channel_id, published_after):
    videos = []
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        publishedAfter=published_after,
        type="video",
        maxResults=50
    )
    while request:
        response = request.execute()
        for item in response.get("items", []):
            videos.append({
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"]
            })
        request = youtube.search().list_next(request, response)
    return videos

def add_videos_to_playlist(youtube, playlist_id, videos, watched_videos):
    for video in videos:
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
                print(f"Added: {video['title']}")
                watched_videos.add(video["videoId"])
                time.sleep(TIME_DELAY)
            except Exception as e:
                print(f"Error adding video {video['title']}: {e}")

def main():
    youtube = get_authenticated_service()
    print("Authenticated successfully!")

    watched_videos = load_watched_videos(WATCHED_VIDEOS_FILE)
    published_after = (datetime.utcnow() - timedelta(days=1)).isoformat("T") + "Z"

    for channel_name in CHANNEL_NAMES:
        channel_id = get_channel_id(youtube, channel_name)
        if channel_id:
            videos = get_videos_by_channel(youtube, channel_id, published_after)
            add_videos_to_playlist(youtube, PLAYLIST_ID, videos, watched_videos)

    save_watched_videos(WATCHED_VIDEOS_FILE, watched_videos)
    print(f"Process completed. Total videos added: {len(watched_videos)}")

if __name__ == "__main__":
    main()
