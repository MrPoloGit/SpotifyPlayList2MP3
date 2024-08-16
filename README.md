# SpotifyPlaylist2MP3

This is an old simple script I made that I remade and finally uploaded which allows you to download MP3 files for all tracks in a given Spotify playlist using YouTube as the source, I made this before realizing spotify-dl exists. 
At least I got some experience working with APIs, and I plan to use Spotify's API in a future project.

## Why?
I am lazy, don't like ads(I ain't paying for premium), and being able to listen to music offline including music that isn't on spotify would be nice.

## Setup
1. Install python3

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SpotifyPlaylist2MP3.git
   cd SpotifyPlaylist2MP3
   ```
3. Download requirements
   ```bash
   pip install -r requirements.txt
   ```
   
4. Create .env file and get Spotify API tokens by making a app on the Spotify developer dashboard
   ```env
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   ```

5. Run it
   ```bash
   python get_playlist_songs.py <playlist_id_1> <playlist_id_2> ...
   ```