from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Buttons


class Session(QWidget):
    """Holds all data and can be restarted to show changes."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.initUi()

    def initUi(self):
        """Ui generator."""
        pass
