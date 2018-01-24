from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import SideBar


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

        layout.addWidget(sidebar)

        self.setLayout(layout)
