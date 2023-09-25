from classes.wav import Wav
from classes.spotify import SpotifyPlaylist

MUSIC_DIRECTORY = ""
DNB_PLAYLIST_URI = "https://open.spotify.com/playlist/2N4OvEsC9kf6LVVrc4397m?si=98eb00cf407949c7"
FILTER_PLAYLIST_URI = "https://open.spotify.com/playlist/2GphZJwY0ZDy5dn2J8KTEJ?si=857bab2f38bf4399"

def main():
    # Create class instances
    # wav = Wav(MUSIC_DIRECTORY)
    dnb_spotify = SpotifyPlaylist(DNB_PLAYLIST_URI)
    filter_spotify = SpotifyPlaylist(FILTER_PLAYLIST_URI)

    dnb_tracks = dnb_spotify.get_tracks()
    filter_tracks = filter_spotify.get_tracks()

    overlap = [track for track in dnb_tracks if track in filter_tracks]

    for track in overlap:
        print(track)


if __name__ == "__main__":
    main()
