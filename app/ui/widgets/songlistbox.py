from PyQt6.QtWidgets import QListWidget, QMenu
from PyQt6.QtCore import Qt
import os

class SongListBox(QListWidget):
    def __init__(self, parent, songbook_path):
        super().__init__(parent)
        self.parent = parent
        self.songbook_path = songbook_path
        # Right click to remove song
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.itemClicked.connect(self.on_item_clicked)

    def add_song(self, song, url, save=False):
        self.insertItem(self.count(), song)
        # Add to the songbook file

        if save:
            print("Saving song: ", song)
            with open(self.songbook_path, "a") as file:
                file.write(f"{song}|URL={url}\n")

    def on_item_clicked(self, item):
        print("Item clicked:", item.text())
        # Get the URL of the song
        url = self.get_song_url(item.text())
        # Set the thumbnail
        print(url)
        self.parent.set_thumbnail(url)


    def get_song_url(self, song_name):
        songbook_path = self.songbook_path
        with open(songbook_path, "r") as file:
            for line in file:
                try:
                    song, url = line.strip().split("|URL=")
                    if song == song_name:
                        return url
                except ValueError:
                    pass
        return None

    def show_context_menu(self, position):
        menu = QMenu(self)
        remove_action = menu.addAction("Remove")
        action = menu.exec(self.mapToGlobal(position))
        if action == remove_action:
            item = self.itemAt(position)
            if item:
                self.remove_song(item)

    def remove_song(self, song):
        self.takeItem(self.row(song))
        # Remove from the songbook file
        song_name = song.text()
        songbook_path = self.songbook_path
        with open(songbook_path, "r") as file:
            lines = file.readlines()
    
        with open(songbook_path, "w") as file:
            removed_one = False
            for line in lines:
                try:
                    song, url = line.strip().split("|URL=")
                    if song != song_name or removed_one:
                        file.write(line)
                    
                    if song == song_name:
                        removed_one = True
                        
                except ValueError:
                    pass

    def load_songs(self):
        """
        Load the songs from the database.
        """
        songbook_path = self.songbook_path
        # Read the songs from the songbook file
        songs = []
        # If file does not exist, create it
        if not os.path.exists(songbook_path):
            with open(songbook_path, "w") as file:
                pass
    
        with open(songbook_path, "r") as file:
            for line in file:
                songs.append(line.strip().split("|URL="))

        for song in songs:
            song_name, song_url, *_ = song

            self.add_song(song_name, song_url, save=False)