"""Session manager."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import MenuBar
from Dashboard import DashScroll
import Manager
from colorama import Fore, Style


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
        print(Fore.CYAN)
        print("Start of dashboard updater")
        self.updateStatus()
        self.updateCheckIn()
        self.updateCheckOut()
        print(Fore.CYAN)
        print("End of dashboard updater")
        print(Style.RESET_ALL)

    def updateCheckIn(self):
        """Update the checkIn scroller."""
        print(Fore.CYAN)
        print("updateCheckIn")
        print("Going to CheckInManager")
        print(Style.RESET_ALL)
        manager = Manager.CheckInManager(self, self.cursor)
        checkIns = manager.getToday()
        print(Fore.CYAN)
        print("Finishied with CheckInManager")
        print("Sending the data we got from the manager to the dashboard")
        print(Style.RESET_ALL)
        self.checkIn.getList().addItems([2, checkIns])
        print(Fore.CYAN)
        print("Finished sending the data")
        print(Style.RESET_ALL)

    def updateCheckOut(self):
        """Update the checkOut scroller."""
        print(Fore.CYAN)
        print("updateCheckOut")

        # rsvManager = Manager.ReservationManager(self, self.cursor)
        # rsvManager.getActiveRsvs()
        # rsvManager.getFinishedRsvs()

        print("Going to CheckOutManager")
        print(Style.RESET_ALL)
        manager = Manager.CheckOutManager(self, self.cursor)
        checkOuts = manager.getToday()
        print(Fore.CYAN)
        print("Finishied with CheckOutManager")

        print("Sending the data we got from the manager to the dashboard")
        print(Style.RESET_ALL)
        self.checkOut.getList().addItems([3, checkOuts])
        print(Fore.CYAN)
        print("Finished sending the data")
        print(Style.RESET_ALL)

    def updateStatus(self):
        """Update the roomStatus scroller."""
        print(Fore.CYAN)
        print("updateCheckIn")
        print("Going to RoomManager")
        print(Style.RESET_ALL)
        manager = Manager.RoomManager(self, self.cursor)
        rooms = manager.getRooms()
        roomsData = [manager.getRoom(room) for room in rooms]
        print(Fore.BLUE)
        print(roomsData)
        print(Fore.CYAN)
        print("Finishied with RoomManager")
        print("Sending the data we got from the manager to the dashboard")
        print(Style.RESET_ALL)
        self.roomStatus.getList().addItems([1, roomsData])
        print(Fore.CYAN)
        print("Finished sending the data")
        print(Style.RESET_ALL)
