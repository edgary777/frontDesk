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

    def __init__(self, Type, room, parent, reservation=None):
        """Init."""
        super().__init__(parent)

        self.type = Type
        try:
            if Type != 2 and reservation is None:
                raise AttributeError
        except AttributeError:
            print("DashItem")
            print(
                "You either forgot to pass a reservation or got the type wrong"
            )
            raise

        self.reservation = reservation
        self.room = room

        self.items = [
            "RoNumber", "RoStatus", "RoType", "RoAvailableExtras", "RoNotes",
            "RoMaxCap", "RoBeds", "ReName", "ReDateIn", "ReDateOut",
            "ReNights", "ReAdults", "ReMinors", "ReGroup", "ReExtras",
            "ReNotes", "ReTotal", "RePaid", "ReOwed"
        ]
        for item in self.items:
            setattr(self, item, None)

        self.init(Type)  # 0 == In, 1 == out, 2 == status

    def init(self, Type):
        """Init item."""
        # It may seem like CheckIn DashItem's shouldn't have an assigned number, but
        # room number is assigned the day the reservation is to be claimed, and Non-Status
        # dashboard items only appear on the dashboard the day they are needed,
        # so room numbers will have been assigned already and therefore it makes sense :).

        rsvData = self.reservation.getData()
        roomData = self.room.getData()

        self.RoNumber = roomData["number"]
        self.RoStatus = roomData["status"]
        self.RoType = roomData["type"]
        self.RoAvailableExtras = roomData["extras"]
        self.RoNotes = roomData["notes"]
        self.RoMaxCap = roomData["maxCapacity"]
        self.RoBeds = roomData["beds"]
        if Type == 0 or Type == 1:
            # Data for all reservations
            self.ReName = self.reservation.getGuestName()
            self.ReDateIn = rsvData["dateIn"]
            self.ReDateOut = rsvData["dateOut"]
            self.ReNights = self.reservation.getNights()
            self.ReAdults = rsvData["adults"]
            self.ReMinors = rsvData["minors"]
            self.ReGroup = rsvData["group"]
            self.ReExtras = rsvData["extras"]
            self.ReNotes = rsvData["notes"]
        if Type == 1:
            # Data for currently fulfilled reservations
            self.ReTotal = self.reservation.getTotal()
            self.RePaid = rsvData["paid"]
            self.ReOwed = self.reservation.getOwed()

    def getType(self):
        """Return the type of item.

        0 == In, 1 == out, 2 == status
        """
        return self.type

    def getData(self):
        """Return the item data as a dict.

        keys:
        type, roomNo, status, roomType, availableExtras, roomNotes,
        name, dateIn, dateOut, nights, adults, minors, group,
        requestedExtras, notes, total, paid, owed
        """
        data = {}
        for item in self.items:
            if not getattr(self, item) is None:
                data[item] = getattr(self, item)
        data["type"] = self.type
        return data
