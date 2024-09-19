import sys
import threading
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QFileDialog, QSplitter
)
from PySide6.QtCore import Qt

from src.sequence.script import sequence, get_sequence_all_name
from src.sequence import Config, widgets


class SequenceFileWidget(QWidget):
    def __init__(self, main):
        super().__init__()

        self.select_folder = QPushButton("Выбрать папку")
        self.select_folder.clicked.connect(main.open_folder_dialog)

        self.checkbox_widget = widgets.ShowCheckBox(main)

        self.show_all_checkbox = QPushButton("Выполнить секвенцию")
        self.show_all_checkbox.clicked.connect(self.checkbox_widget.finds)

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.select_folder)
        self.layout.addWidget(self.checkbox_widget.scroll_area)
        self.layout.addWidget(self.show_all_checkbox)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        Config()

        self.setWindowTitle("Omoluzu Sequence")
        self.setGeometry(100, 100, 1400, 600)

        self.file_widget = SequenceFileWidget(self)
        self.player_video = widgets.PlayVideo()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.file_widget)
        splitter.addWidget(self.player_video)

        self.general_layout = QHBoxLayout()
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
