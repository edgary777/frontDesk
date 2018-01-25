from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DashScroll(QWidget):
    """Dashboard scroll area."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.initUi()

    def initUi(self):
        """Ui setup."""
        pass


class DashList(QWidget):
    """Dashboard items list."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.initUi()

    def initUi(self):
        """Ui setup."""
        pass


class DashItemUi(QWidget):
    """Dashboard item graphic representation."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.initUi()

    def initUi(self):
        """Ui setup."""
        pass


class DashItem(object):
    """Dashboard item data representation."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)
