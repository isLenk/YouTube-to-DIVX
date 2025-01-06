from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt6.QtCore import QTimer
import sys
from ..utils.youtube import YouTube

class DownloadWindow(QMainWindow):
    queue = set()

    def __init__(self, pending):
        super().__init__()
        self.queue = set(pending)
        self.initUI()
        self.download()

        # Close aplication when download is finished
        if len(self.queue) == 0:
            QTimer.singleShot(1000, QApplication.quit)

    def download(self):
        if len(self.queue) == 0: return

        piece = self.queue.pop()
        self.setCurrent(piece)
        YouTube.download(piece[1])

        QTimer.singleShot(1000, self.download)

    def initUI(self):
        self.setWindowTitle('Karaoke - Download Window')
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel('TITLE', self)
        self.label.setGeometry(10, 10, 200, 40)

        self.downloadingFromLabel = QLabel("Downloading:", self)
        self.downloadingFromLabel.setGeometry(10, 30, 200, 40)

        self.urlLabel = QLabel("https://youtube.com", self)
        self.urlLabel.setGeometry(10,50, 200, 40)

        self.show()

    def setCurrent(self, piece):
        self.label.setText(piece[0])
        self.urlLabel.setText(piece[1])