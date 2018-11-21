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

    def __init__(self, cursor, connection):
        """Init."""
        super().__init__()

        self.startDb = Db.Db()
        self.session = None
        self.cursor = cursor
        self.user = None
        self.connection = connection
        # print(self.startDb.selectUsernames(self.cursor))

        self.setWindowTitle(self.getVersion())
        self.initUi()
        self.setStyleSheet("font-family: 'Roboto'; color: #333333;")

    def initUi(self):
        """Ui Setup."""
        layout = QVBoxLayout()
        # self.session = self.start()
        layout.addWidget(self.session)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.start()

    def start(self, user=None):
        """Start a session."""
        # If a user was passed, then use it to start a session.
        if user:
            self.user = user

        if self.user:
            print("Loggin in")
            self.session = Session.Session(self)
            self.changeDisplay(self.session)
            return

        # Checking for users with root privileges.

        verifyRoot = self.startDb.verifyRoot(self.cursor)
        if verifyRoot == 2 or verifyRoot is False:
            print("No root or no users at all, register root to keep going.")
            # No registered users, must create a root starting.
            widget = RootCreator(self, self)
            self.changeDisplay(widget)
            return

        # Checking for users with admin privileges.

        verifyAdmin = self.startDb.verifyAdmin(self.cursor)
        if verifyAdmin == 2:
            # For some reason there are no users, so we restart to prompt for root.
            # Raise Error to log message.
            print("No users registered?? restarted to try to prompt for new root.")
            self.start()
            return
        elif verifyAdmin is False:
            # No registered admin users, must create an admin starting.
            print("There's a root, but not an admin, register an admin to keep going.")
            widget = AdminCreator(self, self)
            self.changeDisplay(widget)
            return
        elif verifyAdmin:
            # login prompt.
            print("There's a registered admin and a registered root. Login to start.")
            widget = Login(self, self)
            self.changeDisplay(widget)
            return

    def changeDisplay(self, widget):
        """Change what is being displayed on the main window."""
        # Remove the currently displayed widget on the passed window layout.
        toRemoveWI = self.layout().takeAt(0)  # QWidgetItem
        if toRemoveWI is None:
            print("There was no item to remove.")
            # The window is empty, add the widget without removing.
            self.layout().addWidget(widget)
            return
        # Set the widget for garbage collection.
        toRemoveW = toRemoveWI.widget()  # QWidget
        toRemoveW.setParent(None)
        # set a the new widget on the passed window.
        self.layout().addWidget(widget)

    def logout(self):
        """Log out and show the login screen."""
        if self.user is not None:
            # for i in reversed(range(self.layout.count())):
            #     self.layout.itemAt(i).widget().deleteLater()
            self.user = None
            self.setWindowTitle(self.getVersion())
            widget = Login(self, self)
            self.changeDisplay(widget)

    def getVersion(self):
        """Return the last version number used on the changelog."""
        with open("CHANGELOG.md", "r") as version:
            for line in version:
                if line[:2] == "##":
                    if line[:14] == "## Unreleased ":
                        return "V" + line[14:]
                    elif line[:4] == "## V":
                        return "V" + line[4:]

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
window = MainWindow(cursor, connection)
# Having a fixed size for the windows makes it unable to be maximized
# window.setMaximumWidth(1380)
window.showMaximized()
sys.exit(app.exec_())
