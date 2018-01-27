from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from DataItems import DataItem


class RoomD(DataItem):
    """Data representation of a room."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.items = [
            "ID", "number", "type", "beds", "maxCapacity", "extras", "status",
            "notes"
        ]

        for item in self.items:
            setattr(self, item, None)



class RoomUi(QWidget):
    """Graphic representation of a room."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)
