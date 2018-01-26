from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ReservationD(QWidget):
    """Data representation of a reservation."""

    def __init__(self, guest, rooms, user, data, parent):
        """Init."""
        super().__init__(parent)

        self.ID = None
        self.guest = guest
        self.rooms = rooms  # 1 reservation can comprise multiple rooms.
        self.user = user  # The user who made the reservation.
        self.data = data
        self.adults = None
        self.minors = None
        self.guestID = None  # Passport, INE, driving license, etc...
        self.dateIn = None
        self.dateOut = None
        self.rate = None
        self.paid = None
        self.status = None
        self.company = None
        self.extras = None
        self.group = None
        self.notes = None
        self.otherGuests = None  # People other than the one who made the reservation.


class ReservationUi(QWidget):
    """Graphic representation of a reservation."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)
