from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class RoomD(QWidget):
    """Data representation of a room."""

    def __init__(self, data, parent):
        """Init."""
        super().__init__(parent)

        self.data = data

        self.items = [
            "ID", "number", "type", "beds", "maxCapacity", "extras", "status",
            "notes"
        ]

        for item in self.items:
            setattr(self, item, None)

    def setData(self):
        """Parse the data and assign it to variables.

        Data must be a dict with this keys:
        ID, number, type beds, maxCapacity, extras, status, notes

        notes is the only one that can be empty.
        """
        for key, value in self.data.items():
            setattr(self, key, value)

    def getData(self):
        """Return the reservation data as a dict.

        keys:
        ID, number, type beds, maxCapacity, extras, status, notes
        """
        data = {}
        for item in self.items:
            data[item] = getattr(self, item)
        return data


class RoomUi(QWidget):
    """Graphic representation of a room."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)
