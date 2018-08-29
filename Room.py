from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from DataItems import DataItem
import Db


class RoomD(DataItem):
    """Data representation of a room."""

    def __init__(self, roomNo, parent, cursor):
        """Init."""
        super().__init__(parent)

        self.ID = roomNo

        self.cursor = cursor
        self.db = Db.Db()

        self.items = [
            "roomNo", "roomType", "roomTypeDesc", "beds", "maxCapacity", "extras",
            "status", "notes", "roomTypeLongDesc"
            ]

        for item in self.items:
            setattr(self, item, None)

        self.roomFromId()

    def roomFromId(self):
        """Init room from ID."""
        roomData = self.db.getRoom(self.ID, self.cursor)
        roomTypeData = self.db.getRoomType(roomData[1], self.cursor)
        roomExtrasData = self.db.getRoomExtras(self.ID, self.cursor)

        self.roomNo = self.ID
        self.roomType = roomTypeData[0]
        self.roomTypeDesc = roomTypeData[1]
        self.beds = roomTypeData[2]
        self.maxCapacity = roomTypeData[3]
        self.roomTypeLongDesc = roomTypeData[4]
        self.extras = [room[2] for room in roomExtrasData]
        self.status = roomData[2]
        self.notes = roomData[4]

    def gotNote(self):
        """Return True if there is a note, False if there isn't one."""
        if self.notes is not None:
            if self.notes != "":
                return True
            else:
                return False
        else:
            return False


class RoomUi(QWidget):
    """Graphic representation of a room."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)
