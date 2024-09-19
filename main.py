import sys
import threading
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QPushButton, QVBoxLayout,
    QWidget, QScrollArea,
    QFileDialog, QCheckBox
)

from src.sequence.script import sequence, get_sequence_all_name
from src.sequence import Config


class CheckSequenceWidget(QCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def input(self, value: str):
        key, value = value.split('=')

        match key:
            case 'progress':
                print(value)

                text = self.text().split(' [')
                print(text)
                self.setText(text[0] + ' [' + value + ']')


class CheckBoxWidget(QWidget):
    def __init__(self, main):
        super().__init__()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self)
        self.scroll_area.setWidgetResizable(True)

        self.main = main
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            background-color: white;
        """)

    def finds(self):
        checkboxes: list[CheckSequenceWidget] = self.findChildren(CheckSequenceWidget)
        for checkbox in checkboxes:
            if checkbox.isChecked():
                self.main.run_sequence(checkbox)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        Config()

        self.setWindowTitle("Omoluzu Sequence")
        self.setGeometry(100, 100, 800, 600)

        self.select_folder = QPushButton("Выбрать папку")  # todo: Асинхранный выбор папки, а точнее анализа файлов в нем, так как он сейчас блокирует приложение
        self.select_folder.clicked.connect(self.open_folder_dialog)

        self.checkbox_widget = CheckBoxWidget(self)

        self.show_all_checkbox = QPushButton("RUN")
        self.show_all_checkbox.clicked.connect(self.checkbox_widget.finds)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.select_folder)
        self.layout.addWidget(self.checkbox_widget.scroll_area)
        self.layout.addWidget(self.show_all_checkbox)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_path:
            self.sequences = get_sequence_all_name(Path(folder_path))
            for name in self.sequences.names:
                checkbox = CheckSequenceWidget(name)
                self.checkbox_widget.layout.addWidget(checkbox)

    def run_sequence(self, sequence_name):
        thread = threading.Thread(
            target=sequence,
            args=(self.sequences.get_sequence(
                sequence_name.text()), sequence_name  # todo: В имя текста есть дополнительная информация [end] которая при повторном запуске не находит sequence
            )
        )
        thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
