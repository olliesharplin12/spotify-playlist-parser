from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.id3 import ID3

file_path = 'D:\\Music HDD\\WAVs\\The Launch - TREi Remix.wav'

# audio = WAVE('D:\\Music HDD\\WAVs\\The Launch - TREi Remix.wav', ID3=ID3)
# print(audio['TIT2'])  # Title
# print(audio['TPE1'])  # Artist


# import wave

# with wave.open('D:\\Music HDD\\WAVs\\The Launch - TREi Remix.wav', 'rb') as wav_file:
#     params = wav_file.getparams()
#     print(params)


# import mutagen

# # Load the WAV file
# audio = mutagen.File(file_path)

# # Print out the metadata
# if audio is not None:
#     for key, value in audio.items():
#         print(f"{key}: {value}")
# else:
#     print("No metadata found or file is not a supported format.")

import taglib

song = taglib.File(file_path)
print(song.tags)  # This will print out metadata, if available