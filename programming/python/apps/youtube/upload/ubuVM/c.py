import os
import time
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Define the scopes and file paths
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRET_FILE = 'client_secret.json'
VIDEO_FOLDER = '/home/ubuntu/Downloads'
UPLOADED_RECORD = 'uploaded_videos.txt'

# Maximum number of retries for failed uploads and delay between retries (in seconds)
MAX_RETRIES = 3
RETRY_DELAY = 10

def get_authenticated_service():
    creds = None
    # Load stored credentials if they exist
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Refresh or get new credentials if necessary
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            try:
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print("Could not open a browser. Please visit the following URL to authorize this application:")
                auth_url, _ = flow.authorization_url(prompt='consent')
                print(auth_url)
                print("Enter the authorization code:")
                auth_code = input()
                creds = flow.fetch_token(code=auth_code)
        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('youtube', 'v3', credentials=creds)

def load_uploaded_videos():
    """Load the list of already uploaded videos from file."""
    if os.path.exists(UPLOADED_RECORD):
        with open(UPLOADED_RECORD, 'r') as f:
            uploaded = {line.strip() for line in f if line.strip()}
    else:
        uploaded = set()
    return uploaded

def save_uploaded_video(video_filename):
    """Append a video filename to the uploaded record."""
    with open(UPLOADED_RECORD, 'a') as f:
        f.write(video_filename + "\n")

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
                    'privacyStatus': 'public',  # 'public', 'unlisted', or 'private'
                    'selfDeclaredMadeForKids': False
                }
            }
            media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
            request = youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )

            response = None
            # This loop handles the resumable upload
            while response is None:
                status, response = request.next_chunk()
            
            if 'id' in response:
                print(f'Video id "{response["id"]}" was successfully uploaded.')
                # Make a single check of the processing status
                video_status = youtube.videos().list(
                    part='status',
                    id=response['id']
                ).execute()
                status_info = video_status['items'][0]['status']
                if status_info.get('uploadStatus') == 'processed':
                    print(f'Video "{title}" is processed and available.')
                else:
                    print(f'Video "{title}" has been uploaded but is still processing.')
                return True  # Upload successful
            else:
                print(f'Unexpected response: {response}')
                retries += 1
                break

        except HttpError as e:
            print(f'HTTP error {e.resp.status} occurred: {e.content.decode()}')
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
    return False

def main():
    youtube = get_authenticated_service()
    uploaded_videos = load_uploaded_videos()

    for filename in os.listdir(VIDEO_FOLDER):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            if filename in uploaded_videos:
                print(f'Skipping "{filename}" (already uploaded).')
                continue

            file_path = os.path.join(VIDEO_FOLDER, filename)
            title = os.path.splitext(filename)[0]
            print(f'Found video file: {file_path}')
            print(f'Uploading "{filename}"...')

            if upload_video(youtube, file_path, title):
                print(f'Successfully uploaded and published "{filename}".')
                save_uploaded_video(filename)
            else:
                print(f'Skipping "{filename}" due to upload failure.')

    print('All videos processed.')

if __name__ == '__main__':
    main()
