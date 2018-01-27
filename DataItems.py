from PyQt5.QtWidgets import *


class DataItem(QWidget):
    """Data representation of object."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

    def setData(self, data):
        """Parse the data and assign it to variables."""
        for key, value in data.items():
            if key in self.items:
                setattr(self, key, data[key])

    def getData(self):
        """Return the reservation data as a dict."""
        data = {}
        for item in self.items:
            data[item] = getattr(self, item)
        return data
