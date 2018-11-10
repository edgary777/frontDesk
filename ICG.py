"""Initial Credentials Generator."""
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
# Disable


def blockPrint():
    """Disable printing to terminal."""
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    """Enable printing to terminal."""
    sys.stdout = sys.__stdout__


class RootCreator(QWidget):
    """Login window shown at startup to create a root user."""

    def __init__(self, parent, restart, cursor):
        """Init."""
        super().__init__(parent)

        self.cursor = cursor

        self.restart = restart

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

        title = QLabel("Crear Usuario Root")
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

        self.accept = QPushButton("ACEPTAR")
        self.accept.clicked.connect(lambda: self.registerUser())
        # self.accept.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.accept.setStyleSheet(self.buttonStyle)

        self.passwordV = QLineEdit()
        self.passwordV.setTextMargins(buttonPadding)
        self.passwordV.setPlaceholderText("Verificar Contraseña")
        self.passwordV.setAlignment(Qt.AlignCenter)
        self.passwordV.setStyleSheet(self.inputStyle)
        self.passwordV.setEchoMode(QLineEdit.Password)
        self.passwordV.returnPressed.connect(self.accept.click)

        self.message = QLabel()
        self.message.setStyleSheet(self.messageStyle)
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setWordWrap(True)
        self.message.setMinimumHeight(16)

        # enter events to go to the next field.
        self.username.returnPressed.connect(self.password.setFocus)
        self.password.returnPressed.connect(self.passwordV.setFocus)


        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.passwordV)
        layout.addWidget(self.accept)
        layout.addWidget(self.message)
        layout.addStretch()

        self.setLayout(layout)
        self.username.setFocus()

    def registerUser(self):
        """Register root user when the accept button is pressed."""
        if self.password.text() == "" or self.passwordV.text() == "" or self.username.text() == "":
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

        if self.db.verifyUser(self.username.text(), self.cursor) is True:
            # Username was already registered.
            self.message.setText("Nombre de usuario no disponible.")
            print("Username already exists.")
            return
        # If all those tests were passed, now the root user can be registered.

        userTypeId = 0
        userDescription = "Root"
        userLongDescription = "User with complete access privileges."
        self.db.newUserTypeDef(
            self.cursor, [userTypeId, userDescription, userLongDescription])

        typeID = 0
        username = self.username.text()
        password = self.encrypt(self.password.text())
        registerDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registeredBy = self.username.text()

        data = [typeID, username, password, registerDate, registeredBy]
        columns = ["typeID", "username",
                   "password", "registerDate", "registeredBy"]

        self.db.newUser(self.cursor, data, columns)

        self.restart()

    def encrypt(self, password):
        """Encrypt the password."""
        return hashpw(password.encode('utf8'), gensalt())


class AdminCreator(QWidget):
    """Login window shown at startup to create an admin user."""

    def __init__(self, parent, restart, cursor):
        """Init."""
        super().__init__(parent)

        self.restart = restart
        self.cursor = cursor

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

        title = QLabel("Crear Administrador")
        title.setStyleSheet(self.titleStyle)
        title.setAlignment(Qt.AlignCenter)

        buttonPadding = QMargins(10, 0, 10, 0)

        self.username = QLineEdit()
        self.username.setTextMargins(buttonPadding)
        self.username.setPlaceholderText("Usuario")
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setStyleSheet(self.inputStyle)

        self.name = QLineEdit()
        self.name.setTextMargins(buttonPadding)
        self.name.setPlaceholderText("Nombre")
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setStyleSheet(self.inputStyle)

        self.lastName = QLineEdit()
        self.lastName.setTextMargins(buttonPadding)
        self.lastName.setPlaceholderText("Apellidos")
        self.lastName.setAlignment(Qt.AlignCenter)
        self.lastName.setStyleSheet(self.inputStyle)

        # The previous fields need some validation to ensure the data is not garbage.

        self.email = QLineEdit()
        self.email.setTextMargins(buttonPadding)
        self.email.setPlaceholderText("E-Mail")
        self.email.setAlignment(Qt.AlignCenter)
        self.email.setStyleSheet(self.inputStyle)

        self.password = QLineEdit()
        self.password.setTextMargins(buttonPadding)
        self.password.setPlaceholderText("Contraseña")
        self.password.setAlignment(Qt.AlignCenter)
        self.password.setStyleSheet(self.inputStyle)
        self.password.setEchoMode(QLineEdit.Password)

        self.accept = QPushButton("ACEPTAR")
        self.accept.clicked.connect(
            lambda: self.rootPrompt(self.password.text()))
        # self.accept.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.accept.setStyleSheet(self.buttonStyle)

        self.passwordV = QLineEdit()
        self.passwordV.setTextMargins(buttonPadding)
        self.passwordV.setPlaceholderText("Verificar Contraseña")
        self.passwordV.setAlignment(Qt.AlignCenter)
        self.passwordV.setStyleSheet(self.inputStyle)
        self.passwordV.setEchoMode(QLineEdit.Password)
        self.passwordV.returnPressed.connect(self.accept.click)

        self.message = QLabel()
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

        # textChanged signals to clean alert message on edit.
        self.username.textEdited.connect(lambda: self.message.setText(""))
        self.name.textEdited.connect(lambda: self.message.setText(""))
        self.lastName.textEdited.connect(lambda: self.message.setText(""))
        self.email.textEdited.connect(lambda: self.message.setText(""))
        self.password.textEdited.connect(lambda: self.message.setText(""))

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.name)
        layout.addWidget(self.lastName)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.passwordV)
        layout.addWidget(self.accept)
        layout.addWidget(self.message)
        layout.addStretch()

        self.setLayout(layout)
        self.username.setFocus()

    def rootPrompt(self, password):
        """Prompt for root credentials to create new admin user."""
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

        if self.db.verifyUser(self.username.text(), self.cursor) is True:
            # Username was already registered.
            self.message.setText("Nombre de usuario no disponible.")
            print("Username already exists.")
            return

        # If all those tests were passed, now we prompt for a root user permission.

        dialog = Dialogs.RootCredentialsD(self, self.userData, self.cursor)

        if dialog.exec_() == QDialog.Accepted:
            self.registerUser()

    def registerUser(self):
        """Register the admin user data."""
        userTypeId = 1
        userDescription = "Admin"
        userLongDescription = "User with administrator privileges."
        self.db.newUserTypeDef(
            self.cursor, [userTypeId, userDescription, userLongDescription])

        typeID = 1
        username = self.username.text()
        name = self.name.text()
        lastName = self.lastName.text()
        email = self.email.text()
        password = self.encrypt(self.password.text())
        registerDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registeredBy = self.username.text()

        data = [typeID, username, name, lastName,
                email, password, registerDate, registeredBy]
        columns = ["typeID", "username", "name", "lastName", "email",
                   "password", "registerDate", "registeredBy"]

        self.db.newUser(self.cursor, data, columns)
        # user = [ID, TYPE[ROOT=0, ADMIN=1, USER=2], USERNAME, NAME, LASTNAME]
        userData = self.db.getUser(username, self.cursor)
        user = [userData[0], userData[1],
                userData[2], userData[3], userData[4]]
        self.restart(user)

    def userData(self, data):
        """Get the user data from the prompt."""
        self.data = data

    def encrypt(self, password):
        """Encrypt the password."""
        return hashpw(password.encode('utf8'), gensalt())
