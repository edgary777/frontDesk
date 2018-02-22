from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from DataItems import DataItem
import Room
import Db
import datetime
import Manager


class ReservationD(DataItem):
    """Data representation of a reservation."""

    def __init__(self, rsvID, cursor, parent):
        """Init."""
        super().__init__(parent)
        self.parent = parent
        self.cursor = cursor
        self.ID = rsvID
        # guestID == Passport, INE, driving license, etc...
        # otherGuests == People other than the one who made the reservation.
        self.items = [
            "rsvID", "guestID", "statusID", "userID", "companyID", "adults",
            "minors", "dateIn", "dateOut", "rate", "paid", "rsvgroup",
            "notes", "registerDate"
        ]

        for item in self.items:
            setattr(self, item, None)

        self.createFromID()

    def createFromID(self):
        """Init room from ID."""
        db = Db.Db()
        rsvData = db.getReservation(self.ID, self.cursor)
        x = 0
        for item in self.items:
            setattr(self, item, rsvData[x])
            x += 1

        # self.rsvID = self.ID
        self.rooms = db.getReservationRooms(self.rsvID, self.cursor)
        self.extras = db.getReservationExtras(self.rsvID, self.cursor)
        self.otherGuests = db.getReservationOGuests(self.rsvID, self.cursor)
        self.parking = db.getReservationParking(self.rsvID, self.cursor)
        self.roomIDs = db.getReservationRoomsIDs(self.rsvID, self.cursor)
        self.cursor = None

    def assignRooms(self, cursor=None):
        """Assign the rooms to the reservation."""
        # if there are rooms already occupied try and assign the room to the roomGroup
        # with the most occupied rooms. Rooms are grouped because they can share AC or
        # water heaters, so grouping them makes sense economically.
        # if there are no rooms already occupied, randomly assign it.

        # When instantiating a reservation it is passed a cursor object, but it is deleted
        # after a while because the connectionto the db needs to be closed.
        if self.cursor is None and not cursor is None:
            self.cursor = cursor
        else:
            print("Missing Cursor on reservation assignRooms")
            return
        if len(self.roomIDs) == 0:
            db = Db.Db()
            roomIDs = []
            for roomType in self.rooms:
                for room in range(roomType[3]):
                    din = datetime.datetime.strptime(self.dateIn, "%Y-%m-%d")
                    dout = datetime.datetime.strptime(self.dateOut, "%Y-%m-%d")
                    roomIDs.append(db.getBestRoom(din, dout, roomType[2], cursor))
            for room in roomIDs:
                db.insertRsvRoomID(self.rsvID, room, self.cursor)
            self.roomIDs = db.getReservationRoomsIDs(self.rsvID, self.cursor)
        self.cursor = None

    def getGuestName(self):
        """Return formatted name."""
        db = Db.Db()
        startConnection = db.startConnection()
        connection = startConnection[0]
        cursor = startConnection[1]

        guest = db.getGuest(self.guestID, cursor)
        db.endConnection(connection)
        return guest[2] + ", " + guest[1]

    def getNights(self):
        """Return the number of nights the guest is staying."""
        return 1

    def getTotal(self):
        """Return the total amount to be paid by the guest."""
        return self.getNights() * self.rate

    def getOwed(self):
        """Return the amount owed by the guest."""
        return 1

    def updatePaid(self):
        """Update the amount paid by the guest."""
        return 1

    def getMultiRoom(self):
        """Return room number."""
        if len(self.rooms) > 1:
            return len(self.rooms)
        else:
            return False

    def getRoomsIDs(self):
        """Return rooms IDs."""
        return self.roomIDs

    def getExtras(self):
        """Return the reservation extras"""
        return self.extras

    def gotNote(self):
        """Return True if there is a note, False if there isn't one."""
        if self.notes is not None:
            if self.notes != "":
                return True
            else:
                return False
        else:
            return False

    def getRoomForDashboard(self, parent):
        """Return room object for dashboard when not multiroom."""
        db = Db.Db()
        startConnection = db.startConnection()
        connection = startConnection[0]
        cursor = startConnection[1]

        room = Room.RoomD(self.roomIDs[0][2], cursor, parent)
        db.endConnection(connection)
        return room

class ReservationUi(QWidget):
    """Graphic representation of a reservation."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)
