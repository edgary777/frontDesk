"""Dashboard display."""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import datetime


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
        self.area.setFrameShape(QFrame.NoFrame)
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
        self.layout.setSpacing(3)
        self.layout.setContentsMargins(3, 3, 3, 3)
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
        if items[0]:
            if items[0] == 1:
                for data in items[1]:
                    self.items.append([1, data])
            elif items[0] == 2:
                for data in items[1]:
                    self.items.append([2, data])
            elif items[0] == 3:
                for data in items[1]:
                    self.items.append([3, data])
            else:
                # print("Invalid Value")
                # print(items)
                pass

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
                self.parent().parent().parent().setMinimumHeight(300)
                self.parent().parent().parent().setMaximumWidth(260)
                self.parent().parent().parent().setMinimumWidth(260)
                if len(roomRow) <= rowLen:
                    roomRow.append(DashRoomItem(data[1], self))
                    counter += 1
                if len(roomRow) == rowLen or counter == rooms:
                    uiItem = DashRoomRow(roomRow, rowLen, self)
            elif data[0] == 2:
                self.parent().parent().parent().setMaximumWidth(520)
                self.parent().parent().parent().setMinimumWidth(400)
                uiItem = DashCheckInItem(data[1], self)
            elif data[0] == 3:
                self.parent().parent().parent().setMaximumWidth(520)
                self.parent().parent().parent().setMinimumWidth(400)
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

    def paintEvent(self, event):
        """Set window background color."""
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)


class SuperCheck(QWidget):
    """Parent class for the check-in and check-out dashboard items."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.mono = QFont()
        self.mono.setStyleHint(QFont.Monospace)
        self.mono.setFamily("Roboto Mono")
        self.fontAwesome = QFont()
        self.fontAwesome.setFamily("FontAwesome")

        self.roomNoStyle = """font-size: 20px;
                              font-weight: 900;
                              font-family: 'Roboto Mono';
                           """

        self.nameStyle = """font-size: 16px;
                            font-weight: bold;
                         """

        self.groupStyle = """font-size: 16px;
                             font-weight: Regular;
                          """

        # self.setStyleSheet("border: 3px solid black")

        self.maxNameWidth = 185

    def noteIcon(self, Note, place, layout):
        """Return notes icon if status is True."""
        size = 40
        if Note is not None:
            pixmap = QPixmap("Resources/note.png").scaled(
                size, size, Qt.KeepAspectRatio)
            notesIcon = QLabel()
            notesIcon.setPixmap(pixmap)
            noteText = "<html><head/><body><p>" + Note + "</p></body></html>"
            notesIcon.setToolTip(noteText)
            layout.addWidget(notesIcon, 0, place, 4, 1, Qt.AlignCenter)

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
        p.setColor(self.backgroundRole(), Qt.lightGray)
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
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setHorizontalSpacing(8)

        # This dict contains the position of the data we need to populate the ui.
        # RoomNo = 12, Status = 2
        # Group = 11, Nights = 7(dateIn) && 8 (dateOut)
        roomNo = QLabel(str(self.rsvData[12]))
        roomNo.setFont(self.mono)
        roomNo.setStyleSheet(self.roomNoStyle)
        layout.addWidget(roomNo, 0, 0, 4, 1, Qt.AlignCenter)  # Room

        groupName = "" if self.rsvData[11] is None else self.rsvData[11]
        groupNameLabel = QLabel(str(groupName))
        groupNameLabel.setStyleSheet(self.groupStyle)
        groupNameLabel.setMaximumWidth(self.maxNameWidth)
        layout.addWidget(groupNameLabel, 2, 1, 2, 1, Qt.AlignTop)  # Group

        if self.guestData[2] is not None:
            guestName = str(self.guestData[1]) + " " + str(self.guestData[2])
        else:
            guestName = str(self.guestData[1])

        guestNameLabel = QLabel(guestName)
        guestNameLabel.setStyleSheet(self.nameStyle)
        guestNameLabel.setMaximumWidth(self.maxNameWidth)

        layout.addWidget(guestNameLabel, 0, 1, 2, 1, Qt.AlignBottom)
        self.noteIcon(self.rsvData[14], 2, layout)

        din = datetime.datetime.strptime(self.rsvData[7], "%Y-%m-%d")
        dout = datetime.datetime.strptime(self.rsvData[8], "%Y-%m-%d")

        nights = abs((dout - din).days)

        # Paid = 10, rate = 9
        paid = 0 if self.rsvData[10] is None else self.rsvData[10]
        owed = (self.rsvData[9] * nights) - paid

        owedLabel = QLabel("$" + str(owed))
        owedStyle = """QLabel {
            font-size: 22px;
            font-weight: bold;
            text-align: center;
        }"""
        owedLabel.setStyleSheet(owedStyle)

        owedLabel.setAlignment(Qt.AlignCenter)

        layout.addWidget(owedLabel, 0, 3, 4, 2)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)

        layout.setColumnMinimumWidth(2, 50)

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

        self.setToolTip(str(self.rsvData[0]))  # Reservation Number

    def initUi(self):
        """UI setup."""
        layout = QGridLayout()
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setHorizontalSpacing(5)

        # This dict contains the position of the data we need to populate the ui.
        # RoomNo = 12, Status = 2
        # Group = 11, Nights = 7(dateIn) && 8 (dateOut)
        roomNo = QLabel(str(self.rsvData[12]))
        roomNo.setFont(self.mono)
        roomNo.setStyleSheet(self.roomNoStyle)
        layout.addWidget(roomNo, 0, 0, 4, 1, Qt.AlignCenter)  # Room

        groupName = "" if self.rsvData[11] is None else self.rsvData[11]
        groupNameLabel = QLabel(str(groupName))
        groupNameLabel.setStyleSheet(self.groupStyle)
        groupNameLabel.setMaximumHeight(16)
        groupNameLabel.setWordWrap(True)
        layout.addWidget(groupNameLabel, 2, 1, 2, 1, Qt.AlignTop)  # Group

        if self.guestData[2] is not None:
            guestName = str(self.guestData[1]) + " " + str(self.guestData[2])
        else:
            guestName = str(self.guestData[1])

        guestNameLabel = QLabel(guestName)
        guestNameLabel.setMaximumHeight(16)
        guestNameLabel.setStyleSheet(self.nameStyle)
        guestNameLabel.setWordWrap(True)
        layout.addWidget(guestNameLabel, 0, 1, 2, 1, Qt.AlignBottom)

        self.noteIcon(self.rsvData[14], 2, layout)

        self.guestsIcon(self.rsvData[5], self.rsvData[6], 3, layout)

        din = datetime.datetime.strptime(self.rsvData[7], "%Y-%m-%d")
        dout = datetime.datetime.strptime(self.rsvData[8], "%Y-%m-%d")

        nightsStyle = """QLabel {
            font-size: 15px;
            font-weight: 900;
            text-align: center;
        }"""

        nights = abs((dout - din).days)

        if nights > 1:
            nightsLabel = QLabel(str(nights) + " Noches")
            nightsLabel.setStyleSheet(nightsStyle)
            nightsLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(nightsLabel, 2, 3, 2, 1)
        else:
            nightsLabel = QLabel(str(nights) + " Noche")
            nightsLabel.setStyleSheet(nightsStyle)
            nightsLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(nightsLabel, 2, 3, 2, 1)

        layout.setColumnMinimumWidth(2, 40)
        layout.setColumnMinimumWidth(3, 75)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 12)
        layout.setColumnStretch(2, 4)
        layout.setColumnStretch(3, 3)

        self.setLayout(layout)

    def guestsIcon(self, adults, minors, place, layout):
        """Return a layout with the adults and minors icon and number."""
        adultsRich = """
        <html>
        <head/>
        <body>
            <p>
                <span style='font-family: "Roboto"; font-size: 20px; font-weight: bold;'>
                    <span style='font-size: 18px;'>
                        \uf183
                    </span>
                    {}
                </span>
            </p>
        </body>
        </html>""".format(adults)

        minorsRich = """
        <html>
        <head/>
        <body>
            <p>
                <span style='font-family: "Roboto"; font-size: 20px; font-weight: bold;'>
                    <span style='font-size: 13px;'>
                        \u00A0\uf1ae
                    </span>
                    {}
                </span>
            </p>
        </body>
        </html>""".format(adults)

        Adults = QLabel(adultsRich)
        Adults.setContentsMargins(0, 0, 0, 0)
        Adults.setAlignment(Qt.AlignCenter)
        Adults.setToolTip("Adultos")

        Minors = QLabel(minorsRich)
        Minors.setContentsMargins(0, 0, 0, 0)
        Minors.setAlignment(Qt.AlignCenter)
        Minors.setToolTip("Menores")

        internalLayout = QHBoxLayout()
        internalLayout.addStretch()
        internalLayout.addWidget(Adults)
        internalLayout.addWidget(Minors)
        internalLayout.addStretch()

        internalLayout.setContentsMargins(0, 0, 0, 0)
        internalLayout.setAlignment(Qt.AlignCenter)

        layout.addLayout(internalLayout, 0, place, 2, 1)


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

        roomNo = QLabel(self.data[0])

        roomNo.setAlignment(Qt.AlignCenter)
        styleSheet = """
        QLabel {
            font-size: 18px;
            font-weight: bold;
        }"""

        roomNo.setStyleSheet(styleSheet)

        layout.addWidget(roomNo)

        self.setLayout(layout)

    def paintEvent(self, event):
        """Set window background color."""
        self.setAutoFillBackground(True)
        p = self.palette()
        if self.data[2] == 0:
            p.setColor(self.backgroundRole(), Qt.green)  # Libre
        elif self.data[2] == 1:
            p.setColor(self.backgroundRole(), Qt.cyan)  # En Limpieza
        elif self.data[2] == 2:
            p.setColor(self.backgroundRole(), Qt.red)  # Ocupado
        if self.data[2] == 3:
            p.setColor(self.backgroundRole(), Qt.lightGray)  # Fuera de servicio

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

        layout.setSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addStretch()
        for item in self.items:
            layout.addWidget(item)

        if len(self.items) != self.rowLen:
            width = self.items[0].width()
            height = self.items[0].height()
            for item in range(self.rowLen - len(self.items)):
                spacer = QWidget(self)
                spacer.setFixedSize(width, height)
                layout.addWidget(spacer)

        layout.addStretch()
        self.setLayout(layout)

    # def paintEvent(self, event):
    #     """Set window background color."""
    #     self.setAutoFillBackground(True)
    #     p = self.palette()
    #     p.setColor(self.backgroundRole(), Qt.blue)
    #     self.setPalette(p)
