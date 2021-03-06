from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class PicBtn(QAbstractButton):
    """Image button with static, hovered, and clicked states.

    Functionality is mostly the same as QPushButton.
    """

    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent,
                 actionL=None, actionR=None, fWidth=None, fHeight=None):
        """Init."""
        super().__init__(parent)
        self.pixmap = QPixmap(pixmap)
        self.pixmap_hover = QPixmap(pixmap_hover)
        self.pixmap_pressed = QPixmap(pixmap_pressed)

        self.actionL = actionL
        self.actionR = actionR

        self.fWidth = fWidth
        self.fHeight = fHeight

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def enterEvent(self, event):
        """Enter event."""
        self.update()

    def leaveEvent(self, event):
        """Leave event."""
        self.update()

    def setActionL(self, action):
        """Set left mouse button acton."""
        self.actionL = action

    def setActionR(self, action):
        """Set right mouse button acton."""
        self.actionR = action

    def fixedDimentions(self):
        """Set fixed dimentions if defined by user."""
        if self.fWidth:
            self.setFixedWidth(self.fWidth)
        if self.fHeight:
            self.setFixedHeight(self.fHeight)

    def mousePressEvent(self, QMouseEvent):
        """Reimplement mouse events."""
        if QMouseEvent.button() == Qt.LeftButton:
            self.setDown(not self.isDown())
            if self.actionL:
                self.actionL()
        elif QMouseEvent.button() == Qt.RightButton:
            if self.actionR:
                self.actionR()

    def sizeHint(self):
        """Size hint."""
        return self.pixmap.size()

    def paintEvent(self, event):
        """Paint Event."""
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)


class SimpleBtn(QAbstractButton):
    """
    Simple Button.

    Color MUST be an rgb string array (eg. red = "255, 0, 0")

    style is a stylesheet as 'QLabel { color : black;'
    """

    def __init__(self, width, height, rounded, color, label, style,
                 parent, growH=False, growV=False, actionL=None,
                 actionR=None):
        """Init."""
        super().__init__(parent)

        self.widths = width
        self.heights = height
        self.rounded = rounded

        col = [int(color.strip()) for color in color.split(',')]
        self.color = QColor(qRgb(col[0], col[1], col[2]))
        self.label = label

        self.actionL = actionL
        self.actionR = actionR

        # Button will not grow unless specified in the parameters.
        if growH is True and growV is True:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        elif growH is True:
            self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        elif growV is True:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        else:
            self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        label = QLabel(self.label)
        label.setStyleSheet(style)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def setActionL(self, action):
        """Set left mouse button acton."""
        self.actionL = action

    def setActionR(self, action):
        """Set right mouse button acton."""
        self.actionR = action

    def mousePressEvent(self, QMouseEvent):
        """Reimplement mouse events."""
        if QMouseEvent.button() == Qt.LeftButton:
            self.setDown(not self.isDown())
            if self.actionL:
                self.actionL()
        elif QMouseEvent.button() == Qt.RightButton:
            if self.actionR:
                self.actionR()

    def paintEvent(self, event):
        """Paint Event."""
        # If the mouse is over the button make the color lighter
        color = self.color.lighter(130) if self.underMouse() else self.color

        # If the button is being pressed then make it darker
        if self.isDown():
            color = self.color.darker(110)

        # Set up the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create the path for the figure
        path = QPainterPath()
        path.addRoundedRect(
            QRectF(0.0, 0.0, self.width(), self.height()), self.rounded,
            self.rounded)

        # Fill the paths with color
        painter.fillPath(path, color)

    def minimumSizeHint(self):
        """Set the minimum size hint."""
        return QSize(self.widths, self.heights)


class MenuBarBtn(QAbstractButton):
    """
    Menu Bar Button.

    Color MUST be an rgb string array (eg. red = "255, 0, 0")

    icon must be a png file with transparent background.
    """

    def __init__(self, color, label, parent, icon=None, actionL=None, actionR=None):
        """Init."""
        super().__init__(parent)

        self.parent = parent
        self.widths = self.parent.getWidth()
        self.heights = self.widths / 4

        col = [int(color.strip()) for color in color.split(',')]
        self.color = QColor(qRgb(col[0], col[1], col[2]))
        self.label = label

        self.icon = icon

        self.actionL = actionL
        self.actionR = actionR

        self.initUi()

    def initUi(self):
        """Ui Setup."""
        self.setMinimumHeight(35)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if self.icon:
            iconSize = 30

            pixmap = QPixmap(self.icon)
            pixmap = pixmap.scaled(iconSize, iconSize, Qt.KeepAspectRatio)
            icon = QLabel()
            icon.setPixmap(pixmap)
            # icon.setFixedSize(iconSize + 10, iconSize + 10)
            icon.setAlignment(Qt.AlignCenter)

        self.qlabel = QLabel(self.label)
        self.qlabel.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()
        layout.addStretch()
        if self.icon:
            layout.addWidget(icon)
        layout.addWidget(self.qlabel)
        layout.addStretch()
        self.setLayout(layout)

    def setActionL(self, action):
        """Set left mouse button acton."""
        self.actionL = action

    def setActionR(self, action):
        """Set right mouse button acton."""
        self.actionR = action

    def mousePressEvent(self, QMouseEvent):
        """Reimplement mouse events."""
        if QMouseEvent.button() == Qt.LeftButton:
            self.setDown(not self.isDown())
            if self.actionL:
                self.actionL()
        elif QMouseEvent.button() == Qt.RightButton:
            if self.actionR:
                self.actionR()

    def paintEvent(self, event):
        """Paint Event."""
        self.setAutoFillBackground(True)

        # If the mouse is over the button make the color lighter
        color = self.color.lighter(130) if self.underMouse() else self.color

        # If the button is being pressed then make it darker
        if self.isDown():
            color = self.color.darker(130)

        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def resizeMe(self, width):
        """Resize the button."""
        self.setMaximumWidth(width)

    def resizeEvent(self, event):
        """Resize Event."""
        height = self.parent.getHeight()
        self.setMaximumHeight(height)
        size = self.width() * 0.08
        size = "7" if size < 7 else str(size)
        style = """QLabel{{
            color: white;
            font-weight: bold;
            font-size: {}pt;
        }}""".format(size)
        self.qlabel.setStyleSheet(style)

    # def minimumSizeHint(self):
    #     """Set the minimum size hint."""
    #     return QSize(self.widths, self.heights)
