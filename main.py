"""Main file."""
import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt
import Db
import atexit
import logging
import inspect
import Session
from Login import Login
from ICG import RootCreator, AdminCreator

# Logging errors to a file should only happen when the program has been freezed.
# The logging will only be used when the file path and python path are the same.

# Find the file path and split it to a list.
filePath = inspect.stack()[0][1].split('/')
# Remove the file from the path to get the directory.
del filePath[len(filePath) - 1]
# Turn the path into a string again.
filePath = "/".join(filePath)

if os.path.dirname(sys.executable) == filePath:

    logging.basicConfig(filmoveename=os.path.dirname(sys.executable) + '/errors.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger('mylogger')

    def my_handler(type, value, tb):
        """Error handler."""
        logger.exception("Uncaught exception: {0}".format(str(value)))

    sys.excepthook = my_handler


class MainWindow(QWidget):
    """Main window widget."""

    def __init__(self, cursor):
        """Init."""
        super().__init__()

        self.startDb = Db.Db()
        self.session = None
        self.cursor = cursor
        print(self.startDb.selectUsernames(self.cursor))
        self.setWindowTitle("V0.6.0")

        self.initUi()
        self.setStyleSheet("font-family: 'Roboto'; color: #333333;")

    def initUi(self):
        """Ui Setup."""
        layout = QVBoxLayout()
        self.session = self.start()
        layout.addWidget(self.session)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

    def start(self, user=None):
        """Start a session."""
        if user:
            print("Loggin in")
            return Session.Session(user, self, self.cursor)

        verifyRoot = self.startDb.verifyRoot(self.cursor)
        if verifyRoot == 2 or verifyRoot is False:
            print("No root or no users, register root to keep going.")
            # No registered users, must create a root starting.
            self.Root = RootCreator(self, self.restart, cursor)
            return self.Root

        verifyAdmin = self.startDb.verifyAdmin(self.cursor)
        if verifyAdmin == 2:
            # For some reason there are no users, so we restart to prompt for root.
            # Raise Error to log message.
            print("No users registered?? restarted to try to prompt for new root.")
            self.restart()
        elif verifyAdmin is False:
            print("There's a root but not an admin, register an admin to keep going.")
            # No registered admin users, must create an admin starting.
            self.Admin = AdminCreator(self, self.restart, self.cursor)
            return self.Admin
        elif verifyAdmin:
            print("There's a registered admin and a registered root, login to start.")
            # login prompt.
            self.login = Login(self, self.restart, self.cursor)
            return self.login

    def restart(self, user=None):
        """Restart the session."""
        self.session.setParent(None)
        self.session.deleteLater()
        # Prompt for user login data and verify credentials in db
        if not user:
            self.start()
        # user = [ID, TYPE[ROOT=0, ADMIN=1, USER=2]]
        self.session = self.start(user)
        self.layout().addWidget(self.session)

    def paintEvent(self, event):
        """Set window background color."""
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)


# Disable
def blockPrint():
    """Disable printing to terminal."""
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    """Enable printing to terminal."""
    sys.stdout = sys.__stdout__


debugPrint = True

if debugPrint is False:
    blockPrint()
else:
    enablePrint()

debugDb = False

if debugDb:
    exists = os.path.isfile("database.db")
    if exists:
        os.remove("database.db")

    exists = os.path.isfile("database.db-journal")
    if exists:
        os.remove("database.db-journal")

db = Db.Db()

# if debugDb:
#     dummy = Db.dummyDb()
#     dummy.dummyDB()

startConnection = db.startConnection()
connection = startConnection[0]
cursor = startConnection[1]

atexit.register(db.endConnection, connection)

app = QApplication(sys.argv)
window = MainWindow(cursor)
# Having a fixed size for the windows makes it unable to be maximized
# window.setMaximumWidth(1380)
window.showMaximized()
sys.exit(app.exec_())
