
from .config import AppConfig
from pytubefix import YouTube as YT
import requests 
from PyQt6.QtWidgets import QApplication
class YouTube:

    def download(url: str) -> None:
        """
        Download the video from the given URL.

        Args:
            url (str): The URL of the video.
        """

        yt = YT(url)
        
        yt.streams.first().download(AppConfig.DOWNLOAD_PATH)
        return yt.title

    def get_thumbnail(raw_url: str) -> str:
        # Check if 'v=' is in the URL
        if "v=" not in raw_url:
            return None
        
        video_id = raw_url.split("v=")[1]
        thumnail_url = "http://img.youtube.com/vi/%s/0.jpg" % video_id

        # https://noembed.com/embed?dataType=json&url=
        # Call above
        print(requests.get(f"https://noembed.com/embed?dataType=json&url={raw_url}").json())

        return thumnail_url

    # ? IF NEEDED - https://noembed.com/embed?dataType=json&url=
