# a.py — Clone YouTube/Shorts videos to *your* channel
# Usage: python a.py <url1> <url2> ...
# Dependencies: yt-dlp, ffmpeg, google-api-python-client, google-auth-oauthlib

import os, sys, re
from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

# Constants
SAFE_CHARS = r'[\\/*?:"<>|]'
SECRET_PATH = r"C:\Users\micha\Downloads\client_secret.json"

def win_safe(s: str) -> str:
    """Make Windows-safe filename"""
    return re.sub(SAFE_CHARS, "", s)

def _find_output_file(info: dict, ydl: YoutubeDL) -> str:
    """Find final MP4 file from yt-dlp"""
    if info.get("filepath") and os.path.isfile(info["filepath"]):
        return info["filepath"]
    for req in info.get("requested_downloads", []):
        fp = req.get("filepath")
        if fp and os.path.isfile(fp):
            return fp
    if info.get("_filename"):
        guess = os.path.splitext(info["_filename"])[0] + ".mp4"
        if os.path.isfile(guess):
            return guess
    guess = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp4"
    if os.path.isfile(guess):
        return guess
    raise FileNotFoundError("MP4 file not found after download.")

def download(url: str) -> tuple[str, str, str]:
    """Download video and return (filepath, title, description)"""
    opts = {
        "format": "bestvideo*+bestaudio/best",
        "merge_output_format": "mp4",
        "restrictfilenames": True,
        "outtmpl": "%(title)s [%(id)s].%(ext)s",
        "noplaylist": True,
        "quiet": False,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        path = _find_output_file(info, ydl)
    title = win_safe(info.get("title", "No Title"))
    desc = info.get("description", "")
    return path, title, desc

def yt_auth():
    """Authenticate and return YouTube API client"""
    if not os.path.isfile(SECRET_PATH):
        raise FileNotFoundError(f"Missing: {SECRET_PATH}")
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = InstalledAppFlow.from_client_secrets_file(SECRET_PATH, scopes)
    creds = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=creds)

def upload(youtube, path: str, title: str, desc: str) -> str:
    """Upload MP4 to YouTube"""
    body = {
        "snippet": {"title": title, "description": desc, "categoryId": "22"},
        "status": {"privacyStatus": "private"}
    }
    media = MediaFileUpload(path, resumable=True)
    response = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    return response["id"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python a.py <youtube_url1> <youtube_url2> ...")
        sys.exit(1)

    try:
        yt = yt_auth()
    except Exception as e:
        print("❌ YouTube auth failed:", e)
        sys.exit(1)

    for url in sys.argv[1:]:
        try:
            print(f"\n⬇️  Downloading: {url}")
            fpath, title, desc = download(url)
            print("✅ Downloaded:", fpath)

            print("📤 Uploading...")
            video_id = upload(yt, fpath, title, desc)
            print("📺 Uploaded → https://youtu.be/" + video_id)

            os.remove(fpath)
            print("🧹 Deleted local file")

        except Exception as err:
            print(f"❌ Error processing {url}:", err)

