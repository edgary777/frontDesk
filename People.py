from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GuestD(QWidget):
    """Data representation of guest."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.ID = None
        self.name = None
        self.lastName = None
        self.guestID = None  # Passport, INE, driving license, etc...
        self.age = None
        self.phones = None  # [number, ext, name] Can have more than 1
        self.emails = None  # Can have more than 1
        self.addresses = None  # Can have more than 1
        self.country = None
        self.state = None
        self.county = None
        self.notes = None
        # Company's hold invoice data, so if the guest needs an invoice, even if he is a
        # "Persona Fisica", a company must be registered.
        # they would register to their name instead of a company name.
        self.company = None


class GuestUi(QWidget):
    """Graphic representation of a guest."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)


class CompanyD(QWidget):
    """Data representation of company."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.ID = None
        self.businessName = None  # eg. Syrup Design Studio
        self.companyName = None  # eg. Duraznos en almibar SA de CV, Edgar Solis Vizcarra
        self.addresses = None  # Can have more than 1
        self.phones = None  # [number, ext, name] Can have more than 1
        self.emails = None  # Can have more than 1
        self.RFC = None
        self.contact = None  # name of contact person
        self.country = None
        self.state = None
        self.county = None
        self.notes = None


class CompanyUi(QWidget):
    """Graphic representation of a company."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)


class UserD(QWidget):
    """Data representation of a user."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.ID = None
        self.type = None  # ADMIN=0, USER=1
        self.name = None
        self.lastName = None
        self.notes = None


class UserUi(QWidget):
    """Graphic representation of a user."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)
