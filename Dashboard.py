from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DashScroll(QWidget):
    """Dashboard scroll area."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.initUi()

        self.list = DashList(self)
        self.setScrollItem(self.list)

    def initUi(self):
        """Ui setup."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.area = QScrollArea()
        self.area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # This must be done so it can update dynamically
        self.area.setWidgetResizable(True)

        layout.addWidget(self.area)
        self.setLayout(layout)

    def setScrollItem(self, item):
        """Set the item for the scroll area."""
        self.area.setWidget(item)

    def getList(self):
        """Return it's DashList."""
        return self.list


class DashList(QWidget):
    """Dashboard items list."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.items = []

        self.initUi()

    def initUi(self):
        """Ui setup."""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def addItems(self,items):
        """Add an item."""
        for item in items:
            self.items.append(item)
        self.updateUi()

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
        for i in reversed(range(self.layout.count())):
            if i > 0:
                ob = self.layout.takeAt(i).widget()
                ob.setParent(None)
                ob.deleteLater()

    def fillUi(self):
        """Add all items in the items list to the layout."""
        for item in self.items:
            uiItem = DashItemUi(item, self)
            self.layout.addWidget(uiItem)

    def updateUi(self):
        """Update the Ui."""
        self.cleanUi()

        self.fillUi()


class DashItemUi(QWidget):
    """Dashboard item graphic representation."""

    def __init__(self, dashItem, parent):
        """Init."""
        super().__init__(parent)

        self.dItem = dashItem.getData()

        if dashItem.getType() != 2:
            self.IOUi()
        else:
            self.statusUi()

    def IOUi(self):
        """Check-In and Check-Out Ui setup."""
        # No de cuarto, nombre, No de noches, fecha de entrada, fecha de salida
        pass

    def statusUi(self):
        """Room status Ui setup."""
        items = {
            "number": (0, 0, 2, 1, "RoNumber"),
            "status": (0, 1, 1, 1, "RoStatus"),
            "type": (1, 1, 1, 1, "RoType"),
            "beds": (0, 3, 1, 1, "RoBeds"),
            "max": (0, 4, 1, 1, "RoMaxCap")
        }

        layout = QGridLayout()

        for key, value in items.items():
            setattr(self, key + "Label", QLabel(str(self.dItem[value[4]])))
            layout.addWidget(
                getattr(self, key + "Label"), value[0], value[1], value[2],
                value[3])

        if not self.dItem["RoNotes"] is None:
            pixmap = QPixmap("Resources/note.png").scaled(40, 40, Qt.KeepAspectRatio)
            self.notesIcon = QLabel()
            self.notesIcon.setPixmap(pixmap)
            layout.addWidget(self.notesIcon, 0, 2, 2, 1)
        else:
            self.notesIcon = QSpacerItem(20, 20)
            layout.addWidget(self.notesIcon, 0, 2, 2, 1)

        self.extras = self.extrasIcons(self.dItem["RoExtras"])
        layout.addLayout(self.extras, 1, 3, 1, 2)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 5)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)

        self.setLayout(layout)

    def extrasIcons(self, extras):
        """Return a layout with the icons of the extras passed."""
        layout = QHBoxLayout()
        for i in range(5):
            pixmap = QPixmap("Resources/ac.png").scaled(20, 20, Qt.KeepAspectRatio)
            icon = QLabel()
            icon.setPixmap(pixmap)
            layout.addWidget(icon)
        return layout

    def paintEvent(self, event):
        """Set window background color."""
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(p)


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
            "RoExtras", "RoMaxCap", "RoBeds", "ReName", "ReDateIn",
            "ReDateOut", "ReNights", "ReAdults", "ReMinors", "ReGroup",
            "ReExtras", "ReNotes", "ReTotal", "RePaid", "ReOwed"
        ]

        self.init(Type)  # 0 == In, 1 == out, 2 == status

    def init(self, Type):
        """Init item."""
        # It may seem like CheckIn DashItem's shouldn't have an assigned number, but
        # room number is assigned the day the reservation is to be claimed, and Non-Status
        # dashboard items only appear on the dashboard the day they are needed,
        # so room numbers will have been assigned already and therefore it makes sense :).

        roomData = self.room.getData()

        self.RoNumber = roomData["number"]
        self.RoStatus = roomData["status"]
        self.RoType = roomData["type"]
        self.RoAvailableExtras = roomData["extras"]
        self.RoNotes = roomData["notes"]
        self.RoMaxCap = roomData["maxCapacity"]
        self.RoBeds = roomData["beds"]
        self.RoExtras = roomData["extras"]
        if Type == 0 or Type == 1:
            # Data for all reservations
            rsvData = self.reservation.getData()
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
            try:
                if not getattr(self, item) is None:
                    data[item] = getattr(self, item)
            except AttributeError:
                pass
        data["type"] = self.type
        return data
