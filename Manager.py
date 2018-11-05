"""Coordinator for the interactions with the data."""
import Db
import datetime


class superManager(object):
    """Parent Class for the managers."""

    def assignRoom(self, reservation):
        """
        Assign a room to the reservation.

        Input: List or tuple of reservation data where the item 0 is a reservation ID
        Output: None
        """
        # if there are rooms already occupied try and assign the room to the roomGroup
        # with the most occupied rooms. Rooms are grouped because they can share AC or
        # water heaters, so grouping them makes sense economically.
        # if there are no rooms already occupied, randomly assign it.
        if self.db.getReservationRoom(reservation, self.cursor)[0][0] is None:
            roomType = self.db.getReservationRoomType(reservation, self.cursor)[0]
            din = datetime.datetime.strptime(reservation[7], "%Y-%m-%d")
            dout = datetime.datetime.strptime(reservation[8], "%Y-%m-%d")
            room = self.db.getBestRoom(din, dout, roomType, self.cursor)
            self.db.updateRsvRoomID(reservation[0], room, self.cursor)
        else:
            pass
            # print("Nothing to do here, the reservation already has a room")


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
        """Return room data for scroller.

        Input: None
        Output: Returns a list of all the rooms in the hotel, each item is a roomNo.
        """
        rooms = self.db.getRooms(self.cursor)

        return rooms

    def getRoom(self, ID):
        """Return a room data object from it's ID."""
        room = self.db.getRoom(ID, self.cursor)
        return room

    def roomsForDay(self, date, Type, amount):
        """Return data objects of free rooms on the passed date."""
        pass

    def roomsForPeriod(self, start, end):
        """Return list of free rooms.

        The rooms returned must be free during the whole period between start and end.
        """
        pass


class ReservationManager(superManager):
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
        """Return list of finished reservations."""
        rsvIDs = self.db.selectFinishedRsvs(self.cursor)
        reservations = []

        for rsvID in rsvIDs:
            reservation = self.db.getReservation(rsvID, self.cursor)
            self.assignRoom(reservation)
            reservations.append(reservation)

    def getActiveRsvs(self):
        """Return list of ongoing checked in reservations."""
        rsvIDs = self.db.selectActiveRsvs(self.cursor)
        rsvs = []

        if rsvIDs:
            for rsv in rsvIDs:
                data = self.db.getReservation(rsv, self.cursor)
                rsvs.append(data)

            # To be honest I don't know why there's a room assigner in here, I'll leave it
            # for the time being, but I think it should be removed once everything else is
            # working correctly.
            for rsv in rsvs:
                self.assignRoom(rsv)
        else:
            # print("Apparently there are no current ongoing reservations.")
            pass


class CheckInManager(superManager):
    """Check-Ins manager."""

    def __init__(self, parent, cursor):
        """Init."""
        self.db = Db.Db()
        self.cursor = cursor
        self.parent = parent

    def getToday(self):
        """Return the data of the reservations that will Check-In today."""
        rsvNumbers = self.db.getTodayCheckIns(self.cursor)
        reservations = []

        for rsvID in rsvNumbers:
            reservation = self.db.getReservation(rsvID, self.cursor)
            self.assignRoom(reservation)
            reservation = self.db.getReservation(rsvID, self.cursor)
            guest = self.db.getGuest(reservation[1], self.cursor)
            reservations.append([reservation, guest])

        # for rsv in reservations:
        #     self.assignRoom(rsv)
        #
        # reservations =[]
        # for rsvID in rsvNumbers:
        #     reservation = self.db.getReservation(rsvID, self.cursor)
        #     reservations.append(reservation)

        return reservations

    def updateRoom(self, room):
        """Update room status."""
        pass

    def getCheckIn(self):
        """Return CheckIns for scroller."""
        pass


class CheckOutManager(superManager):
    """CheckOuts manager."""

    def __init__(self, parent, cursor):
        """Init."""
        self.db = Db.Db()
        self.cursor = cursor
        self.parent = parent

    def getToday(self):
        """Return the data of the reservations that will Check-Out today."""
        rsvNumbers = self.db.getTodayCheckOuts(self.cursor)
        reservations = []

        for rsvID in rsvNumbers:
            reservation = self.db.getReservation(rsvID, self.cursor)
            self.assignRoom(reservation)
            reservation = self.db.getReservation(rsvID, self.cursor)
            guest = self.db.getGuest(reservation[1], self.cursor)
            reservations.append([reservation, guest])

        return reservations

    def updateRoom(self, room):
        """Update room status."""
        pass

    def getCheckOut(self):
        """Return CheckIns for scroller."""
        pass
