import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import argparse
import yt_dlp
import re

# Load environment variables from .env file
load_dotenv()

# Get the client ID and client secret from environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

# Set up Spotify API authentication
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Get Spotify playlist tracks and download corresponding YouTube videos.")
parser.add_argument('playlist_ids', type=str, nargs='+', help="The Spotify Playlist IDs (space-separated)")

# Parse command-line arguments
args = parser.parse_args()

# Process each playlist ID provided in the command line
for playlist_id in args.playlist_ids:
    # Fetch the playlist using the playlist ID
    playlist = sp.playlist(playlist_id)

    # Clean playlist name to be a valid folder name
    playlist_name = re.sub(r'[\\/*?:"<>|]', "", playlist['name'])

    # Create the output directory with the format "playlist_name - playlist_ID"
    output_dir = os.path.join("mp3s", f"{playlist_name} - {playlist_id}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Display the playlist's tracks
    print(f"Playlist Name: {playlist['name']} (ID: {playlist_id})\n")
    for idx, item in enumerate(playlist['tracks']['items']):
        track = item['track']
        song_name = track['name']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        query = f"{song_name} by {artists}"
        print(f"{idx + 1}. {query}")

        # Set up yt-dlp options to save the files in the playlist-specific folder
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',  # Set to 320 kbps for best quality
            }],
            'outtmpl': os.path.join(output_dir, f'{song_name}.%(ext)s'),  # Save in the specific playlist directory
            'noplaylist': True,  # Prevent downloading playlists in case a playlist link is found
            'quiet': False,  # Show detailed progress
            'no_warnings': True,  # Ignore non-fatal warnings
        }

        try:
            # Search on YouTube
            search_results = yt_dlp.YoutubeDL({'quiet': True}).extract_info(f"ytsearch:{query}", download=False)['entries']
            if search_results:
                video_url = search_results[0]['webpage_url']
                print(f"Downloading: {query} - {video_url}")

                # Download the video using yt-dlp
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
            else:
                print(f"No results found for {query}")
        except Exception as e:
            print(f"Error downloading {query}: {e}")
