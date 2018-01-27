import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from DataItems import DataItem


class GuestD(DataItem):
    """Data representation of guest."""

    def __init__(self, parent=None):
        """Init."""
        super().__init__(parent)

        # self.guestID is a pyisical ID and can be a passport, driving license etc.
        # self.guestID must be formatted [idType, idNumber]
        #
        # self.phones must be formatted [number, ext, name]
        # self.phones, self.emails and self.addresses can have more than 1 item
        #
        # self.company:
        # Company's hold invoice data, so if the guest needs an invoice, even if he is a
        # "Persona Fisica", a company must be registered.
        # they would register to their name instead of a company name.

        self.items = [
            "ID", "name", "lastName", "guestID", "age", "phones", "emails",
            "addresses", "country", "state", "county", "notes"
        ]

        for item in self.items:
            setattr(self, item, None)

    def getName(self):
        """Return formatted name."""
        return self.lastName + ", " + self. name


class GuestUi(QWidget):
    """Graphic representation of a guest."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)


class CompanyD(DataItem):
    """Data representation of company."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        # businessName eg. Syrup Design Studio
        #
        # companyName eg. Duraznos en almibar SA de CV, Edgar Solis Vizcarra
        #
        # self.phones must be formatted [number, ext, name]
        # self.phones, self.emails and self.addresses can have more than 1 item
        #
        # contact == name of contact person

        self.items = [
            "ID", "businessName", "companyName", "addresses", "phones",
            "emails", "RFC", "contact", "country", "state", "county", "notes"
        ]

        for item in self.items:
            setattr(self, item, None)


class CompanyUi(QWidget):
    """Graphic representation of a company."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)


class UserD(DataItem):
    """Data representation of a user."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        # self.type [ADMIN=0, USER=1]

        self.items = ["ID", "type", "name", "lastName", "notes"]

        for item in self.items:
            setattr(self, item, None)


class UserUi(QWidget):
    """Graphic representation of a user."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)
