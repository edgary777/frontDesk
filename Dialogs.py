"""Dialogs to show data or prompt for information."""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Db
from bcrypt import checkpw


class CredentialsPromptD(QDialog):
    """Dialog to prompt for the credentials of a user."""

    def __init__(self, parent, callback, minPrivilege, cursor):
        """Init."""
        super().__init__(parent)

        self.minPrivilege = minPrivilege

        self.cursor = cursor

        self.callback = callback

        self.setFixedWidth(300)
        # self.setFixedHeight(200)

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

        title = QLabel("Registrar Cambios")
        title.setStyleSheet(self.titleStyle)
        title.setAlignment(Qt.AlignCenter)

        buttonPadding = QMargins(10, 0, 10, 0)

        self.username = QLineEdit()
        self.username.setTextMargins(buttonPadding)
        self.username.setPlaceholderText("Usuario")
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setStyleSheet(self.inputStyle)

        self.password = QLineEdit()
        self.password.setTextMargins(buttonPadding)
        self.password.setPlaceholderText("Contraseña")
        self.password.setAlignment(Qt.AlignCenter)
        self.password.setStyleSheet(self.inputStyle)
        self.password.setEchoMode(QLineEdit.Password)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.checkCredentials)
        self.buttons.rejected.connect(self.reject)
        self.buttons.setStyleSheet(self.buttonStyle)

        self.message = QLabel()
        self.message.setStyleSheet(self.messageStyle)
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setWordWrap(True)
        self.message.setMinimumHeight(16)

        # enter events to go to the next field.
        self.username.returnPressed.connect(self.password.setFocus)
        self.password.returnPressed.connect(self.buttons.accepted)

        # textChanged signals to clean alert message on edit.
        self.password.textEdited.connect(lambda: self.message.setText(""))
        self.username.textEdited.connect(lambda: self.message.setText(""))

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.buttons)
        layout.addWidget(self.message)
        layout.addStretch()

        self.setLayout(layout)
        self.username.setFocus()

    def checkCredentials(self):
        """Register root user when the accept button is pressed."""
        print("Called")
        if self.password.text() == "" or self.username.text() == "":
            # Verify no field is empty.
            self.message.setText("Por favor rellena todos los campos.")
            print("Empty Field")
            return

        username = self.username.text()
        data = self.db.getUser(username, self.cursor)
        if data is False:
            self.message.setText("Usuario ó contraseña incorrectos.")
            self.password.setText("")
            print("Username doesn't exist")
            return

        if self.checkPass(self.password.text(), data[6]) is False:
            self.message.setText("Usuario ó contraseña incorrectos.")
            self.password.setText("")
            print("Password is incorrect")
            return

        if data[1] > self.minPrivilege:
            self.message.setText("Este usuario no tiene permiso de realizar esta acción.")
            self.password.setText("")
            print("User does not have enough privileges.")
            return
        # If all those tests were passed, now pass the data and accept the dialog.
        self.callback(data)
        self.accept()

    def checkPass(self, password, hashedPass):
        """Encrypt the password."""
        return checkpw(password.encode('utf8'), hashedPass)

    def keyPressEvent(self, event):
        """Reimplementation of the dialog key press event."""
        # I don't need the dialog to catch key presses, and when it does, it catches
        # any time enter is pressed anywhere on the dialog as a call to the ok button.
        # It was very annoying so I just reimplemented it to nothing.
        pass
