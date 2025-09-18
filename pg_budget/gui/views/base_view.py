"""BaseView"""

from PySide6.QtWidgets import QWidget, QVBoxLayout


class BaseView(QWidget):
    """class Base for View"""

    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(20, 20, 20, 20)
        self._layout.setSpacing(20)
        self.setLayout(self._layout)

        self._init()

    def _init(self):
        """init override"""

    def load(self):
        """load override"""
        raise NotImplementedError
