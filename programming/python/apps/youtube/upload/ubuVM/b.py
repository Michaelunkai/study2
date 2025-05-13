import os
import time
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Path to the client_secret.json file
CLIENT_SECRET_FILE = 'client_secret.json'

# Path to the folder containing videos
VIDEO_FOLDER = '/home/ubuntu/Downloads'

# Maximum number of retries for failed uploads
MAX_RETRIES = 3

# Delay between retries (in seconds)
RETRY_DELAY = 10

def get_authenticated_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            try:
                # Try to use the local server flow (for environments with a browser)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                # Fallback for headless environments (e.g., servers)
                print("Could not open a browser. Please visit the following URL to authorize this application:")
                auth_url, _ = flow.authorization_url(prompt='consent')
                print(auth_url)
                print("Enter the authorization code:")
                auth_code = input()
                creds = flow.fetch_token(code=auth_code)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, file_path, title):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            body = {
                'snippet': {
                    'title': title,
                    'description': 'Uploaded by Python script',
                    'tags': ['upload', 'python', 'youtube'],
                    'categoryId': '22'  # Category ID for People & Blogs
                },
                'status': {
                    'privacyStatus': 'public',  # Can be 'public', 'unlisted', or 'private'
                    'selfDeclaredMadeForKids': False  # Not for kids
                }
            }

            media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
            request = youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if 'id' in response:
                    print(f'Video id "{response["id"]}" was successfully uploaded.')
                    # Verify the video is published
                    video_id = response['id']
                    video_status = youtube.videos().list(
                        part='status',
                        id=video_id
                    ).execute()
                    if video_status['items'][0]['status']['uploadStatus'] == 'processed':
                        print(f'Video "{title}" is published and available.')
                        return True  # Upload and publish successful
                    else:
                        print(f'Video "{title}" is still processing. Waiting...')
                        time.sleep(10)  # Wait for the video to process
                else:
                    print(f'The upload failed with an unexpected response: {response}')
                    retries += 1
                    break
        except HttpError as e:
            print(f'An HTTP error {e.resp.status} occurred: {e.content.decode()}')
            retries += 1
            if retries < MAX_RETRIES:
                print(f'Retrying in {RETRY_DELAY} seconds...')
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            retries += 1
            if retries < MAX_RETRIES:
                print(f'Retrying in {RETRY_DELAY} seconds...')
                time.sleep(RETRY_DELAY)

    print(f'Failed to upload {file_path} after {MAX_RETRIES} retries.')
    return False  # Upload failed after retries

def main():
    youtube = get_authenticated_service()
    for filename in os.listdir(VIDEO_FOLDER):
        if filename.endswith('.mp4') or filename.endswith('.mov') or filename.endswith('.avi') or filename.endswith('.mkv'):
            file_path = os.path.join(VIDEO_FOLDER, filename)
            title = os.path.splitext(filename)[0]  # Use the file name as the title
            print(f'Found video file: {file_path}')
            print(f'Uploading {filename}...')

            success = upload_video(youtube, file_path, title)
            if not success:
                print(f'Skipping {filename} due to upload failure.')
            else:
                print(f'Successfully uploaded and published {filename}.')

    print('All videos processed.')

if __name__ == '__main__':
    main()
