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

        self.delete = QPushButton('deleted')
        self.delete.clicked.connect(self.action_deleted_video)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.check)
        self.layout.addWidget(self.play)
        self.layout.addWidget(self.delete)

        if not os.path.exists(self.path_video):
            self.play.hide()
            self.delete.hide()

    @property
    def path_video(self) -> str:
        """Path to save current video"""
        return os.path.join(
            str(Config.output_path), self.sequence_info.output_name)

    def isChecked(self) -> bool:
        """Abstract to isChecked QCheckBox
        :return: state checking QCheckBox"""
        return self.check.isChecked()

    def text(self) -> str:
        """Abstract to text QCheckBox
        :return: text to QCheckBox"""
        return self.check.text()

    def input(self, value: str) -> None:
        """Input Adapter for sequence file
        :param value: output command"""
        key, value = value.split('=')

        match key:
            case 'progress':
                text = self.text().split(' [')
                self.check.setText(text[0] + ' [' + value + ']')
                if value == 'end':
                    self.play.show()
                    self.delete.show()

    def action_play_video(self) -> None:
        """Play video to VideoWidget"""
        self.main.player_video.player.setSource(
            QUrl.fromLocalFile(self.path_video))

        self.main.player_video.player.play()

    def action_deleted_video(self) -> None:
        """Deleted video of file system"""
        os.remove(self.path_video)
        self.play.hide()
        self.delete.hide()
