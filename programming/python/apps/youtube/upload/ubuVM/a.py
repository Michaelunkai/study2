#!/usr/bin/env python3
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# Path to your OAuth 2.0 Client Secrets JSON file.
# Rename your file to "client_secret.json" or update this variable accordingly.
CLIENT_SECRETS_FILE = "client_secret.json"

# This scope allows full access to upload videos.
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_authenticated_service():
    # Set up the OAuth 2.0 flow using a local server for authentication.
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES
    )
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, file_path):
    file_name = os.path.basename(file_path)
    # Define the metadata for the video.
    body = {
        "snippet": {
            "title": file_name,
            "description": "Automatically uploaded via script",
            "categoryId": "22"  # Category 22 corresponds to "People & Blogs"
        },
        "status": {
            "privacyStatus": "private"  # Change to "public" or "unlisted" as needed
        }
    }

    # Prepare the media upload with resumable support.
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print(f"Starting upload for {file_name}")
    response = None
    # Upload the file in chunks and display the progress.
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"Uploading {file_name}: {progress}%")
    print(f"Upload complete for {file_name}\n")

def main():
    youtube = get_authenticated_service()
    directory = "/home/ubuntu/Downloads"

    # Loop through all files in the directory and upload each .mkv file.
    for filename in os.listdir(directory):
        if filename.lower().endswith(".mkv"):
            file_path = os.path.join(directory, filename)
            try:
                upload_video(youtube, file_path)
            except googleapiclient.errors.HttpError as e:
                print(f"HTTP error occurred while uploading {filename}: {e}")
            except Exception as e:
                print(f"Error occurred while uploading {filename}: {e}")

if __name__ == "__main__":
    main()

