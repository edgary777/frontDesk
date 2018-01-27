from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ReservationD(QWidget):
    """Data representation of a reservation."""

    def __init__(self, guest, rooms, user, data, parent):
        """Init."""
        super().__init__(parent)

        self.guest = guest
        self.rooms = rooms  # 1 reservation can comprise multiple rooms.
        self.user = user  # The user who made the reservation.
        self.data = data

        # guestID == Passport, INE, driving license, etc...
        # otherGuests == People other than the one who made the reservation.
        self.items = [
            "ID", "adults", "minors", "guestID", "dateIn", "dateOut", "rate",
            "paid", "status", "company", "extras", "group", "notes",
            "otherGuests"
        ]

        for item in self.items:
            setattr(self, item, None)

    def getData(self):
        """Return the reservation data as a dict.

        Keys:
        ID, guest, rooms, user, data, adults, minors,
        guestID, dateIn, dateOut, rate, paid, status, company,
        extras, group, notes, otherGuests
        """
        data = {}
        for item in self.items:
            data[item] = getattr(self, item)

        data["guest"] = self.guest
        data["rooms"] = self.rooms
        data["user"] = self.user
        return data

    def setData(self):
        """Parse the data passed and assign it to variables.

        Data must be a dict with this keys:
        ID, guest, rooms, user, data, adults, minors,
        guestID, dateIn, dateOut, rate, paid, status, company,
        extras, group, notes, otherGuests

        Some can be left out if empty.
        """
        for key, value in self.data.items():
            setattr(self, key, value)

    def assignRoom(self):
        """Assign a room to the reservation."""
        # if there are rooms already occupied try and assign the room to the roomGroup
        # with the most occupied rooms. Rooms are grouped because they can share AC or
        # water heaters, so grouping them makes sense economically.
        # if there are no rooms already occupied, randomly assign it.
        pass


class ReservationUi(QWidget):
    """Graphic representation of a reservation."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)
