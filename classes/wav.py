import os

class Wav:
    def __init__(self, directory):
        self.directory = directory
    
    def read_songs(self):
        computer_songs = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                computer_songs.append(os.path.join(root, file))
