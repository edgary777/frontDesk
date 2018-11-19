"""Session manager."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import MenuBar
from Dashboard import DashScroll
import Manager
import Db


class Session(QWidget):
    """Holds all data and can be restarted to show changes or change user."""

    def __init__(self, user, mainW, cursor):
        """Init."""
        super().__init__(mainW)

        # user = [ID, TYPE[ROOT=0, ADMIN=1, USER=2]]
        self.mainW = mainW
        self.user = user

        self.cursor = cursor

        self.db = Db.Db()

        self.userData = self.db.getUserById(self.user[0], self.cursor)

        self.username = self.userData[2]

        if self.userData[1] == 0:
            self.userType = " Root"
        elif self.userData[1] == 1:
            self.userType = " Admin"
        elif self.userData[1] == 2:
            self.userType = " Usuario"
        else:
            # Raise error because this data is wrong.
            pass

        title = self.mainW.getVersion() + " - Usuario: {} - Privilegios: {}".format(
            str(self.username), self.userType)

        self.mainW.setWindowTitle(title)

        self.initUi()

    def initUi(self):
        """Ui Setup."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        btnList = ["Reservación", "Check-In", "Check-Out", "Configuración"]
        menubar = MenuBar.MenuBar(btnList, self, self.mainW)

        self.checkIn = DashScroll(self)
        self.checkOut = DashScroll(self)
        self.roomStatus = DashScroll(self)

        self.updateAll()

        dashLayout = QHBoxLayout()
        dashLayout.setContentsMargins(10, 0, 10, 0)
        dashLayout.setSpacing(5)

        dashLayout.addWidget(self.checkIn)
        dashLayout.addStretch()
        dashLayout.addWidget(self.checkOut)
        dashLayout.addStretch()
        dashLayout.addWidget(self.roomStatus)

        dashLayout.setStretchFactor(self.checkIn, 2)
        dashLayout.setStretchFactor(self.checkOut, 2)
        dashLayout.setStretchFactor(self.roomStatus, 1)

        layout.addLayout(dashLayout)
        layout.addWidget(menubar)

        self.setLayout(layout)

    def updateAll(self):
        """Update all scrollers."""
        self.updateStatus()
        self.updateCheckIn()
        self.updateCheckOut()

    def updateCheckIn(self):
        """Update the checkIn scroller."""
        manager = Manager.CheckInManager(self, self.cursor)
        checkIns = manager.getToday()
        self.checkIn.getList().addItems([2, checkIns])

    def updateCheckOut(self):
        """Update the checkOut scroller."""
        # rsvManager = Manager.ReservationManager(self, self.cursor)
        # rsvManager.getActiveRsvs()
        # rsvManager.getFinishedRsvs()
        manager = Manager.CheckOutManager(self, self.cursor)
        checkOuts = manager.getToday()

        self.checkOut.getList().addItems([3, checkOuts])

    def updateStatus(self):
        """Update the roomStatus scroller."""
        manager = Manager.RoomManager(self, self.cursor)
        rooms = manager.getRooms()
        roomsData = [manager.getRoom(room) for room in rooms]
        self.roomStatus.getList().addItems([1, roomsData])
