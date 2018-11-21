"""Settings menu display."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import UserCreator


class SettingsWindow(QWidget):
    """Settings menu display widget."""

    def __init__(self, mainW):
        """Init."""
        super().__init__(mainW)

        self.mainW = mainW

        self.initUi()

        # self.newUser.clicked.connect()
        self.logout.clicked.connect(self.mainW.logout)
        self.exit.clicked.connect(lambda: self.mainW.start())

        self.newUser.clicked.connect(self.newUserWindow)

    def newUserWindow(self):
        """Change the window to the user creator."""
        widget = UserCreator.UserCreator(self, self.mainW)
        self.mainW.changeDisplay(widget)

    def initUi(self):
        """Ui setup."""
        layout = QVBoxLayout()

        self.newUser = QPushButton("Nuevo Usuario")
        self.logout = QPushButton("Cerrar Sesión")
        self.exit = QPushButton("Salir")

        layout.addStretch()
        layout.addWidget(self.newUser)
        layout.addWidget(self.logout)
        layout.addWidget(self.exit)
        layout.addStretch()

        self.setLayout(layout)
