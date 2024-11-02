AMPERSAND = " & "

def joined_artist_match(artists_a, artists_b):
    for artist in artists_a:
        if AMPERSAND in artist:
            artists = artist.split(AMPERSAND)
            if all([artist.strip() in artists_b for artist in artists]):
                return True
    return False

class Track:
    def __init__(self, id: str, name: str, artists: list[str], raw_name: str, raw_artists: list[str]):
        self.id = id
        self.name = name
        self.artists = artists
        self.raw_name = raw_name
        self.raw_artists = raw_artists
    
    def formatted_string(self):
        return ", ".join(self.artists) + " - " + self.name
    
    def __str__(self):
        return ", ".join(self.raw_artists) + " - " + self.raw_name

    def __eq__(self, obj):
        def artist_overlap(artists_a: list[str], artists_b: list[str]) -> bool:
            a_lower = [artist.lower() for artist in artists_a]
            b_lower = [artist.lower() for artist in artists_b]
            return any([artist in b_lower for artist in a_lower]) \
                or joined_artist_match(a_lower, b_lower) \
                or joined_artist_match(b_lower, a_lower)
        return isinstance(obj, Track) and self.name.lower() == obj.name.lower() and artist_overlap(self.artists, obj.artists)

    def __lt__(self, other):
        return self.artists[0] < other.artists[0]
