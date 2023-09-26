import os
import music_tag

ALLOWED_FILE_EXTENSIONS = ["wav", "mp3"]

class Wav:
    def __init__(self, directory):
        self.directory = directory
    
    def read_tracks(self):
        tracks = []
        i = 0
        for _, _, files in os.walk(self.directory):
            for file in files:
                extension = file.split(".")[-1]
                if extension not in ALLOWED_FILE_EXTENSIONS:
                    print("Warning: Invalid file extension {0} for {1}".format(extension, file))
                    continue

                properties = self.read_properties(file)
                if properties is None:
                    print("Warning: Unsupported format error for {0}".format(file))
                    continue

                title, artist = properties
                # tracks.append(Trac)
                if i < 200:
                    if title is not None or artist is not None:
                        print(file, title, artist)
                    i += 1
                else:
                    break
    
    def read_properties(self, filename):
        file_path = os.path.join(self.directory, filename)
        try:
            file = music_tag.load_file(file_path)
            title = file['title'].first
            artist = file['artist'].first
            return title, artist
        except music_tag.UnsupportedFormatError:
            return None
 

if __name__ == "__main__":
    test_directory = "D:\\Music HDD\\WAVs"
    wav = Wav(test_directory)
    tracks = wav.read_tracks()
