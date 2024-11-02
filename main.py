from classes.rekordbox import Rekordbox
from classes.spotify import SpotifyPlaylist

MUSIC_DIRECTORY = "D:\\Music HDD\\WAVs"
DNB_PLAYLIST_URI = "https://open.spotify.com/playlist/2N4OvEsC9kf6LVVrc4397m?si=98eb00cf407949c7"
FILTER_PLAYLIST_URI = "https://open.spotify.com/playlist/2GphZJwY0ZDy5dn2J8KTEJ?si=857bab2f38bf4399"

def main():
    dnb_spotify = SpotifyPlaylist(DNB_PLAYLIST_URI)
    filter_spotify = SpotifyPlaylist(FILTER_PLAYLIST_URI)

    dnb_tracks = dnb_spotify.get_tracks()
    filter_tracks = filter_spotify.get_tracks()

    spotify_tracks = [track for track in dnb_tracks if track not in filter_tracks]

    rekordbox = Rekordbox(MUSIC_DIRECTORY)
    rekordbox_tracks = rekordbox.get_tracks()

    spotify_only = []
    for spotify_track in spotify_tracks:
        if spotify_track not in rekordbox_tracks:
            spotify_only.append(spotify_track)
    
    rekordbox_only = []
    for rekordbox_track in rekordbox_tracks:
        if rekordbox_track not in spotify_tracks:
            rekordbox_only.append(rekordbox_track)

    print(f"\nSpotify Only Tracks ({len(spotify_only)})")
    for track in sorted(spotify_only):
        print(track)

    # print("\nRekordbox Only Tracks ({len(rekordbox_only)})")
    # for track in sorted(rekordbox_only)[:100]:
    #     print(track)
    
    print()


if __name__ == "__main__":
    main()
