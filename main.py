import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt
import Session


class MainWindow(QWidget):
    """Main window widget."""

    def __init__(self):
        """Init."""
        super().__init__()

        self.session = None

        self.initUi()

    def initUi(self):
        """Ui Setup."""
        self.session = self.start()
        layout = QVBoxLayout()
        layout.addWidget(self.session)

        self.setLayout(layout)

    def start(self, user=None):
        """Start a session."""
        # user = [ID, NAME, TYPE[ADMIN=0, USER=1]]
        if not user:
            # Prompt for user login data and verify credentials in db
            user = [0, "Edgar", 0]
        return Session.Session(user, self)

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


app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
sys.exit(app.exec_())
