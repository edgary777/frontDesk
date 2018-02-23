import Room
import Reservation
import Db


class RoomManager(object):
    """Rooms manager."""

    def __init__(self, parent, cursor):
        """Init."""
        self.db = Db.Db()
        self.cursor = cursor
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
        roomsD = self.db.getRooms(self.cursor)
        rooms = []
        for room in roomsD:
            rooms.append(Room.RoomD(room, self.parent, self.cursor))

        return rooms

    def getRoom(self, ID):
        """Return a room data object from it's ID."""
        return Room.RoomD(ID, self.parent, self.cursor)

    def roomsForDay(self, date, Type, amount):
        """Return data objects of free rooms on the passed date."""
        pass

    def roomsForPeriod(self, start, end):
        """Return list of free rooms.

        The rooms returned must be free during the whole period between start and end.
        """
        pass


class ReservationManager(object):
    """Reservation manager."""

    def __init__(self, parent, cursor):
        """Init."""
        self.db = Db.Db()
        self.cursor = cursor
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

    def getFinishedRsvs(self):
        """Return list of ReservationD Objects of finished reservations."""
        rsvIDs = self.db.selectFinishedRsvs(self.cursor)
        rsvs = []

        for rsv in rsvIDs:
            rsvs.append(
                Reservation.ReservationD(rsv[0], self.parent, self.cursor))

        for rsv in rsvs:
            rsv.assignRooms(self.cursor)

    def getActiveRsvs(self):
        """Return list of ReservationD Objects of finished reservations."""
        rsvIDs = self.db.selectActiveRsvs(self.cursor)
        rsvs = []

        for rsv in rsvIDs:
            rsvs.append(
                Reservation.ReservationD(rsv[0], self.parent, self.cursor))

        for rsv in rsvs:
            rsv.assignRooms(self.cursor)


class CheckInManager(object):
    """Check-Ins manager."""

    def __init__(self, parent, cursor):
        """Init."""
        self.db = Db.Db()
        self.cursor = cursor
        self.parent = parent

    def getToday(self):
        """Return data objects of the reservations that will Check-In today."""
        rsvD = self.db.getTodayCheckIns(self.cursor)
        reservations = []
        for rsvID in rsvD:
            reservations.append(
                Reservation.ReservationD(rsvID[0], self.parent, self.cursor))

        for rsv in reservations:
            rsv.assignRooms(self.cursor)

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

    def __init__(self, parent, cursor):
        """Init."""
        self.db = Db.Db()
        self.cursor = cursor
        self.parent = parent

    def getToday(self):
        """Return data objects of the reservations that will Check-Out today."""
        rsvD = self.db.getTodayCheckOuts(self.cursor)
        reservations = []
        for rsvID in rsvD:
            reservations.append(
                Reservation.ReservationD(rsvID[0], self.parent, self.cursor))

        return reservations

    def updateRoom(self, room):
        """Update room status."""
        pass

    def getCheckOut(self):
        """Return CheckIns for scroller."""
        pass
