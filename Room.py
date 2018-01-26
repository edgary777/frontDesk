from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class RoomD(QWidget):
    """Data representation of a room."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.ID = None
        self.number = None
        self.type = None
        self.beds = None
        self.maxCapacity = None
        self.extras = None
        self.status = None
        self.notes


class RoomUi(QWidget):
    """Graphic representation of a room."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)
