import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate_youtube():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def get_uploads_playlist_id(youtube):
    response = youtube.channels().list(part="contentDetails", mine=True).execute()
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_all_video_ids(youtube, uploads_playlist_id):
    video_ids = []
    next_page_token = None
    while True:
        response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return video_ids

def filter_private_videos(youtube, video_ids):
    private_ids = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        response = youtube.videos().list(
            part="status",
            id=",".join(chunk)
        ).execute()
        for item in response["items"]:
            if item["status"]["privacyStatus"] == "private":
                private_ids.append(item["id"])
    return private_ids

def set_videos_public(youtube, video_ids):
    for vid in video_ids:
        youtube.videos().update(
            part="status",
            body={
                "id": vid,
                "status": {
                    "privacyStatus": "public"
                }
            }
        ).execute()
        print(f"✅ Changed to public: https://www.youtube.com/watch?v={vid}")

if __name__ == "__main__":
    youtube = authenticate_youtube()
    uploads_playlist_id = get_uploads_playlist_id(youtube)
    all_video_ids = get_all_video_ids(youtube, uploads_playlist_id)
    private_videos = filter_private_videos(youtube, all_video_ids)

    if not private_videos:
        print("🎉 No private videos found.")
    else:
        print(f"Found {len(private_videos)} private video(s). Updating to public...")
        set_videos_public(youtube, private_videos)
        print("🎯 Done.")
