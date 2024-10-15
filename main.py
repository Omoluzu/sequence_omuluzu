__version__ = '1.0.0'
__author__ = 'Volkov Aleksey'

import os.path
import sys
import threading
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QPushButton, QVBoxLayout,
    QWidget, QFileDialog, QSplitter
)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QIcon, QPixmap

from src.sequence.script import sequence, get_sequence_all_name
from src.sequence import Config, widgets


class SequenceFileWidget(QWidget):
    def __init__(self, main):
        super().__init__()

        folder_icon = QIcon(
            QPixmap(os.path.join('src', 'sequence', 'style', 'folder.png'))
        )
        document_icon = QIcon(
            QPixmap(os.path.join('src', 'sequence', 'style', 'document.png'))
        )

        self.select_button = QPushButton("Выбрать папку")
        self.select_button.clicked.connect(main.open_folder_dialog)
        self.select_button.setIcon(folder_icon)
        self.select_button.setObjectName('select_button')

        self.checkbox_widget = widgets.ShowCheckBox(main)

        self.sequence_button = QPushButton("Собрать видео файл")
        self.sequence_button.clicked.connect(self.checkbox_widget.finds)
        self.sequence_button.setIcon(document_icon)
        self.sequence_button.setObjectName('sequence_button')

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.checkbox_widget.scroll_area)
        self.layout.addWidget(self.sequence_button)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        Config()

        self.setWindowTitle(f"Sequence (Волков Алексей) v.{__version__}")

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.title_bar = widgets.TitleBar(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setGeometry(100, 100, 1400, 600)
        self.setObjectName('central_widget')

        styles = os.path.join('src', 'sequence', 'style', 'style.css')
        with open(styles, 'r', encoding='utf-8') as styles_file:
            self.setStyleSheet(styles_file.read())

        self.file_widget = SequenceFileWidget(self)
        self.player_video = widgets.PlayVideo()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.file_widget)
        splitter.addWidget(self.player_video)

        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.addWidget(self.title_bar)
        self.general_layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(self.general_layout)
        self.setCentralWidget(container)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_path:
            try:
                self.sequences = get_sequence_all_name(Path(folder_path))
            except OSError as err:
                show_error_message(str(err))
            else:
                self.file_widget.checkbox_widget.added_sequences(self.sequences)

    def run_sequence(self, sequence_widget):
        thread = threading.Thread(
            target=sequence,
            args=(self.sequences.get_sequence(
                sequence_widget.text()), sequence_widget
            )
        )
        thread.start()

    def changeEvent(self, event: QEvent) -> None:
        """Overriding the trigger for changing the main application window
        :param event: intercepted event"""
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()


def show_error_message(err):
    msg = QMessageBox()
    msg.setWindowTitle("Ошибка")
    msg.setText(err)
    msg.setIcon(QMessageBox.Critical)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
