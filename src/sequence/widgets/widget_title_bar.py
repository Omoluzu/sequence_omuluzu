from PySide6.QtGui import QPalette, QMouseEvent
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QLabel,
    QStyle,
    QWidget,
    QHBoxLayout,
    QToolButton,
    QMainWindow,
)


class WidgetTitleBar(QWidget):
    """Class that defines the top bar of the application"""

    def __init__(self, main: QMainWindow):
        super().__init__(main)
        self.setMaximumHeight(28)
        self.main = main
        self.setBackgroundRole(QPalette.ColorRole.Highlight)
        self.initial_pos = None
        self.title_bar_layout = QHBoxLayout(self)
        self.title_bar_layout.setContentsMargins(1, 1, 1, 1)
        self.title_bar_layout.setSpacing(2)

        self._set_title_bar_title()
        self._set_buttons()

    def _set_title_bar_title(self) -> None:
        """Setting the name of the application"""
        self.title = QLabel(self.main.windowTitle())
        self.title.setObjectName('title_widget')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_bar_layout.addWidget(self.title)

    def _set_buttons(self) -> None:
        """Setting up application window control buttons"""
        self.min_button = QToolButton(self)
        min_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMinButton
        )
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        self.max_button = QToolButton(self)
        max_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMaxButton
        )
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)

        self.close_button = QToolButton(self)
        close_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarCloseButton
        )
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        self.normal_button = QToolButton(self)
        normal_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarNormalButton
        )
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(28, 28))
            button.setObjectName("title_buttons")
            self.title_bar_layout.addWidget(button)

    def window_state_changed(self, state: Qt.WindowState) -> None:
        """Overriding the Window Status Change Method
        :param state: Changed status"""
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Overriding the method for intercepting the LMB click event
        :param event: intercepted event"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Overriding the method for intercepting the mouse cursor movement
        event
        :param event: intercepted event"""
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Overriding the method for intercepting the LMB press end event
        :param event: intercepted event"""
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()
