"""Login window."""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import Db
import sys
import os
from bcrypt import checkpw


class Login(QWidget):
    """Login window shown at startup."""

    def __init__(self, parent, mainW):
        """Init."""
        super().__init__(parent)

        self.mainW = mainW

        self.setFixedWidth(300)
        self.setFixedHeight(200)

        self.titleStyle = """
        QLabel {
            font-size: 30px;
            font-weight: 900;
        }
        """

        self.buttonStyle = """
        QPushButton {
            font-size: 20px;
            font-weight: 900;
        }
        """

        self.inputStyle = """
        QLineEdit {
            font-size: 25px;
            border: 2px solid #666666;
            border-radius: 8px;
            font-weight: bold;
        }"""

        self.messageStyle = """
        QLabel {
            color: red;
            font-size: 16px;
            font-weight: regular;
        }"""

        self.db = Db.Db()

        self.initUi()

    def initUi(self):
        """Ui setup."""
        layout = QVBoxLayout()

        title = QLabel("Inicia Sesión")
        title.setStyleSheet(self.titleStyle)
        title.setAlignment(Qt.AlignCenter)

        buttonPadding = QMargins(10, 0, 10, 0)

        self.username = QLineEdit()
        self.username.setTextMargins(buttonPadding)
        self.username.setPlaceholderText("Username")
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setStyleSheet(self.inputStyle)

        self.password = QLineEdit()
        self.password.setTextMargins(buttonPadding)
        self.password.setPlaceholderText("Password")
        self.password.setAlignment(Qt.AlignCenter)
        self.password.setStyleSheet(self.inputStyle)
        self.password.setEchoMode(QLineEdit.Password)

        self.message = QLabel()
        self.message.setStyleSheet(self.messageStyle)
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setWordWrap(True)
        self.message.setMinimumHeight(16)

        self.accept = QPushButton("ACEPTAR")
        self.accept.clicked.connect(self.login)
        # self.accept.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.accept.setStyleSheet(self.buttonStyle)
        self.password.returnPressed.connect(self.accept.click)

        # enter event to go to the next field.
        self.username.returnPressed.connect(self.password.setFocus)

        # textChanged signals to alert clean message on edit.
        self.password.textEdited.connect(lambda: self.message.setText(""))
        self.username.textEdited.connect(lambda: self.message.setText(""))

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.accept)
        layout.addWidget(self.message)
        layout.addStretch()

        self.setLayout(layout)
        self.username.setFocus()

    def getData(self, username):
        """Return the data of the user from the database."""
        data = self.db.getUser(username, self.mainW.cursor)
        if data is not False:
            return data
        else:
            # Raise error and sende message to the display.
            print("No user registered with that username")
            return False

    def checkPass(self, password, dbPassword):
        """Check if the password is the same as in the db."""
        return checkpw(password.encode('utf8'), dbPassword)

    def login(self):
        """Restart with the user if the data is correct."""
        if self.password.text() == "" or self.username.text() == "":
            self.message.setText("Por favor rellena ambos campos.")
            print("Empty Field")
            return

        self.dbPass = self.getData(self.username.text())
        if self.dbPass:
            self.dbPass = self.dbPass[6]
        else:
            # Raise error and sende message to the display.
            self.password.setText("")
            self.message.setText("Usuario ó contraseña incorrectos.")
            print("No user registered with that username.")
            return

        if self.checkPass(self.password.text(), self.dbPass):
            user = self.db.getUser(self.username.text(), self.mainW.cursor)
            # user = [ID, TYPE[ROOT=0, ADMIN=1, USER=2]]
            user = [user[0], user[1]]
            self.mainW.start(user)
        else:
            # Raise error and sende message to the display.
            self.password.setText("")
            self.message.setText("Usuario ó contraseña incorrectos.")
            print("Username or password are wrong.")
            return False
