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

    def addItems(self, items):
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
        self.layout.addStretch()

    def updateUi(self):
        """Update the Ui."""
        self.cleanUi()

        self.fillUi()


class DashItemUi(QWidget):
    """Dashboard item graphic representation."""

    def __init__(self, dashItem, parent):
        """Init."""
        super().__init__(parent)

        # dash Item
        self.dashItem = dashItem
        # dash Item data
        self.dItem = dashItem.getData()

        if dashItem.getType() != 2:
            self.IOUi()
        else:
            self.statusUi()
        self.setFixedHeight(60)

    def IOUi(self):
        """Check-In and Check-Out Ui setup."""
        if self.dashItem.getMulti() is False:
            self.singleRoomUi()
        else:
            self.multiRoomUi()

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

        # Note Icon setup
        self.noteIcon(self.dashItem.gotNote("ro"), 2, layout)

        self.extras = self.extrasIcons(self.dItem["RoExtras"])
        layout.addLayout(self.extras, 1, 3, 1, 2)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 5)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)

        self.setLayout(layout)

    def singleRoomItems(self):
        """Return items for single room reservation."""
        items = None
        if self.dashItem.getType() == 0:
            # This is for checkins
            items = {
                "number": (0, 0, 2, 1, "RoNumber"),
                "name": (0, 1, 1, 1, "ReName"),
                "status": (0, 2, 2, 1, "RoStatus"),
                "group": (0, 4, 1, 1, "ReGroup"),
                "nights": (1, 4, 1, 1, "ReNights")
            }
        else:
            # This is for checkouts
            items = {
                "number": (0, 0, 2, 1, "RoNumber"),
                "name": (0, 1, 1, 1, "ReName"),
                "group": (1, 1, 1, 1, "ReGroup"),
                "status": (0, 2, 2, 1, "RoStatus"),
                "total": (0, 4, 2, 1, "ReTotal"),
                "owed": (0, 5, 2, 1, "ReOwed")
            }
        return items

    def singleRoomUi(self):
        """Return layout for single room reservations."""
        layout = QGridLayout()

        items = self.singleRoomItems()

        # Labels from items
        for key, value in items.items():
            setattr(self, key + "Label", QLabel(str(self.dItem[value[4]])))
            layout.addWidget(
                getattr(self, key + "Label"), value[0], value[1], value[2],
                value[3])

        # Note Icon setup
        self.noteIcon(self.dashItem.gotNote("re"), 3, layout)

        # Guest Icons setup
        if self.dashItem.getType() == 0:
            guestsIcons = self.guestsIcon(20, self.dItem["ReAdults"],
                                          self.dItem["ReMinors"])
            layout.addLayout(guestsIcons, 1, 1, 1, 1)

            self.extras = self.extrasIcons(self.dItem["ReExtras"])
            layout.addLayout(self.extras, 0, 5, 1, 2)

        # Layout setup
        self.setLayout(layout)

    def multiRoomUi(self):
        """Multi room Ui setup."""
        layout = QGridLayout()
        items = {
            "name": (0, 1, 1, 1, "ReName"),
            "group": (1, 1, 1, 1, "ReGroup")
        }

        # Labels from items
        for key, value in items.items():
            setattr(self, key + "Label", QLabel(str(self.dItem[value[4]])))
            layout.addWidget(
                getattr(self, key + "Label"), value[0], value[1], value[2],
                value[3])

        # Multi-Room room number
        rooms = self.dashItem.getMulti()
        roomsLabel = QLabel("M" + str(rooms))

        layout.addWidget(roomsLabel, 0, 0, 2, 1)

        # Note Icon setup
        self.noteIcon(self.dashItem.gotNote("re"), 1, layout)

        # Guest Icons setup
        if self.dashItem.getType() == 0:
            guestsIcons = self.guestsIcon(40, self.dItem["ReAdults"],
                                          self.dItem["ReMinors"])
            layout.addLayout(guestsIcons, 0, 3, 2, 1)

        self.setLayout(layout)

    def guestsIcon(self, size, adults, minors):
        """Return a layout with the adults and minors icon and number."""
        layout = QHBoxLayout()

        pixmap = QPixmap("Resources/ac.png").scaled(size, size,
                                                    Qt.KeepAspectRatio)
        adultIcon = QLabel()
        adultIcon.setPixmap(pixmap)
        layout.addWidget(adultIcon)
        adultLabel = QLabel(str(adults))
        layout.addWidget(adultLabel)

        pixmap = QPixmap("Resources/ac.png").scaled(size, size,
                                                    Qt.KeepAspectRatio)
        minorIcon = QLabel()
        minorIcon.setPixmap(pixmap)
        layout.addWidget(minorIcon)
        minorLabel = QLabel(str(minors))
        layout.addWidget(minorLabel)

        return layout

    def noteIcon(self, status, place, layout):
        """Return notes icon if status is True."""
        if status is True:
            pixmap = QPixmap("Resources/note.png").scaled(
                40, 40, Qt.KeepAspectRatio)
            notesIcon = QLabel()
            notesIcon.setPixmap(pixmap)
        else:
            pixmap = QPixmap().scaled(40, 40, Qt.KeepAspectRatio)
            notesIcon = QLabel()
            notesIcon.setPixmap(pixmap)
        layout.addWidget(notesIcon, 0, place, 2, 1)

    def extrasIcons(self, extras):
        """Return a layout with the icons of the extras passed."""
        layout = QHBoxLayout()
        for i in range(len(extras)):
            pixmap = QPixmap("Resources/extra_{}.png".format(i)).scaled(
                20, 20, Qt.KeepAspectRatio)
            icon = QLabel()
            icon.setPixmap(pixmap)
            layout.addWidget(icon)
        return layout

    def paintEvent(self, event):
        """Set window background color."""
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green)
        self.setPalette(p)


class DashItem(QWidget):
    """Dashboard item data representation."""

    def __init__(self, Type, parent, room=None, reservation=None):
        """Init."""
        super().__init__(parent)
        self.parent = parent

        self.type = Type
        try:
            if Type != 2 and reservation is None:
                pass
        except AttributeError:
            print("DashItem")
            print(
                "You either forgot to pass a reservation or got the type wrong"
            )
            raise

        self.reservation = reservation
        self.room = room

        if self.room is None and self.reservation:
            self.room = self.reservation.getRoomForDashboard(self.parent)

        self.items = [
            "RoNumber", "RoStatus", "RoType", "RoAvailableExtras", "RoNotes",
            "RoExtras", "RoMaxCap", "RoBeds", "ReName", "ReDateIn",
            "ReDateOut", "ReNights", "ReAdults", "ReMinors", "ReGroup",
            "ReExtras", "ReNotes", "ReTotal", "RePaid", "ReOwed"
        ]

        self.setup(Type)  # 0 == In, 1 == out, 2 == status

    def setup(self, Type):
        """Init item."""
        # It may seem like CheckIn DashItem's shouldn't have an assigned number, but
        # room number is assigned the day the reservation is to be claimed, and Non-Status
        # dashboard items only appear on the dashboard the day they are needed,
        # so room numbers will have been assigned already and therefore it makes sense :D.

        self.multi = None

        if self.reservation is not None:
            if self.reservation.getMultiRoom() is True:
                self.multi = True
            else:
                self.multi = False
        else:
            self.multi = False

        if self.multi is False:
            roomData = self.room.getData()
            self.RoNumber = roomData["roomNo"]
            self.RoStatus = roomData["status"]
            self.RoType = roomData["roomType"]
            self.RoAvailableExtras = roomData["extras"]
            self.RoNotes = roomData["notes"]
            self.RoMaxCap = roomData["maxCapacity"]
            self.RoBeds = roomData["beds"]
            self.RoExtras = roomData["extras"]
        else:
            self.RoNumber = "M"

        if Type == 0 or Type == 1:
            # Data for all reservations
            rsvData = self.reservation.getData()
            self.ReName = self.reservation.getGuestName()
            self.ReDateIn = rsvData["dateIn"]
            self.ReDateOut = rsvData["dateOut"]
            self.ReNights = self.reservation.getNights()
            self.ReAdults = rsvData["adults"]
            self.ReMinors = rsvData["minors"]
            self.ReGroup = rsvData["rsvgroup"] if rsvData["rsvgroup"] else ""
            self.ReExtras = self.reservation.getExtras()
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

    def gotNote(self, what):
        """Return True if there are notes, false if there arent.

        what can be 'ro'(room) or 're'(reservation)
        """
        if what == "ro":
            if self.room.gotNote():
                return True
            else:
                return False
        if what == "re":
            if self.reservation.gotNote():
                return True
            else:
                return False

    def getMulti(self):
        """Return number of rooms if multi room, return False if single room."""
        rooms = self.reservation.getMultiRoom()
        if rooms is None:
            return False
        return rooms

    def getData(self):
        """Return the item data as a dict."""
        data = {}
        for item in self.items:
            try:
                if not getattr(self, item) is None:
                    data[item] = getattr(self, item)
            except AttributeError:
                # some items will be none an raise an error.
                # it is not an error so just move on.
                pass
        data["type"] = self.type
        return data
