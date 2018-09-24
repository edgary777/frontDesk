"""Dashboard display."""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from colorama import Fore, Style
import datetime
import sys
import os


# Disable
def blockPrint():
    """Disable printing to terminal."""
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    """Enable printing to terminal."""
    sys.stdout = sys.__stdout__


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
        """Add an item.

        Input: Takes 1 argument "items".
            items must be a list of data with the first item being an indicator
            of the type of data and the second item being a list of data for the
            dashboard items.

            items = [type, [[data1], [data2], ...]]

            Indicator meaning:
                1 = room
                2 = check-in
                3 = check-out

        Output: None
        """
        print(Fore.RED)
        print("DashList/addItem")
        print(items)
        if items[0]:
            if items[0] == 1:
                print("I got 1")
                print(items)
                for data in items[1]:
                    self.items.append([1, data])
            elif items[0] == 2:
                print("I got 2")
                print(items)
                for data in items[1]:
                    self.items.append([2, data])
            elif items[0] == 3:
                print(" I got 3")
                print(items)
                for data in items[1]:
                    self.items.append([3, data])
            else:
                print("Invalid Value")
                print(items)
        print(Style.RESET_ALL)
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
        roomRow = []
        counter = 0
        rooms = len(self.items)
        uiItem = None
        rowLen = 3
        for data in self.items:
            if data[0] == 1:
                if len(roomRow) <= rowLen:
                    roomRow.append(DashRoomItem(data[1], self))
                    counter += 1
                if len(roomRow) == rowLen or counter == rooms:
                    uiItem = DashRoomRow(roomRow, rowLen, self)
            elif data[0] == 2:
                uiItem = DashCheckInItem(data[1], self)
            elif data[0] == 3:
                uiItem = DashCheckOutItem(data[1], self)
            if data[0] == 1:
                if uiItem is not None:
                    self.layout.addWidget(uiItem)
                    roomRow = []
                    uiItem = None
            else:
                self.layout.addWidget(uiItem)
        self.layout.addStretch()

    def updateUi(self):
        """Update the Ui."""
        self.cleanUi()

        self.fillUi()


class SuperCheck(QWidget):
    """Parent class for the check-in and check-out dashboard items."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

    def guestsIcon(self, size, adults, minors, place, layout):
        """Return a layout with the adults and minors icon and number."""
        innerLayout = QHBoxLayout()

        pixmap = QPixmap("Resources/ac.png").scaled(size, size,
                                                    Qt.KeepAspectRatio)
        adultIcon = QLabel()
        adultIcon.setPixmap(pixmap)
        innerLayout.addWidget(adultIcon)
        adultLabel = QLabel(str(adults))
        innerLayout.addWidget(adultLabel)

        pixmap = QPixmap("Resources/ac.png").scaled(size, size,
                                                    Qt.KeepAspectRatio)
        minorIcon = QLabel()
        minorIcon.setPixmap(pixmap)
        innerLayout.addWidget(minorIcon)
        minorLabel = QLabel(str(minors))
        innerLayout.addWidget(minorLabel)

        layout.addLayout(innerLayout, 0, place, 2, 1)

    def noteIcon(self, Note, place, layout):
        """Return notes icon if status is True."""
        if Note is not None:
            pixmap = QPixmap("Resources/note.png").scaled(
                40, 40, Qt.KeepAspectRatio)
            notesIcon = QLabel()
            notesIcon.setPixmap(pixmap)
            self.setToolTip(str(Note))
        else:
            pixmap = QPixmap().scaled(40, 40, Qt.KeepAspectRatio)
            notesIcon = QLabel()
            notesIcon.setPixmap(pixmap)
        layout.addWidget(notesIcon, 0, place, 3, 1)

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


class DashCheckOutItem(SuperCheck):
    """Check-Out graphic representation for the dashboard."""

    def __init__(self, data, parent):
        """Init."""
        super().__init__(parent)

        self.rsvData = data[0]

        self.guestData = data[1]

        self.initUi()

        self.setFixedHeight(60)

        self.setToolTip(str(self.rsvData[0]))

    def initUi(self):
        """UI setup."""
        layout = QGridLayout()

        # This dict contains the position of the data we need to populate the ui.
        # RoomNo = 12, Status = 2
        # Group = 11, Nights = 7(dateIn) && 8 (dateOut)
        layout.addWidget(QLabel(str(self.rsvData[12])), 1, 0, 2, 1)  # Room

        groupName = "" if self.rsvData[11] is None else self.rsvData[11]
        layout.addWidget(QLabel(str(groupName)), 2, 2, 2, 1)  # Group

        if self.guestData[2] is not None:
            guestName = str(self.guestData[1]) + " " + str(self.guestData[2])
        else:
            guestName = str(self.guestData[1])

        layout.addWidget(QLabel(guestName), 0, 1, 2, 1)
        self.noteIcon(self.rsvData[14], 2, layout)

        din = datetime.datetime.strptime(self.rsvData[7], "%Y-%m-%d")
        dout = datetime.datetime.strptime(self.rsvData[8], "%Y-%m-%d")

        nights = abs((dout - din).days)

        # Paid = 10, rate = 9
        paid = 0 if self.rsvData[10] is None else self.rsvData[10]
        owed = (self.rsvData[9] * nights) - paid

        owedLabel = QLabel("$" + str(owed))

        owedLabel.setAlignment(Qt.AlignCenter)

        layout.addWidget(owedLabel, 1, 3, 2, 2)

        self.setLayout(layout)


class DashCheckInItem(SuperCheck):
    """Check-In graphic representation for the dashboard."""

    def __init__(self, data, parent):
        """Init."""
        super().__init__(parent)

        self.rsvData = data[0]

        self.guestData = data[1]

        self.initUi()

        self.setFixedHeight(60)

        self.setToolTip(str(self.rsvData[0]))

    def initUi(self):
        """UI setup."""
        layout = QGridLayout()

        # This dict contains the position of the data we need to populate the ui.
        # RoomNo = 12, Status = 2
        # Group = 11, Nights = 7(dateIn) && 8 (dateOut)
        layout.addWidget(QLabel(str(self.rsvData[12])), 1, 0, 2, 1)  # Room

        groupName = "" if self.rsvData[11] is None else self.rsvData[11]
        layout.addWidget(QLabel(str(groupName)), 2, 1, 2, 1)  # Group

        if self.guestData[2] is not None:
            guestName = str(self.guestData[1]) + " " + str(self.guestData[2])
        else:
            guestName = str(self.guestData[1])

        layout.addWidget(QLabel(guestName), 0, 1, 2, 1)
        self.noteIcon(self.rsvData[14], 2, layout)

        self.guestsIcon(10, self.rsvData[5], self.rsvData[6], 3, layout)

        din = datetime.datetime.strptime(self.rsvData[7], "%Y-%m-%d")
        dout = datetime.datetime.strptime(self.rsvData[8], "%Y-%m-%d")

        nights = abs((dout - din).days)

        if nights > 1:
            layout.addWidget(QLabel(str(nights) + " Noches"), 2, 3, 2, 1)
        else:
            layout.addWidget(QLabel(str(nights) + " Noche"), 2, 3, 2, 1)

        self.setLayout(layout)


class DashRoomItem(QWidget):
    """Room graphic representation for the dasboard."""

    def __init__(self, data, parent):
        """Init."""
        super().__init__(parent)

        self.data = data

        self.initUi()

        self.setFixedHeight(75)
        self.setFixedWidth(75)

        self.setToolTip(str(self.data[0]))

    def initUi(self):
        """UI setup."""
        layout = QVBoxLayout()

        # print(self.data)
        roomNo = QLabel(self.data[0])

        roomNo.setAlignment(Qt.AlignCenter)
        styleSheet = """
        QLabel {
            font-size: 18px;
        }"""

        roomNo.setStyleSheet(styleSheet)

        layout.addWidget(roomNo)

        self.setLayout(layout)

    def paintEvent(self, event):
        """Set window background color."""
        self.setAutoFillBackground(True)
        p = self.palette()
        if self.data[2] == 0:
            p.setColor(self.backgroundRole(), Qt.green)
        elif self.data[2] == 1:
            p.setColor(self.backgroundRole(), Qt.cyan)
        elif self.data[2] == 2:
            p.setColor(self.backgroundRole(), Qt.lightGray)
        if self.data[2] == 3:
            p.setColor(self.backgroundRole(), Qt.red)


        self.setPalette(p)


class DashRoomRow(QWidget):
    """Container to organize DashRoomItems."""

    def __init__(self, items, rowLen, parent):
        """Init."""
        super().__init__(parent)

        self.items = items
        self.rowLen = rowLen

        self.initUi()

    def initUi(self):
        """UI setup."""
        layout = QHBoxLayout()

        for item in self.items:
            layout.addWidget(item)

        if len(self.items) != self.rowLen:
            width = self.items[0].width()
            height = self.items[0].height()
            for item in range(self.rowLen - len(self.items)):
                spacer = QWidget(self)
                spacer.setFixedSize(width, height)
                layout.addWidget(spacer)

        self.setLayout(layout)

    # def paintEvent(self, event):
    #     """Set window background color."""
    #     self.setAutoFillBackground(True)
    #     p = self.palette()
    #     p.setColor(self.backgroundRole(), Qt.blue)
    #     self.setPalette(p)
