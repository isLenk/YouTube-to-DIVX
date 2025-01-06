''' app/utils/config.py '''


class AppConfig:
    """
    Configuration File
    """
    APP_NAME: str = "Premier98i Karaoke Downloader"
    SONGBOOK_PATH: str = "songbook.txt"
    DOWNLOAD_PATH: str = "downloads"
    
    @classmethod
    def initialize(cls) -> None:
        """
        Perform any necessary initializations here, e.g.:
        - Loading settings from a file
        """
    def get_var(self) -> None:
        """
        Get the Var.
        """