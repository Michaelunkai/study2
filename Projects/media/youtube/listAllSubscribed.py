import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
OAUTH_CLIENT_FILE = r"C:\study\Credentials\youtube\OAuthclient.txt"

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
            raise ValueError("CLIENT_ID or CLIENT SECRET not found in the file.")
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

def list_subscribed_channels(youtube):
    channels = []
    request = youtube.subscriptions().list(
        part="snippet",
        mine=True,
        maxResults=50,
        fields="nextPageToken,items/snippet/title"
    )
    while request:
        response = request.execute()
        for item in response['items']:
            channel_title = item['snippet']['title']
            channels.append(channel_title)
            print(f"Subscribed to: {channel_title}")
        request = youtube.subscriptions().list_next(request, response)
    return channels

def main():
    client_id, client_secret = read_client_credentials(OAUTH_CLIENT_FILE)
    youtube = get_authenticated_service(client_id, client_secret)
    list_subscribed_channels(youtube)

if __name__ == "__main__":
    main()
