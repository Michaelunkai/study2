# a.py ── clone any YouTube / Shorts URL to *your* channel
# deps:  yt-dlp  ffmpeg  google-api-python-client  google-auth-oauthlib

import os, sys, re
from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

# ───────────────────── helpers ────────────────────────────────────────────────
SAFE_CHARS = r'[\\/*?:"<>|]'

def win_safe(s: str) -> str:
    """Strip characters Windows can’t store in filenames."""
    return re.sub(SAFE_CHARS, "", s)

def _find_output_file(info: dict, ydl: YoutubeDL) -> str:
    """
    Robustly locate the final .mp4 written by yt-dlp/ffmpeg, even if keys vary.
    """
    # 1️⃣ ‘filepath’ (present since yt-dlp 2024.07)
    if info.get("filepath") and os.path.isfile(info["filepath"]):
        return info["filepath"]

    # 2️⃣ per-format entry under ‘requested_downloads’
    for req in info.get("requested_downloads", []):
        fp = req.get("filepath")
        if fp and os.path.isfile(fp):
            return fp

    # 3️⃣ ‘_filename’ → adjust ext to .mp4 (merge_output_format)
    if info.get("_filename"):
        guess = os.path.splitext(info["_filename"])[0] + ".mp4"
        if os.path.isfile(guess):
            return guess

    # 4️⃣ fallback: ydl.prepare_filename(info) + .mp4
    guess = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp4"
    if os.path.isfile(guess):
        return guess

    raise FileNotFoundError("Could not locate merged .mp4 – check yt-dlp/ffmpeg")

def download(url: str) -> tuple[str, str, str]:
    """
    Download & merge best video+audio → MP4.
    Returns (path, title, description)
    """
    opts = {
        "format": "bestvideo*+bestaudio/best",
        "merge_output_format": "mp4",
        "restrictfilenames": True,                # ensures OS-safe paths
        "outtmpl": "%(title)s [%(id)s].%(ext)s",
        "noplaylist": True,
        "quiet": False,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        path = _find_output_file(info, ydl)

    title = win_safe(info["title"])
    desc  = info.get("description", "")
    return path, title, desc

def yt_auth():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    flow   = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes)
    creds  = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=creds)

def upload(youtube, path: str, title: str, desc: str) -> str:
    body = {
        "snippet": {"title": title, "description": desc, "categoryId": "22"},
        "status":  {"privacyStatus": "private"}     # change to "public" if you wish
    }
    media = MediaFileUpload(path, resumable=True)
    resp  = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    return resp["id"]

# ───────────────────── main ───────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        url = input("Paste YouTube (or Shorts) URL 👉 ").strip()
        if not url:
            sys.exit("No URL supplied – exiting.")

        print("⬇  Downloading …")
        fpath, title, desc = download(url)
        print("✔  Saved:", fpath)

        print("🔑  Google OAuth …")
        yt = yt_auth()

        print("⬆  Uploading to your channel …")
        vid_id = upload(yt, fpath, title, desc)
        print("✅  Uploaded → https://youtu.be/" + vid_id)

        os.remove(fpath)
        print("🗑  Local file deleted")
    except Exception as err:
        print("❌  Error:", err)

