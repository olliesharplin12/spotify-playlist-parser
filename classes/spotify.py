import spotipy
import spotipy.oauth2 as oauth2
import sys

from .track import Track
from config import CLIENT_ID, CLIENT_SECRET

FETCH_LIMIT = 100
PLAYLIST_FIELDS = "total,items(track(id,name,artists(name),album(name)))"

class Spotify:
    _sp = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def instance(self):
        if self._sp is None:
            self._sp = self.setup_spotify()
        return self._sp

    def setup_spotify():
        oauth = oauth2.SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri="http://localhost:3000")
        return spotipy.Spotify(auth_manager=oauth)

def is_valid_track(track_json):
    if (track_json["track"]["artists"][0]["name"] == "" and track_json["track"]["album"]["name"] == "") \
        or track_json["track"]["album"]["name"] == "Sheriff's Mixes":
            return False
    return True

def filter_name(name):
        filters = ["-", "("]
        for filter in filters:
            if filter in name:
                name = name.split(filter)[0]
        return name.strip()

class SpotifyPlaylist:
    def __init__(self, playlist_uri):
        self.sp = Spotify.instance()
        self.playlist_uri = playlist_uri
    
    def get_tracks(self):
        tracks_json = []
        offset = 0
        while True:
            response = self.sp.playlist_tracks(self.playlist_uri, offset=offset, limit=FETCH_LIMIT, fields=PLAYLIST_FIELDS)
            tracks_json += response['items']
            if len(response['items']) < FETCH_LIMIT:
                break
            else:
                offset += len(response['items'])
                print(offset)
        
        tracks = []
        for track in tracks_json:
            if not is_valid_track(track):
                continue
            name = filter_name(track["track"]["name"])
            artists = [artist["name"] for artist in track["track"]["artists"]]
            tracks.append(Track(track["track"]["id"], name, artists, track["track"]["name"], artists))
        return tracks


if __name__ == "__main__":
    test_playlist_uri = "https://open.spotify.com/playlist/2QTyeLQCrSXulLc9fSzdzv?si=0c6c01b178024ce7"
    playlist = SpotifyPlaylist(test_playlist_uri)
    tracks = playlist.get_tracks()
    for track in tracks:
        print(track)
