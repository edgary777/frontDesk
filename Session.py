from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import SideBar
from Dashboard import DashScroll, DashItem
import random
import Room

class Session(QWidget):
    """Holds all data and can be restarted to show changes or change user."""

    def __init__(self, user, parent):
        """Init."""
        super().__init__(parent)

        # user = [ID, NAME, TYPE[ADMIN=0, USER=1]]
        self.user = user

        self.initUi()

    def initUi(self):
        """Ui Setup."""
        layout = QVBoxLayout()

        btnList = ["Reservación", "Check-In", "Check-Out", "Configuración"]
        sidebar = SideBar.SideBar(btnList, self)

        self.checkIn = DashScroll(self)
        self.checkOut = DashScroll(self)
        self.roomStatus = DashScroll(self)

        self.updateAll()

        dashLayout = QHBoxLayout()

        dashLayout.addWidget(self.checkIn)
        dashLayout.addWidget(self.checkOut)
        dashLayout.addWidget(self.roomStatus)

        dashLayout.setStretchFactor(self.checkIn, 3)
        dashLayout.setStretchFactor(self.checkOut, 3)
        dashLayout.setStretchFactor(self.roomStatus, 2)

        layout.addLayout(dashLayout)
        layout.addWidget(sidebar)

        self.setLayout(layout)

    def updateAll(self):
        """Update all scrollers."""
        self.updateStatus()
        self.updateCheckIn()
        self.updateCheckOut()

    def updateCheckIn(self):
        """Update the checkIn scroller."""
        pass

    def updateCheckOut(self):
        """Update the checkOut scroller."""
        pass

    def updateStatus(self):
        """Update the roomStatus scroller."""
        rooms = self.roomDummyCreator()
        items = []
        for room in rooms:
            items.append(DashItem(2, room, self))
        self.roomStatus.getList().addItems(items)

    def roomDummyCreator(self):
        """Create dummy rooms for testing."""
        rooms = 10
        roomList = []
        items = [
            "ID", "number", "type", "beds", "maxCapacity", "extras", "status",
            "notes"
        ]
        for room in range(rooms):
            data = {}
            for item in items:
                data[item] = round(random.random() * 10000)
            roomObj = Room.RoomD(self)
            print(roomObj)
            roomObj.setData(data)
            roomList.append(roomObj)

        return roomList
