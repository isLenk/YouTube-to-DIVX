''' app/ui/main_window.py '''
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTextEdit, QPushButton, QLabel
from ..utils.config import AppConfig
from .widgets.songlistbox import SongListBox
from ..utils.youtube import YouTube
from .widgets.USBSelect import USBSelect
from .widgets.KaraokeSelect import KaraokeSelect
from PyQt6.QtGui import QPixmap, QImage
import requests
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout
from pathlib import Path
from ..utils.ffmpeg import FFmpeg
import subprocess
from time import sleep


# Uploaded karaoke songs start at this index
STARTING_NUMBER = 85000

class MainWindow(QMainWindow):
    """
    MainWindow

    Args:
        QMainWindow (QMainWindow): Inheritance
    """

    def __init__(self) -> None:
        """
        Initialize the Main-Window.
        """
        super().__init__()

        # Window-Settings
        self.setWindowTitle(AppConfig.APP_NAME)
        self.setGeometry(100, 100, 1280, 600)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        central_widget.setLayout(layout)


        # Vertically Align to top
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Horizontal Align to center
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Create a textbox labelled 'youtube link'
        self.youtube_link = QTextEdit(self)
        self.youtube_link.setPlaceholderText("Enter YouTube link here")
        self.youtube_link.setFixedHeight(30)

        # Create a download button beside it
        self.download_button = QPushButton("Download", self)
        self.download_button.setFixedHeight(30)

        #  Create a button to convert the mp4 to divx
        self.convert_button = QPushButton("Convert", self)
        self.convert_button.setFixedHeight(30)

        self.create_songbook_button = QPushButton("Generate Songbook", self)
        self.create_songbook_button.setFixedHeight(30)

        self.thumbnail = QLabel(self)

        # Create a listbox to display the songs
        self.song_list = SongListBox(self, songbook_path = AppConfig.SONGBOOK_PATH)

        # Add USBSelect widget
        # self.usb_select = USBSelect(self)
        self.karaoke_devices = KaraokeSelect(self)
        
        # Add widgets to the layout
        # layout.addWidget(self.usb_select, 2, 0, 1, 2)
        
        # Put a black border around thumbnail
        self.thumbnail.setStyleSheet("background-color: rgb(50,50,50);")
        # Set width to 480
        self.thumbnail.setFixedWidth(480)
        # First column
        layout.addWidget(self.youtube_link, 0, 0, 1, 1)
        layout.addWidget(self.download_button, 0, 1, 1, 1)
        layout.addWidget(self.song_list, 2, 0, 1, 1)

        # Second Column
        layout.addWidget(self.thumbnail, 2, 1, 1, 1)

        # Bottom Row
        layout.addWidget(self.karaoke_devices, 3, 0, 1, 1)
        layout.addWidget(self.create_songbook_button, 3, 1, 1, 1)
        layout.addWidget(self.convert_button, 3, 2, 1, 1)
        # Make listbox be on the second column and fill the entire column
        # Bind functions
        self.download_button.clicked.connect(self.on_download_button_clicked)
        self.youtube_link.textChanged.connect(self.on_textbox_input_changed)
        self.convert_button.clicked.connect(self.on_convert_button_clicked)
        self.create_songbook_button.clicked.connect(self.generate_songbook)

        self.song_list.load_songs()

    def set_thumbnail(self, url):
        """
        Set the thumbnail image of the video.

        Args:
            url (str): The URL of the thumbnail image.
        """

        if not url:
            self.thumbnail.clear()
            return 
        
        thumbnail_url = YouTube.get_thumbnail(url)
        if not thumbnail_url:
            # Clear the thumbnail if the URL is invalid
            self.thumbnail.clear()
            return
        image = QImage()
        image.loadFromData(requests.get(thumbnail_url).content)
        self.thumbnail.setPixmap(QPixmap(image))

    def on_textbox_input_changed(self):
        """
        Called when the user finishes typing in the textbox.
        """
        
        # Get the text from the textbox
        url = self.youtube_link.toPlainText()
        self.set_thumbnail(url)

    def on_download_button_clicked(self):
        """
        Called when the user clicks the download button.
        """

        url = self.youtube_link.toPlainText()
        title = YouTube.download(url)
        if not title:
            return
        
        self.song_list.add_song(title, url, save=True)
        self.youtube_link.clear()


    def on_convert_button_clicked(self):
        """
        Called when the user clicks the convert button.
        """
        
        # List all the files in AppConfig.DOWNLOAD_PATH

        download_path = AppConfig.DOWNLOAD_PATH
        # Open the file
        download_path = Path(download_path)

        files = [f for f in download_path.iterdir() if f.is_file()]

        # Check if there are any files to convert
        if not files:
            return
        
        # Delete files in the output directory
        divx_folder = download_path / 'divx'
        for file in divx_folder.iterdir():
            file.unlink()

        


        sleep(1)
        
        for file in files:
            file_with_divx_ext = file.with_suffix('.avi')
            # Put it into 'divx' folder
            divx_folder = download_path / 'divx'
            divx_folder.mkdir(exist_ok=True)
            file_with_divx_ext = divx_folder / file_with_divx_ext.name

            # Use ffmpeg to convert the file
            ffmpeg = FFmpeg(file, file_with_divx_ext)
            ffmpeg.convert_mp4_to_divx(
                self.karaoke_devices.get())
        print("Conversion complete")

    def generate_songbook(self):
        """
        Generate the songbook.
        Uses the files in the DOWNLOAD_PATH/divx folder.
        """

        download_path = AppConfig.DOWNLOAD_PATH
        download_path = Path(download_path)
        divx_folder = download_path / 'divx'

        # Check if the divx folder exists
        if not divx_folder.exists():
            return
        

        # List all the files in the divx folder(no ext)
        files = [f.with_suffix('').name for f in divx_folder.iterdir() if f.is_file()]
        files.sort()
        
        songbook = []
        for index, file in enumerate(files):
            songbook.append(f"{STARTING_NUMBER + index},{file}\n")

        # Write the songbook to the file
        songbook_path = AppConfig.SONGBOOK_PATH
        songbook_path = Path(songbook_path)
        songbook_path = songbook_path.with_suffix('.csv')

        with open(songbook_path, 'w') as f:
            f.writelines(songbook)

        print("Generated songbook.csv")