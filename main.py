import json
import sys
from difflib import SequenceMatcher

from classes.rekordbox import Rekordbox
from classes.spotify import SpotifyPlaylist


MUSIC_DIRECTORY = "D:\\Music HDD\\WAVs"
DNB_PLAYLIST_URI = "https://open.spotify.com/playlist/2N4OvEsC9kf6LVVrc4397m?si=98eb00cf407949c7"
FILTER_PLAYLIST_URI = "https://open.spotify.com/playlist/2GphZJwY0ZDy5dn2J8KTEJ?si=857bab2f38bf4399"

COMPARE_THRESHOLD_MIN = 0.8

def are_strings_similar(str1, str2):
    """
    Compare two strings for similarity.

    Parameters:
        str1 (str): The first string to compare.
        str2 (str): The second string to compare.
        threshold (float): A similarity threshold (between 0 and 1).
                           Higher values mean stricter similarity requirement.

    Returns:
        bool: True if the similarity ratio is above or equal to the threshold,
              False otherwise.
    """
    similarity_ratio = SequenceMatcher(None, str1, str2).ratio()
    return similarity_ratio >= COMPARE_THRESHOLD_MIN

def main():
    dnb_spotify = SpotifyPlaylist(DNB_PLAYLIST_URI)
    filter_spotify = SpotifyPlaylist(FILTER_PLAYLIST_URI)

    dnb_tracks = dnb_spotify.get_tracks()
    filter_tracks = filter_spotify.get_tracks()

    spotify_tracks = sorted([track for track in dnb_tracks if track not in filter_tracks])

    rekordbox = Rekordbox(MUSIC_DIRECTORY)
    rekordbox_tracks = sorted(rekordbox.get_tracks())

    with open("mapping.json", "r") as f:
        manual_mapping = json.load(f)
    
    paired_tracks = {}

    spotify_only = []
    for spotify_track in spotify_tracks:
        # If manual mapping entry exists for track, set this immediately as the paired track
        if spotify_track.id in manual_mapping:
            matching_tracks = [track for track in rekordbox_tracks if track.id == manual_mapping[spotify_track.id]]
            if len(matching_tracks) == 0:
                print(f"WARNING: Cannot find file \"{manual_mapping[spotify_track.id]}\" for mapping entry for Spotify ID {track.id}")
                sys.exit(1)
            elif len(matching_tracks) >= 2:
                print(f"WARNING: Multiple mapping entries found for Spotify ID {track.id}")
                sys.exit(1)
            paired_tracks[spotify_track.id] = matching_tracks[0].id
            continue

        # If direct string match is found, add to paired tracks
        similar_tracks = [track for track in rekordbox_tracks if spotify_track == track]
        if len(similar_tracks) == 1:
            paired_tracks[spotify_track.id] = similar_tracks[0].id
            continue
        elif len(similar_tracks) >= 2:
            print(f"\nWARNING: Duplicate Rekordbox track \"{spotify_track}\" found")
        
        # Spotify local files cannot be saved to mapping (TODO)
        if spotify_track.id == None:
            continue

        # Check for similar tracks and ask user to find matching
        for rekordbox_track in rekordbox_tracks:
            if rekordbox_track not in similar_tracks and \
                (are_strings_similar(str(spotify_track), str(rekordbox_track)) or are_strings_similar(str(spotify_track), rekordbox_track.formatted_string())):
                    similar_tracks.append(rekordbox_track)

        if len(similar_tracks) > 0:
            print(f"\n\"{spotify_track}\" Similar Tracks:")
            print("(X) None")
            for i in range(len(similar_tracks)):
                print(f"({i+1}) {similar_tracks[i]}")
            
            match_found = False
            while True: 
                response = input(" ")
                if response.upper() == "X":
                    break
                
                try:
                    index = int(response) - 1
                except:
                    index = -1

                if index >= 0 and index < len(similar_tracks):
                    match_found = True
                    paired_tracks[spotify_track.id] = similar_tracks[index].id
                    manual_mapping[spotify_track.id] = similar_tracks[index].id
                    with open("mapping.json", "w") as f:
                        json.dump(manual_mapping, f, indent=4)
                    break
                
                print("Invalid input")
            
            if match_found:
                continue
            
        spotify_only.append(spotify_track)

    print(f"\nSpotify Only Tracks ({len(spotify_only)})")
    for track in sorted(spotify_only):
        print(track)
    
    print()


if __name__ == "__main__":
    main()
