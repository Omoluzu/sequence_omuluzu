import os

from PySide6.QtWidgets import QWidget, QCheckBox, QPushButton, QHBoxLayout
from PySide6.QtCore import QUrl, Qt

from src.sequence import Config, SequenceInfo


class SequenceWidget(QWidget):
    def __init__(self, main, sequence_info: SequenceInfo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main
        self.sequence_info = sequence_info

        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName('sequence_widget')
        self.setFixedHeight(40)

        self.check = QCheckBox(sequence_info.regular)
        self.check.setObjectName('sequence_checkbox')

        self.play = QPushButton()
        self.play.clicked.connect(self.action_play_video)
        self.play.setFixedSize(30, 30)
        self.play.setObjectName('play_button')

        self.delete = QPushButton()
        self.delete.clicked.connect(self.action_deleted_video)
        self.delete.setFixedSize(30, 30)
        self.delete.setObjectName('deleted_button')

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.check)
        self.layout.addWidget(self.play)
        self.layout.addWidget(self.delete)

        self.setLayout(self.layout)

        self.layout.setContentsMargins(3, 3, 3, 3)
        self.layout.setSpacing(3)

        if not os.path.exists(self.path_video):
            self.play.hide()
            self.delete.hide()
        else:
            self.check.setDisabled(True)

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

        match key, value:
            case 'progress', 'end':
                text = self.text().split(' [')
                self.play.show()
                self.delete.show()
                self.check.setText(text[0])
            case 'progress', 'continue':
                text = self.text().split(' [')
                self.check.setText(text[0] + ' [in process]')
                self.check.setDisabled(True)
                self.check.setChecked(False)

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
        self.check.setDisabled(False)
