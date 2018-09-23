"""Visualizer for the database."""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Db


class Visualizer(QWidget):
    """Database visualizer."""

    def __init__(self):
        """Init."""
        super().__init__()

        self.tableRooms = QTableWidget(150, 5)
        self.tableRoomstatusDefs = QTableWidget(150, 3)
        self.tableRoomTypesDefs = QTableWidget(150, 5)
        self.tableRoomExtrasDefs = QTableWidget(150, 4)
        self.tableRoomExtras = QTableWidget(150, 3)

        btnUpdate = QPushButton("Update")
        btnUpdate.clicked.connect(self.updateTables)
        btnOk = QPushButton("OK")
        btnOk.clicked.connect(self.accept)

        self.tables = {
            "Rooms": 5,
            "RoomStatusDefs": 3,
            "RoomTypesDefs": 5,
            "RoomExtrasDefs": 4,
            "RoomExtras": 3,
            "RsvStatusDefs": 3,
            "Company": 7,
            "CompanyContacts": 6,
            "CompanyPhones": 7,
            "CompanyAddresses": 10,
            "CompanyEmails": 4,
            "Guests": 7,
            "GuestIDDs": 4,
            "GuestPhones": 7,
            "reservations": 16,
            "GuestEmails": 4
            }

        layout = QGridLayout()
        self.tablesList = []
        x = 0
        y = 0
        for key, value in self.tables.items():
            setattr(self, "table" + key, QTableWidget(1000, value))
            setattr(self, key + "Layout", QVBoxLayout())
            setattr(self, key + "Label", QLabel(key))
            getattr(self, key + "Label").setAlignment(Qt.AlignCenter)
            getattr(self, key + "Layout").addWidget(getattr(self, key + "Label"))
            getattr(self, key + "Layout").addWidget(getattr(self, "table" + key))
            self.tablesList.append(getattr(self, "table" + key))
            layout.addLayout(getattr(self, key + "Layout"), x, y)
            y += 1
            if y == 4:
                y = 0
                x += 1

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(btnUpdate)
        btnLayout.addWidget(btnOk)

        layout.addLayout(btnLayout, x + 1, 0, 1, 4)
        self.setLayout(layout)
        self.updateTables()
        self.updateTables()

    def updateTables(self):
        """Update tables."""
        db = Db.dummyDb()
        tables = ["rooms", "roomStatusDefs", "roomTypesDefs", "roomExtrasDefs",
                  "roomExtras", "rsvStatusDefs", "companies", "companyContacts",
                  "companyPhones", "companyAddresses", "companyEmails", "guests",
                  "guestsIDDs", "guestPhones", "reservations", "guestEmails"]
        t = 0
        for table in tables:
            data = db.getTableItems(table)
            tableObj = self.tablesList[t]
            r = 0
            rawCol = db.getTableMeta(table)
            colNames = [x[1] for x in rawCol]
            tableObj.setHorizontalHeaderLabels(colNames)
            for row in data:
                c = 0
                for column in row:
                    prevItem = tableObj.item(r, c)
                    item = QTableWidgetItem(str(column))
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    if prevItem:
                        if prevItem.text() != str(column):
                            item.setForeground(Qt.white)
                            item.setBackground(Qt.red)
                    else:
                        item.setForeground(Qt.white)
                        item.setBackground(Qt.red)

                    tableObj.setItem(r, c, item)
                    c += 1
                r += 1
            tableObj.resizeColumnsToContents()
            tableObj.resizeRowsToContents()
            t += 1

    def accept(self):
        """Accept."""
        QWidget.close(self)


app = QApplication(sys.argv)
v = Visualizer()
v.showMaximized()
sys.exit(app.exec_())
