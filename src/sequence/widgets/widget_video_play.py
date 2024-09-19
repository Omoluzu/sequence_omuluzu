from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget


class PlayVideoWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(400, self.height())

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.video_widget = QVideoWidget()

        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)

        self.setLayout(layout)
