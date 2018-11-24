"""Settings window widget for the creation of new users."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from bcrypt import hashpw, gensalt
import datetime
import Db
import sys
import os
import Dialogs
import Validators
import Settings


class UserCreator(QWidget):
    """Prompt for data gathering for the creation of new users."""

    def __init__(self, parent, mainW):
        """Init."""
        super().__init__(parent)

        self.mainW = mainW

        self.setFixedWidth(300)

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

        title = QLabel("Crear Usuario")
        title.setStyleSheet(self.titleStyle)
        title.setAlignment(Qt.AlignCenter)

        buttonPadding = QMargins(10, 0, 10, 0)

        self.userType = QComboBox(parent=self)
        self.userType.addItem("Administrador")
        self.userType.addItem("Regular")

        self.username = QLineEdit(parent=self)
        self.username.setTextMargins(buttonPadding)
        self.username.setPlaceholderText("Usuario")
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setStyleSheet(self.inputStyle)

        self.name = QLineEdit(parent=self)
        self.name.setTextMargins(buttonPadding)
        self.name.setPlaceholderText("Nombre")
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setStyleSheet(self.inputStyle)

        self.lastName = QLineEdit(parent=self)
        self.lastName.setTextMargins(buttonPadding)
        self.lastName.setPlaceholderText("Apellidos")
        self.lastName.setAlignment(Qt.AlignCenter)
        self.lastName.setStyleSheet(self.inputStyle)

        # The previous fields need some validation to ensure the data is not garbage.

        self.email = QLineEdit(parent=self)
        self.email.setTextMargins(buttonPadding)
        self.email.setPlaceholderText("E-Mail")
        self.email.setAlignment(Qt.AlignCenter)
        self.email.setStyleSheet(self.inputStyle)

        self.password = QLineEdit(parent=self)
        self.password.setTextMargins(buttonPadding)
        self.password.setPlaceholderText("Contraseña")
        self.password.setAlignment(Qt.AlignCenter)
        self.password.setStyleSheet(self.inputStyle)
        self.password.setEchoMode(QLineEdit.Password)

        self.passwordV = QLineEdit(parent=self)
        self.passwordV.setTextMargins(buttonPadding)
        self.passwordV.setPlaceholderText("Verificar Contraseña")
        self.passwordV.setAlignment(Qt.AlignCenter)
        self.passwordV.setStyleSheet(self.inputStyle)
        self.passwordV.setEchoMode(QLineEdit.Password)

        self.accept = QPushButton("ACEPTAR", parent=self)
        self.accept.clicked.connect(
            lambda: self.credentialsPrompt(self.password.text()))
        # self.accept.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.accept.setStyleSheet(self.buttonStyle)

        self.cancelBtn = QPushButton("CANCELAR", parent=self)
        self.cancelBtn.clicked.connect(lambda: self.mainW.changeDisplay(Settings.SettingsWindow(self.mainW)))
        # self.accept.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.cancelBtn.setStyleSheet(self.buttonStyle)

        self.message = QLabel(parent=self)
        self.message.setStyleSheet(self.messageStyle)
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setWordWrap(True)
        self.message.setMinimumHeight(16)

        # enter events to go to the next field.
        self.username.returnPressed.connect(self.name.setFocus)
        self.name.returnPressed.connect(self.lastName.setFocus)
        self.lastName.returnPressed.connect(self.email.setFocus)
        self.email.returnPressed.connect(self.password.setFocus)
        self.password.returnPressed.connect(self.passwordV.setFocus)
        self.passwordV.returnPressed.connect(self.accept.click)

        # textChanged signals to clean alert message on edit.
        self.username.textEdited.connect(lambda: self.message.setText(""))
        self.name.textEdited.connect(lambda: self.message.setText(""))
        self.lastName.textEdited.connect(lambda: self.message.setText(""))
        self.email.textEdited.connect(lambda: self.message.setText(""))
        self.password.textEdited.connect(lambda: self.message.setText(""))

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(self.userType)
        layout.addWidget(self.username)
        layout.addWidget(self.name)
        layout.addWidget(self.lastName)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.passwordV)
        layout.addWidget(self.accept)
        layout.addWidget(self.cancelBtn)
        layout.addWidget(self.message)
        layout.addStretch()

        self.setLayout(layout)
        self.username.setFocus()

    def credentialsPrompt(self, password):
        """Prompt for credentials to create a new user."""
        if self.password.text() == "" or self.passwordV.text() == "":
            # Verify no field is empty.
            self.message.setText("Por favor rellena todos los campos.")
            print("Empty Field")
            return

        if self.username.text() == "" or self.email.text() == "":
            # Verify no field is empty.
            self.message.setText("Por favor rellena todos los campos.")
            print("Empty Field")
            return

        if self.lastName.text() == "" or self.name.text() == "":
            # Verify no field is empty.
            self.message.setText("Por favor rellena todos los campos.")
            print("Empty Field")
            return

        if len(self.username.text()) < 4:
            # username must be at least 4 characters long.
            self.message.setText(
                "El nombre de usuario debe tener 4 caracteres como minimo.")
            print("Username is too short")
            return

        if not isinstance(self.username.text(), str):
            # Username can't be only numbers.
            self.message.setText("El nombre de usuario no puede ser un número.")

        if len(self.name.text()) < 2:
            # name must be at least 2 characters long.
            self.message.setText(
                "Tu nombre no puede tener menos de 2 caracteres.")
            print("Name is too short")
            return

        if len(self.lastName.text()) < 2:
            # last name must be at least 2 characters long.
            self.message.setText(
                "Tu apellido no puede tener menos de 2 caracteres.")
            print("lastName is too short")
            return

        for character in self.username.text():
            if character == " ":
                print("No spaces allowed in username")
                self.message.setText(
                    "No se pueden usar espacios en el nombre de usuario.")
                return

        if len(self.password.text()) < 6:
            # Password must be at least 6 characters long.
            self.message.setText(
                "La contraseña debe tener 6 caracteres como minimo.")
            print("password is too short")
            return

        if self.password.text() != self.passwordV.text():
            # Verify password and passwordV are exactly the same.
            self.message.setText("Las contraseñas no coinciden.")
            print("passwords are not the same.")
            return

        if Validators.validateEmail(self.email.text()) is False:
            # Verify email is valid.
            self.message.setText("El E-mail introducido no es valido.")
            print("Non Valid Email.")
            return

        if self.db.verifyUser(self.username.text(), self.mainW.cursor) is True:
            # Username was already registered.
            self.message.setText("Nombre de usuario no disponible.")
            print("Username already exists.")
            return

        # If all those tests were passed, now we prompt for a root user permission.
        if self.userType.currentIndex() == 0:
            minPrivilege = 0
        else:
            minPrivilege = 1

        dialog = Dialogs.CredentialsPromptD(self, self.userData, minPrivilege, self.mainW.cursor)

        if dialog.exec_() == QDialog.Accepted:
            self.registerUser()

    def registerUser(self):
        """Register the admin user data."""
        typeID = self.userType.currentIndex() + 1
        username = self.username.text()
        name = self.name.text()
        lastName = self.lastName.text()
        email = self.email.text()
        password = self.encrypt(self.password.text())
        registerDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registeredBy = self.data[0]

        data = [typeID, username, name, lastName,
                email, password, registerDate, registeredBy]
        columns = ["typeID", "username", "name", "lastName", "email",
                   "password", "registerDate", "registeredBy"]

        self.db.newUser(self.mainW.cursor, data, columns)
        self.db.logEntry(self.data[0], 0, [str(username), typeID], self.mainW.cursor)
        self.mainW.connection.commit()
        self.cancelBtn.click()
        # user = [ID, TYPE[ROOT=0, ADMIN=1, USER=2], USERNAME, NAME, LASTNAME]

    def userData(self, data):
        """Get the user data from the prompt."""
        self.data = data

    def encrypt(self, password):
        """Encrypt the password."""
        return hashpw(password.encode('utf8'), gensalt())
