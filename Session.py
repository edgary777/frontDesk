from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import SideBar
from Dashboard import DashScroll, DashItem
import random
import Room
import Reservation
import People
import Manager
import Db
import datetime


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
        manager = Manager.CheckInManager(self)
        checkIns = manager.getToday()
        items = []
        for cin in checkIns:
            items.append(DashItem(1, self, reservation=cin))
        self.checkIn.getList().addItems(items)

    def updateCheckOut(self):
        """Update the checkOut scroller."""
        # manager = Manager.CheckOutManager(self)
        # checkOuts = manager.getToday()
        # items = []
        # for cout in checkOuts:
        #     items.append(DashItem(1, self, reservation=cout))
        # self.checkOut.getList().addItems(items)
        pass

    def updateStatus(self):
        """Update the roomStatus scroller."""
        manager = Manager.RoomManager(self)
        # today = datetime.datetime.today().date()
        rooms = manager.getRooms()
        items = []
        for room in rooms:
            items.append(DashItem(2, self, room=room))
        self.roomStatus.getList().addItems(items)
