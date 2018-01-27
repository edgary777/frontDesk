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
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.area = QScrollArea()

        # This must be done so it can update dynamically
        self.area.setWidgetResizable(True)

        layout.addWidget(self.area)
        self.setLayout(layout)

    def setScrollItem(self, item):
        """Set the item for the scroll area."""
        self.area.setWidget(item)


class DashList(QWidget):
    """Dashboard items list."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.items = []

        self.initUi()

    def initUi(self):
        """Ui setup."""
        pass

    def addItem(self):
        """Add an item."""
        pass

    def removeItem(self):
        """Remove an item."""
        pass

    def addMultiple(self):
        """Add multiple items."""
        pass

    def removeMultiple(self):
        """Remove multiple items."""
        pass

    def modifyItem(self):
        """Modify an item."""
        pass

    def cleanUi(self):
        """Remove all items from the layout."""
        pass

    def fillUi(self):
        """Add all items in the items list to the layout."""
        pass

    def updateUi(self):
        """Update the Ui."""
        pass


class DashItemUi(QWidget):
    """Dashboard item graphic representation."""

    def __init__(self, parent, complex=False):
        """Init."""
        super().__init__(parent)

        self.initUi()

    def IOUi(self):
        """Check-In and Check-Out Ui setup."""
        # No de cuarto, nombre, No de noches, fecha de entrada, fecha de salida
        pass

    def statusUi(self):
        """Room status Ui setup."""
        # No de cuarto, fecha de entrada, fecha de salida, status
        pass


class DashItem(QWidget):
    """Dashboard item data representation."""

    def __init__(self, parent, room=None, reservation=None):
        """Init."""
        super().__init__(parent)

        self.reservation = reservation
        self.room = room
