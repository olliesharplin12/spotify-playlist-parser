import os
import taglib

from .track import Track


ALLOWED_FILE_EXTENSIONS = ["wav", "mp3"]

def filter_title(name):
    filters = ["-", "ft."]
    for filter in filters:
        if filter in name:
            name = name.split(filter)[0]
    return name.strip()

def filter_artists(artists: list[str]):
    filters = ["Remix"]
    filtered_artists = []
    for artist in artists:
        for filter in filters:
            if filter in artist:
                artist = artist.split(filter)[0]
        filtered_artists.append(artist.strip())
    return filtered_artists

class Rekordbox:
    def __init__(self, directory):
        self.directory = directory
    
    def get_tracks(self) -> list[Track]:
        tracks = []
        # i = 0
        for _, _, files in os.walk(self.directory):
            for file in files:
                extension = file.split(".")[-1]
                if extension not in ALLOWED_FILE_EXTENSIONS:
                    print("Warning: Invalid file extension {0} for {1}".format(extension, file))
                    continue

                properties = self.read_properties(file)
                if properties is None:
                    continue

                title, artists, raw_title, raw_artists = properties
                tracks.append(Track(file, title, artists, raw_title, raw_artists))
                # if i < 200:
                #     #if title is not None or artist is not None:
                #     print(title, artist)
                #     i += 1
                # else:
                #     break
        return tracks
    
    def read_properties(self, filename):
        file_path = os.path.join(self.directory, filename)
        tag_file = taglib.File(file_path)
        tags = tag_file.tags

        if 'ARTIST' not in tags:
            print(f"ERROR: Artist tag not found ({file_path} {tags})")
            return None
        
        if 'TITLE' not in tags:
            title = ".".join(filename.split(".")[:-1])
        else:
            title = tags['TITLE'][0]
            if len(tags['TITLE']) > 1:
                print(f"MORE THAN 1 TITLE: {tags['TITLE']}")
        
        filtered_title = filter_title(title)
        filtered_artists = filter_artists(tags['ARTIST'])
        return filtered_title, filtered_artists, title, tags['ARTIST']
 

if __name__ == "__main__":
    test_directory = "D:\\Music HDD\\WAVs"
    rekordbox = Rekordbox(test_directory)
    tracks = rekordbox.read_tracks()
