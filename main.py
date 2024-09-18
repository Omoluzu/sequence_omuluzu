import sys
from pathlib import Path
import threading
from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QPushButton, QVBoxLayout,
    QWidget, QLabel,
    QFileDialog, QCheckBox
)

from src.sequence.script import sequence, get_sequence_all_name


class CheckBoxWidget(QWidget):
    def __init__(self, main):
        super().__init__()

        self.main = main
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def finds(self):
        checkboxes: list[QCheckBox] = self.findChildren(QCheckBox)
        for checkbox in checkboxes:
            if checkbox.isChecked():
                self.main.run_sequence(checkbox.text())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Omoluzu Sequence")

        self.select_folder = QPushButton("Выбрать папку")
        self.select_folder.clicked.connect(self.open_folder_dialog)

        self.checkbox_widget = CheckBoxWidget(self)

        self.show_all_checkbox = QPushButton("RUN")
        self.show_all_checkbox.clicked.connect(self.checkbox_widget.finds)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.select_folder)
        self.layout.addWidget(self.checkbox_widget)
        self.layout.addWidget(self.show_all_checkbox)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_path:
            self.sequences = get_sequence_all_name(Path(folder_path))
            for name in self.sequences.names:
                checkbox = QCheckBox(name)
                self.checkbox_widget.layout.addWidget(checkbox)

    def run_sequence(self, sequence_name):
        thread = threading.Thread(
            target=sequence,
            args=(self.sequences.get_sequence(sequence_name),)
        )
        thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
