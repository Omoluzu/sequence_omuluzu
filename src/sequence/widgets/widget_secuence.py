import os

from PySide6.QtWidgets import QWidget, QCheckBox, QPushButton, QHBoxLayout
from PySide6.QtCore import QUrl

from src.sequence import Config, SequenceInfo


class SequenceWidget(QWidget):
    def __init__(self, main, sequence_info: SequenceInfo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main
        self.sequence_info = sequence_info

        self.check = QCheckBox(sequence_info.regular)

        self.play = QPushButton('play')
        self.play.clicked.connect(self.action_play_video)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.check)

        if os.path.exists(self.path_video):
            self.layout.addWidget(self.play)

    @property
    def path_video(self):
        return os.path.join(
            str(Config.output_path), self.sequence_info.output_name)

    def isChecked(self):
        return self.check.isChecked()

    def text(self):
        return self.check.text()

    def input(self, value: str):
        key, value = value.split('=')

        match key:
            case 'progress':
                text = self.text().split(' [')
                self.check.setText(text[0] + ' [' + value + ']')
                if value == 'end':
                    self.layout.addWidget(self.play)

    def action_play_video(self):
        video_file = self.path_video
        self.main.player_video.player.setSource(QUrl.fromLocalFile(video_file))
        self.main.player_video.player.play()
