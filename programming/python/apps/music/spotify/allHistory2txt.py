import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Provided credentials
CLIENT_ID = '75fcc11296ec4db78c166b92d4d53024'
CLIENT_SECRET = '9f430ad8b8bc461097e17cb18b86b96b'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-top-read'

def get_top_tracks(total_limit=2000, time_range='long_term'):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))
    
    all_tracks = []
    limit = 50  # maximum allowed per request
    offset = 0
    
    # Fetch tracks using pagination until total_limit is reached or no more tracks are available.
    while len(all_tracks) < total_limit:
        results = sp.current_user_top_tracks(limit=limit, offset=offset, time_range=time_range)
        tracks = results.get('items', [])
        if not tracks:
            break
        all_tracks.extend(tracks)
        offset += limit
        # If fewer than limit tracks are returned, we've reached the end.
        if len(tracks) < limit:
            break
    return all_tracks[:total_limit]

def save_tracks_to_txt(tracks, filename="songs.txt"):
    lines = []
    for idx, track in enumerate(tracks, start=1):
        track_name = track.get('name', 'Unknown')
        artist_names = ", ".join(artist.get('name', 'Unknown') for artist in track.get('artists', []))
        # Create a line with rank, track name, and artists.
        line = f"{idx}: {track_name} by {artist_names}"
        lines.append(line)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Saved {len(tracks)} top tracks to '{filename}'")

def main():
    print("Fetching top tracks...")
    top_tracks = get_top_tracks(total_limit=2000, time_range='long_term')
    print(f"Retrieved {len(top_tracks)} tracks.")
    
    save_tracks_to_txt(top_tracks)

if __name__ == "__main__":
    main()
