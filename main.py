import sys
import threading
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QFileDialog
)

from src.sequence.script import sequence, get_sequence_all_name
from src.sequence import Config, widgets


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        Config()

        self.setWindowTitle("Omoluzu Sequence")
        self.setGeometry(100, 100, 1400, 600)

        self.select_folder = QPushButton("Выбрать папку")
        self.select_folder.clicked.connect(self.open_folder_dialog)

        self.checkbox_widget = widgets.ShowCheckBox(self)

        self.show_all_checkbox = QPushButton("RUN")
        self.show_all_checkbox.clicked.connect(self.checkbox_widget.finds)

        self.player_video = widgets.PlayVideo()

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.select_folder)
        self.layout.addWidget(self.checkbox_widget.scroll_area)
        self.layout.addWidget(self.show_all_checkbox)

        self.general_layout = QHBoxLayout()
        self.general_layout.addLayout(self.layout)
        self.general_layout.addWidget(self.player_video)

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
                self.checkbox_widget.added_sequences(self.sequences)

    def run_sequence(self, sequence_name):
        thread = threading.Thread(
            target=sequence,
            args=(self.sequences.get_sequence(
                sequence_name.text()), sequence_name  # todo: В имя текста есть дополнительная информация [end] которая при повторном запуске не находит sequence
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
