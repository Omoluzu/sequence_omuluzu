from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt

from src.sequence import widgets


class ShowCheckBoxWidget(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName('box')

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName('scroll_area')

        self.main = main
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.layout.setContentsMargins(3, 3, 3, 3)
        self.layout.setSpacing(3)

    def finds(self):
        checkboxes = self.findChildren(widgets.Sequence)
        for checkbox in checkboxes:
            if checkbox.isChecked():
                self.main.run_sequence(checkbox)

    def added_sequences(self, sequences):
        for name in sequences.names:
            checkbox = widgets.Sequence(
                main=self.main,
                sequence_info=sequences.get_sequence(name))
            self.layout.addWidget(checkbox)

        self.layout.addStretch()
