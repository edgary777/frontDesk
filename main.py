"""Main file."""

import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt
import Session
import Db
import atexit
import logging
import inspect

# Logging errors to a file should only happen when the program has been freezed.
# The logging will only be used when the file path and python path are the same.

# Find the file path and split it to a list.
filePath = inspect.stack()[0][1].split('/')
# Remove the file from the path to get the directory.
del filePath[len(filePath) - 1]
# Turn the path into a string again.
filePath = "/".join(filePath)

if os.path.dirname(sys.executable) == filePath:

    logging.basicConfig(filename=os.path.dirname(sys.executable) + '/tmp/myapp.log',
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

        self.session = None
        self.cursor = cursor

        self.initUi()

    def initUi(self):
        """Ui Setup."""
        self.session = self.start()
        layout = QVBoxLayout()
        layout.addWidget(self.session)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

    def start(self, user=None):
        """Start a session."""
        # user = [ID, NAME, TYPE[ADMIN=0, USER=1]]
        if not user:
            # Prompt for user login data and verify credentials in db
            user = [0, "Edgar", 0]
        return Session.Session(user, self, self.cursor)

    def restart(self):
        """Restart the session."""
        self.session.setParent(None)
        self.session.deleteLater()
        # Prompt for user login data and verify credentials in db
        user = [0, "Edgar", 0]
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


debugPrint = False

if debugPrint is False:
    blockPrint()
else:
    enablePrint()

debugDb = False

if debugDb:
    exists = os.path.isfile("database.db")
    if exists:
        os.remove("database.db")

db = Db.Db()

if debugDb:
    dummy = Db.dummyDb()
    dummy.dummyDB()


startConnection = db.startConnection()
connection = startConnection[0]
cursor = startConnection[1]

atexit.register(db.endConnection, connection)

app = QApplication(sys.argv)
window = MainWindow(cursor)
window.showMaximized()
sys.exit(app.exec_())
