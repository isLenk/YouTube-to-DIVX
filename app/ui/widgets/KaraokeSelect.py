
from PyQt6.QtWidgets import QComboBox

# Access from ../..utils
from ...utils.ffmpeg import FFmpeg

class KaraokeSelect(QComboBox):
    def __init__(self, parent=None):
        super(KaraokeSelect, self).__init__(parent)
        
        self.addItems(FFmpeg.get_devices())
        self.currentIndexChanged.connect(self.onKaraokeSelect)

    def onKaraokeSelect(self, index):
        print(self.itemText(index))


    def get(self):
        return self.currentText()