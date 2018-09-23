"""Coordinator for the interactions with the data."""
import Db
import datetime
from colorama import Fore, Style


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
        print(Fore.GREEN)
        print("assignRoom")
        print("I got this data to assign a room:")
        print(reservation)
        print("starting the process")
        print(Style.RESET_ALL)
        if self.db.getReservationRoom(reservation, self.cursor)[0][0] is None:
            print(Fore.GREEN)
            print("The reservation had no room, assigning one ...")
            print(Style.RESET_ALL)
            roomType = self.db.getReservationRoomType(reservation, self.cursor)[0]
            din = datetime.datetime.strptime(reservation[7], "%Y-%m-%d")
            dout = datetime.datetime.strptime(reservation[8], "%Y-%m-%d")
            room = self.db.getBestRoom(din, dout, roomType, self.cursor)
            self.db.updateRsvRoomID(reservation[0], room, self.cursor)
            print(Fore.GREEN)
            print("The room was assigned correctly")
        else:
            print(Fore.GREEN)
            print("Nothing to do here, the reservation already has a room")
        print(Style.RESET_ALL)


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
        print(Fore.GREEN)
        print("getRooms")
        print("Hi, I should give you a list of all the rooms in the hotel.")
        print("communicating with the database")
        print(Style.RESET_ALL)
        rooms = self.db.getRooms(self.cursor)
        print(Fore.GREEN)
        print("finished communicating with the database")

        print("This is the data I'll return.")
        print(rooms)

        print(Style.RESET_ALL)

        return rooms

    def getRoom(self, ID):
        """Return a room data object from it's ID."""
        print(Fore.GREEN)
        print("getRooms")
        print("Hi, I should give you a list of all the rooms in the hotel.")
        print("communicating with the database")
        print(Style.RESET_ALL)
        room = self.db.getRoom(ID, self.cursor)
        print(Fore.GREEN)
        print("finished communicating with the database")

        print("This is the data I'll return.")
        print(room)

        print(Style.RESET_ALL)
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
        print(Fore.GREEN)
        print("getActiveRsvs")
        print("Hi, I should give you a list of ongoing reservations that already checked in")
        print("communicating with the database")
        print(Style.RESET_ALL)
        rsvIDs = self.db.selectActiveRsvs(self.cursor)
        print(Fore.GREEN)
        rsvs = []
        print("This are the reservations I got from the database.")
        print(rsvIDs)

        if rsvIDs:
            print("I will now append the data of each reservation to a list.")
            for rsv in rsvIDs:
                print("communicating with the database")
                print(Style.RESET_ALL)
                data = self.db.getReservation(rsv, self.cursor)
                print(Fore.GREEN)
                print("Appending this data to the list:")
                print(data)
                rsvs.append(data)
            print("Finished creating the list.")
            print("The list looks like this:")
            print(rsvs)

            # To be honest I don't know why there's a room assigner in here, I'll leave it
            # for the time being, but I think it should be removed once everything else is
            # working correctly.
            print("I'll now assign a room to the reservations that don't have one.")
            for rsv in rsvs:
                print("passing this data to get a room if needed:")
                print(rsv)
                self.assignRoom(rsv)
            print("Finished Assigning rooms.")
        else:
            print("Apparently there are no currently ongoing reservations.")
        print("I'm done here, bye")

        print(Style.RESET_ALL)


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
