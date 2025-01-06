# Ensures the songbook is consistent with the songs downloaded and converted.
import requests
from pathlib import Path
from .config import AppConfig



class Validator:
    def __init__(self, song_list):
        self.song_list = song_list

    def list_missing_downloads(self):
        """Returns a list of songs that are present in the songbook but not in the download folder."""

        download_path = AppConfig.DOWNLOAD_PATH
        download_path = Path(download_path)
        divx_folder = download_path / 'divx'

        # Check if the divx folder exists
        if not divx_folder.exists():
            return self.song_list

        # List all the files in the divx folder(no ext)
        files = [f.with_suffix('').name for f in divx_folder.iterdir() if f.is_file()]
        files.sort()

        missing = []
        for song in self.song_list:
            if song[0] not in files:
                missing.append(song)

        return missing
    
    def list_missing_songbook(self):
        """Returns a list of songs that are present in the download folder but not in the songbook."""

        download_path = AppConfig.DOWNLOAD_PATH
        download_path = Path(download_path)
        divx_folder = download_path / 'divx'

        # Check if the divx folder exists
        if not divx_folder.exists():
            return []

        # List all the files in the divx folder(no ext)
        files = [f.with_suffix('').name for f in divx_folder.iterdir() if f.is_file()]
        files.sort()

        missing = []
        for file in files:
            found = False
            for song in self.song_list:
                if song[0] == file:
                    found = True
                    break
            if not found:
                missing.append(file)

        return missing