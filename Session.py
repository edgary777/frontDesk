from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import MenuBar
from Dashboard import DashScroll, DashItem
import Manager


class Session(QWidget):
    """Holds all data and can be restarted to show changes or change user."""

    def __init__(self, user, parent, cursor):
        """Init."""
        super().__init__(parent)

        # user = [ID, NAME, TYPE[ADMIN=0, USER=1]]
        self.user = user
        self.cursor = cursor

        self.initUi()

    def initUi(self):
        """Ui Setup."""
        layout = QVBoxLayout()

        btnList = ["Reservación", "Check-In", "Check-Out", "Configuración"]
        menubar = MenuBar.MenuBar(btnList, self)

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
        items = []
        for cin in checkIns:
            items.append(DashItem(0, self, reservation=cin))
        self.checkIn.getList().addItems(items)

    def updateCheckOut(self):
        """Update the checkOut scroller."""
        rsvManager = Manager.ReservationManager(self, self.cursor)
        rsvManager.getActiveRsvs()
        rsvManager.getFinishedRsvs()
        manager = Manager.CheckOutManager(self, self.cursor)
        checkOuts = manager.getToday()
        items = []
        for cout in checkOuts:
            items.append(DashItem(1, self, reservation=cout))
        self.checkOut.getList().addItems(items)

    def updateStatus(self):
        """Update the roomStatus scroller."""
        manager = Manager.RoomManager(self, self.cursor)
        # today = datetime.datetime.today().date()
        rooms = manager.getRooms()
        items = []
        for room in rooms:
            items.append(DashItem(2, self, room=room))
        self.roomStatus.getList().addItems(items)
