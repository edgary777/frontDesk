import Room
import Reservation
import People
import random
import datetime
import Db


class RoomManager(object):
    """Rooms manager."""

    def __init__(self, parent):
        """Init."""
        self.db = Db.Db()
        self.parent = parent

    def updateRoom(self, room):
        """Update room status."""
        pass

    def occupyRoom(self, room):
        """Mark room as occupied."""
        pass

    def freeRoom(self, room):
        """Mark room as unoccupied."""
        pass

    def getRooms(self):
        """Return room data objects for scroller."""
        startConnection = self.db.startConnection()
        connection = startConnection[0]
        cursor = startConnection[1]

        roomsD = self.db.getRooms(cursor)
        rooms = []
        for room in roomsD:
            rooms.append(Room.RoomD(room, cursor, self.parent))

        self.db.endConnection(connection)
        return rooms

    def getRoom(self, ID):
        """Return a room data object from it's ID."""
        return Room.RoomD(ID, self.parent)

    def roomsForDay(self, date, Type, amount):
        """Return data objects of free rooms on the passed date."""
        db = Db.Db()
        rooms = db.getRooms()
        roomsD = db.getFreeRoomsForDay(date)
        roomsID = []
        if roomsD[Type] >= amount:
            for i in range(amount):
                for roomNo in rooms:
                    roomsID.append(ID)
        return roomsID

    def roomsForPeriod(self, start, end):
        """Return list of free rooms.

        The rooms returned must be free during the whole period between start and end.
        """
        pass


class ReservationManager(object):
    """Reservation manager."""

    def __init__(self, parent):
        """Init."""
        self.parent = parent

    def makeReservation(self):
        """Make a new a reservation."""
        pass

    def dataFromID(self, ID):
        """Return reservation from an ID."""
        pass

    def editReservation(self, ID):
        """Edit a reservation."""
        pass

    def cancelReservation(self, ID):
        """Edit a reservation."""
        pass

    def getFreeRooms(self, day):
        """Return list of free room slots by type."""
        pass


class CheckInManager(object):
    """Check-Ins manager."""

    def __init__(self, parent):
        """Init."""
        self.db = Db.Db()
        self.parent = parent

    def getToday(self):
        """Return data objects of the reservations that will Check-In today."""
        startConnection = self.db.startConnection()
        connection = startConnection[0]
        cursor = startConnection[1]

        rsvD = self.db.getTodayCheckIns(cursor)
        reservations = []
        for rsvID in rsvD:
            reservations.append(Reservation.ReservationD(rsvID[0], cursor, self.parent))

        for rsv in reservations:
            rsv.assignRooms(cursor)

        self.db.endConnection(connection)
        return reservations

    def updateRoom(self, room):
        """Update room status."""
        pass

    def assignRoom(self):
        """Assign a room to the reservations missing one."""
        pass

    def getCheckIn(self):
        """Return CheckIns for scroller."""
        pass


class CheckOutManager(object):
    """CheckOuts manager."""

    def __init__(self, db, parent):
        """Init."""
        self.db = db
        self.parent = parent

    def getToday(self):
        """Return data objects of the reservations that will Check-Out today."""
        db = Db.Db(self.db)
        rsvD = db.getTodayCheckOuts()
        rsvs = []
        for rsv in rsvD:
            rsvs.append(Reservation.ReservationD(rsv, self.db, self.parent))
        return rsvs

    def updateRoom(self, room):
        """Update room status."""
        pass

    def getCheckOut(self):
        """Return CheckIns for scroller."""
        pass
