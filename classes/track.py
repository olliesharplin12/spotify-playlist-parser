from typing import List

class Track:
    def __init__(self, name: str, artists: List[str]):
        self.name = name
        self.artists = artists

    def __eq__(self, obj):
        def artist_overlap(artists_a: List[str], artists_b: List[str]) -> bool:
            a_lower = [artist.lower() for artist in artists_a]
            b_lower = [artist.lower() for artist in artists_b]
            return any([artist for artist in a_lower if artist in b_lower])

        return isinstance(obj, Track) and self.name.lower() == obj.name.lower() and artist_overlap(self.artists, obj.artists)

    def __str__(self):
        return ", ".join(self.artists) + " - " + self.name
