"""Menu bar for the main screen."""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import Buttons


class MenuBar(QWidget):
    """Menu bar object."""

    def __init__(self, items, parent):
        """Init."""
        super().__init__(parent)

        self.items = items

        self.initUi()

    def initUi(self):
        """Ui Setup."""
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setFixedHeight(120)
        self.setMinimumHeight(100)
        self.setMaximumHeight(150)
        self.setMinimumWidth(800)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.color = [self.rando(), self.rando(), self.rando()]
        buttons = self.generateButtons(self.items)

        layout.addLayout(buttons)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # layout.addStretch()

    def generateButtons(self, items):
        """Return layout with buttons."""
        x = 0
        colorRGB = self.color
        layout = QHBoxLayout()
        layout.setSpacing(0)

        # Here we make the gradient style for the buttons.
        # We start with a base color and make it lighter, but we must invert the order
        # of the buttons first so the lighter color is on top.
        btns = []
        for i in reversed(items):
            # self.color is a list of rgb values, we must make it a CSV string
            color = ",".join(str(e) for e in colorRGB)
            label = str(i)
            icon = "Resources\c-close.png"
            setattr(self, "btn" + str(x),
                    Buttons.MenuBarBtn(color, label, icon, self))
            btns.append(getattr(self, "btn" + str(x)))
            # layout.addWidget(getattr(self, "btn" + str(x)))
            li = []
            for item in colorRGB:
                li.append(round(item * 1.1))
            colorRGB = li
            x += 1
        for btn in reversed(btns):
            layout.addWidget(btn)

        # layout.addStretch()
        return layout

    def rando(self):
        """Retur random integer."""
        return random.randint(0, 187)

    def getWidth(self):
        """Return width."""
        self.layout().update()
        self.layout().activate()
        return self.width()

    def getHeight(self):
        """Return width."""
        self.layout().update()
        self.layout().activate()
        return self.height()

    def getMiddle(self, items):
        """Return the item with the middle value."""
        ma = max(items)
        mi = min(items)
        for item in items:
            if item != ma and item != mi:
                return item

    def shiftColor(self, items):
        """Shift the color."""
        mid = self.getMiddle(items)
        index = items.index(mid)
        shifted = items[:]
        shifted[index] += 20

        return shifted

    def paintEvent(self, event):
        """Set window background color."""
        # shifted = self.shiftColor(self.color)
        color = self.color
        color = QColor(qRgb(color[0], color[1], color[2]))
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def resizeEvent(self, event):
        """Resize Event."""
        width = self.width() / 4
        width = 200 if width < 200 else width
        x = 0
        for i in reversed(self.items):
            getattr(self, "btn" + str(x)).resizeMe(width)
            x += 1
