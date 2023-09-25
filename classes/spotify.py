import spotipy
import spotipy.oauth2 as oauth2

from .track import Track
from config import CLIENT_ID, CLIENT_SECRET

FETCH_LIMIT = 50
PLAYLIST_FIELDS = "total,items(track(name,artists(name)))"

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
        
        return [Track(track["track"]["name"], [artist["name"] for artist in track["track"]["artists"]]) for track in tracks_json]


if __name__ == "__main__":
    test_playlist_uri = "https://open.spotify.com/playlist/2QTyeLQCrSXulLc9fSzdzv?si=0c6c01b178024ce7"
    playlist = SpotifyPlaylist(test_playlist_uri)
    tracks = playlist.get_tracks()
    for track in tracks:
        print(track)
