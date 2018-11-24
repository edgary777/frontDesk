"""Database communication implementation."""
import sqlite3
import datetime
import random


class Db(object):
    """Database."""

    def __init__(self):
        """Init."""
        self.database = "database.db"
        self.initTables()

    def initTables(self):
        """If table not exists create it."""
        connection = sqlite3.connect(self.database)
        connection.execute("""PRAGMA foreign_keys = ON;""")
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS log(
                        logID INTEGER PRIMARY KEY AUTOINCREMENT,
                        userID INT REFERENCES users(userID),
                        username TEXT,
                        actionType TEXT,
                        log TEXT,
                        date DATE
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS companies(
                        companyID INTEGER PRIMARY KEY AUTOINCREMENT,
                        businessName TEXT,
                        companyName TEXT,
                        RFC TEXT,
                        notes TEXT,
                        registerDate DATE,
                        userID INT REFERENCES users(userID)
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS companyAddresses(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        companyID INT REFERENCES companies(companyID) ON DELETE CASCADE,
                        country TEXT,
                        region TEXT,
                        city TEXT,
                        street TEXT,
                        zone TEXT,
                        extNumber VARCHAR,
                        intNumber VARCHAR,
                        cp VARCHAR
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS companyPhones(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        companyID INT REFERENCES companies(companyID) ON DELETE CASCADE,
                        countryCode VARCHAR,
                        regionCode VARCHAR,
                        phone VARCHAR,
                        ext VARCHAR,
                        name TEXT
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS companyEmails(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        companyID INT REFERENCES companies(companyID) ON DELETE CASCADE,
                        email VARCHAR,
                        name TEXT
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS companyContacts(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        companyID INT REFERENCES companies(companyID) ON DELETE CASCADE,
                        name TEXT,
                        lastName TEXT,
                        notes TEXT
               );"""
        cursor.execute(query)

        # Guest does not store the guest identification,it is stored in the reservation.
        query = """CREATE TABLE IF NOT EXISTS guests(
                        guestID INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        lastName TEXT,
                        age INT,
                        notes TEXT,
                        registerDate DATE,
                        userID INT REFERENCES users(userID)
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS guestAddresses(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        guestID INT REFERENCES guests(guestID) ON DELETE CASCADE,
                        country TEXT,
                        region TEXT,
                        city TEXT,
                        street TEXT,
                        zone TEXT,
                        extNumber VARCHAR,
                        intNumber VARCHAR,
                        cp VARCHAR
                );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS guestPhones(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        guestID INT REFERENCES guests(guestID) ON DELETE CASCADE,
                        countryCode VARCHAR,
                        regionCode VARCHAR,
                        phone VARCHAR,
                        ext VARCHAR,
                        name TEXT
                );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS guestEmails(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        guestID INT REFERENCES guests(guestID) ON DELETE CASCADE,
                        email VARCHAR,
                        name TEXT
                );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS guestsIDDs(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        guestID INT REFERENCES guests(guestID) ON DELETE CASCADE,
                        IDType text,
                        IDNumber VARCHAR
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS users(
                        userID INTEGER PRIMARY KEY AUTOINCREMENT,
                        typeID INT REFERENCES userTypesDefs(typeID),
                        username VARCHAR,
                        name TEXT,
                        lastName TEXT,
                        notes VARCHAR,
                        password VARCHAR,
                        email VARCHAR,
                        registerDate DATE,
                        registeredBy INT
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS userTypesDefs(
                        typeID INTEGER PRIMARY KEY UNIQUE,
                        description TEXT,
                        longDescription TEXT
                );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS rsvStatusDefs(
                        statusID INTEGER PRIMARY KEY UNIQUE,
                        description TEXT,
                        longDescription TEXT
               );"""
        cursor.execute(query)

        # TO DO: Other guests must at least have an adult/minor option, maybe age.
        query = """CREATE TABLE IF NOT EXISTS rsvOtherGuests(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        rsvID INT REFERENCES reservations(rsvID) ON DELETE CASCADE,
                        name TEXT,
                        lastName TEXT,
                        notes TEXT
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS rsvExtras(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        rsvID INT REFERENCES reservations(rsvID),
                        extraID INT REFERENCES rsvExtrasDefs(extraID) ON DELETE CASCADE
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS rsvExtrasDefs(
                        extraID INTEGER PRIMARY KEY UNIQUE,
                        description TEXT,
                        longDescription TEXT,
                        icon TEXT
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS reservations(
                        rsvID INTEGER PRIMARY KEY AUTOINCREMENT,
                        guestID INT REFERENCES guests(guestID),
                        statusID INT REFERENCES rsvStatusDefs(statusID),
                        userID INT REFERENCES users(userID),
                        companyID INT REFERENCES companies(companyID),
                        adults INT,
                        minors INT,
                        dateIn DATE,
                        dateOut DATE,
                        rate FLOAT,
                        paid FLOAT,
                        rsvgroup TEXT,
                        roomNo TEXT,
                        roomType INT,
                        notes TEXT,
                        registerDate DATE
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS rsvParking(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        rsvID INT REFERENCES reservations(rsvID) ON DELETE CASCADE,
                        carModel TEXT,
                        plateNumber VARCHAR
                   );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS rsvRoomsIDs(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        rsvID INT REFERENCES reservations(rsvID),
                        room INT REFERENCES rooms(roomNo) ON DELETE CASCADE
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS roomGroups(
                        groupID INTEGER PRIMARY KEY,
                        groupName TEXT,
                        groupDescription TEXT
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS rooms(
                        roomNo TEXT PRIMARY KEY,
                        typeID INT REFERENCES roomTypesDefs(typeID),
                        statusID INT REFERENCES roomStatusDefs(statusID),
                        userId INT REFERENCES users(userID),
                        notes TEXT,
                        roomGroup TEXT REFERENCES roomGroups(groupID) ON UPDATE CASCADE
               );"""
        cursor.execute(query)

        # table that holds the data for the extras each room has.
        # row1 [1, 1], row2 [1, 2], row3 [2, 2], row4 [2, 4]
        query = """CREATE TABLE IF NOT EXISTS roomExtras(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        roomNo TEXT REFERENCES rooms(roomNo) ON DELETE CASCADE,
                        extraID INT REFERENCES roomExtrasDefs(extraID)
               );"""
        cursor.execute(query)

        # table that says what each extra is.
        # extraID should AUTOINCREMENT, but for testing it was removed.
        query = """CREATE TABLE IF NOT EXISTS roomExtrasDefs(
                        extraID INTEGER PRIMARY KEY UNIQUE,
                        description TEXT,
                        longDescription TEXT,
                        icon TEXT
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS roomTypesDefs(
                        typeID INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT,
                        beds INT,
                        maxCapacity INT,
                        longDescription TEXt
               );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS roomStatusDefs(
                        statusID INTEGER PRIMARY KEY UNIQUE,
                        description TEXT,
                        longDescription TEXT
               );"""
        cursor.execute(query)

        connection.commit()
        connection.close()

    def startConnection(self):
        """Connect to database an return a cursor object."""
        connection = sqlite3.connect(self.database)
        connection.execute("""PRAGMA foreign_keys = ON;""")
        cursor = connection.cursor()
        return [connection, cursor]

    def endConnection(self, connection):
        """Close db connection."""
        connection.commit()
        connection.close()

    def insertQuery(self, table, items, columns=None):
        """Insert escaped query.

        Return a parameterized query and the values for it.
        If you are not passing values for all the table columns
        then you must also pass which columns you are passing.
        """
        # Queries that get input from a user are dangerous.
        # Stay safe by parameterizing them.
        # for each value there must be a '?'.
        parameters = "?"
        if len(items) > 1:
            for value in range((len(items) - 1)):
                parameters += ", ?"

        # When the table has an autoincrementing column it must be excluded from the query
        # so you must select the columns you are going to insert.
        if columns:
            columns = ", ".join(columns)
            query = "INSERT INTO {} ({}) VALUES({});".format(
                table, columns, parameters)
        else:
            query = "INSERT INTO {} VALUES({});".format(table, parameters)

        values = []
        for value in items:
            values.append(value)
        return [query, values]

    def updateRsvRoomID(self, rsvID, roomNo, cursor):
        """Insert data on rsvRoomsIDs."""
        query = "UPDATE reservations SET roomNo = ? WHERE rsvId = ?;"
        cursor.execute(query, [roomNo, rsvID])

    def getTableItems(self, table, cursor):
        """Return all items from table."""
        query = """SELECT * FROM {};""".format(table)
        cursor.execute(query)
        items = cursor.fetchall()

        return items

    def getTableMeta(self, table):
        """Return table columnt titles."""
        connection = sqlite3.connect(self.database)
        connection.execute("""PRAGMA foreign_keys = ON;""")
        cursor = connection.cursor()

        query = """PRAGMA table_info({});""".format(table)
        cursor.execute(query)
        items = cursor.fetchall()

        connection.commit()
        connection.close()

        return items

    def selectiveQuery(self, table, item, column, condition):
        """Return items where the column meets the condition."""
        connection = sqlite3.connect(self.database)
        connection.execute("""PRAGMA foreign_keys = ON;""")
        cursor = connection.cursor()

        query = """SELECT {} FROM {} WHERE {}=?;""".format(item, table, column)
        cursor.execute(query, [condition])
        items = cursor.fetchall()

        connection.commit()
        connection.close()

        return items

    def selectQuery(self, table, column, cursor):
        """Return all items in column from table."""
        query = """SELECT {} FROM {};""".format(column, table)
        cursor.execute(query)
        items = [x[0] for x in cursor]

        return items

    def selectCountWhere(self, table, column, value, cursor):
        """Return the number of instances of a value in a table."""
        query = """SELECT COUNT({}) FROM {} WHERE {}=?;""".format(
            column, table, column)
        cursor.execute(query, value)
        items = cursor.fetchone()[0]

        return items

    def selectCount(self, table, column, cursor):
        """Return the number of instances of a value in a table."""
        query = """SELECT COUNT({}) FROM {};""".format(column, table, column)
        cursor.execute(query)
        items = cursor.fetchone()[0]

        return items

    def selectRoomsOfTypeInGroup(self, roomGroup, roomType, cursor):
        """Return the number of instances of a value in a table."""
        query = """SELECT COUNT(roomNo) FROM rooms WHERE roomGroup= ?;"""
        cursor.execute(query, [roomGroup])
        items = cursor.fetchone()[0]

        return items

    def selectRoom(self, roomNo, cursor):
        """Return all data of a room."""
        roomNo = [roomNo]
        query = """SELECT * FROM rooms WHERE roomNo= ?;"""
        cursor.execute(query, roomNo)
        items = cursor.fetchall()[0]

        return items

    def selectRoomType(self, roomType, cursor):
        """Return roomType data of roomType."""
        roomType = [roomType]
        query = """SELECT * FROM roomTypesDefs WHERE typeID= ?;"""
        cursor.execute(query, roomType)
        items = cursor.fetchall()[0]

        return items

    def selectRoomExtras(self, roomNo, cursor):
        """Return roomExtras of a room."""
        roomNo = [roomNo]
        query = """SELECT * FROM roomExtras WHERE roomNo= ?;"""
        cursor.execute(query, roomNo)
        items = cursor.fetchall()

        return items

    def selectReservationData(self, rsvID, table, cursor):
        """Return rsvOtherGuests of a reservation."""
        rsvID = [rsvID]
        query = """SELECT * FROM {} WHERE rsvID= ?;""".format(table)
        cursor.execute(query, rsvID)
        items = cursor.fetchall()

        return items

    def selectReservationsForDay(self, date, cursor):
        """Return rsvID of Non-Cancelled reservations occupying a room on a date."""
        date = str(date)
        date = [date, date]
        query = """SELECT `rsvID` FROM reservations WHERE dateIn<= ? AND dateOut>= ?
                   AND statusID<> 3;"""
        cursor.execute(query, date)
        return cursor.fetchall()

    def selectReservation(self, rsvID, cursor):
        """Return all data of a reservation.

        Input: Accepts a reservation ID as a value or as
                the first value of a tuple or list

        Output: Returns a tuple with all the data of a reservation.
        """
        if type(rsvID) is tuple:
            rsvID = [rsvID[0]]
        else:
            rsvID = [rsvID]
        query = """SELECT * FROM reservations WHERE rsvID= ?;"""
        cursor.execute(query, rsvID)
        items = cursor.fetchall()[0]

        return items

    def selectReservationRoom(self, rsvID, cursor):
        """Return the room occupied by a reservation.

        Input: Accepts a reservation ID as a value or as
                the first value of a tuple or list

        Output: Returns a list with a tuple inside [(roomNo, roomType)]
        """
        if type(rsvID) is tuple:
            rsvID = [rsvID[0]]
        else:
            rsvID = [rsvID]
        query = """SELECT roomNo, roomType FROM reservations WHERE rsvID= ?;"""
        cursor.execute(query, rsvID)
        items = cursor.fetchall()

        return items

    def selectReservationRoomType(self, rsvID, cursor):
        """Return the room occupied by a reservation."""
        rsvID = [rsvID[0]]
        query = """SELECT roomType FROM reservations WHERE rsvID= ?;"""
        cursor.execute(query, rsvID)
        items = cursor.fetchall()

        return items

    def selectCheckIns(self, date, cursor):
        """Return Check-Ins for date."""
        date = [str(date)]
        query = """SELECT `rsvId` FROM reservations WHERE dateIn= ?;"""
        cursor.execute(query, date)
        items = cursor.fetchall()

        return items

    def selectCheckOuts(self, date, cursor):
        """Return Check-Outs for date."""
        date = [str(date)]
        query = """SELECT `rsvId` FROM reservations WHERE dateOut= ?;"""
        cursor.execute(query, date)
        items = cursor.fetchall()

        return items

    def selectFinishedRsvs(self, cursor):
        """Return rsvId of finished reservations.

        Only of reservations whose checkins where before today and whose checkouts where
        also before today.
        """
        date = datetime.datetime.today().date()
        date = [date, date]
        query = """SELECT `rsvId` FROM reservations WHERE dateIn< ? and dateOut< ?;"""
        cursor.execute(query, date)
        items = cursor.fetchall()

        return items

    def selectActiveRsvs(self, cursor):
        """Return rsvId of active reservations.

        Only of reservations whose checkins where before today and whose checkouts are
        today or later on..
        """
        date = datetime.datetime.today().date()
        date = [date, date]
        query = """SELECT `rsvId` FROM reservations WHERE dateIn< ? and dateOut>= ?;"""
        cursor.execute(query, date)
        items = cursor.fetchall()

        return items

    def selectTable(self, table, cursor):
        """Return all items of a table."""
        query = """SELECT * FROM '{}';""".format(table)
        cursor.execute(query)
        items = cursor.fetchall()

        return items

    def selectUsers(self, cursor):
        """Return all users ID's."""
        return self.selectQuery("users", "userID", cursor)

    def selectUser(self, username, cursor):
        """Return the data of the passed user.

        Input:
        - username
        Output:
        - Returns the user data if the username matches any on the database.
        - Returns False if there's no match for the username.
        """
        username = [username]
        query = """SELECT * FROM users WHERE username= ?;"""
        cursor.execute(query, username)
        items = cursor.fetchall()

        if items != []:
            return items[0]
        else:
            return False

    def selectUserById(self, userID, cursor):
        """Return the data of the passed user ID.

        Input:
        - user ID
        Output:
        - Returns the user data if the user ID matches any on the database.
        - Returns False if there's no match for the user ID.
        """
        userID = [userID]
        query = """SELECT * FROM users WHERE userID= ?;"""
        cursor.execute(query, userID)
        items = cursor.fetchall()

        if items != []:
            return items[0]
        else:
            return False

    def selectUsernames(self, cursor):
        """Return a list of all the usernames registered."""
        query = """SELECT `username` FROM users;"""
        cursor.execute(query)
        items = cursor.fetchall()
        usernames = []
        for item in items:
            usernames.append(str(item[0]))
        return usernames

    def verifyUsers(self, cursor):
        """Return true if there are registered users, False if there aren't."""
        if self.selectUsers(cursor):
            return True
        else:
            return False

    def verifyRoot(self, cursor):
        """Verify if there are admin users.

        Returns True if there are registered users of type Root.
        Returns False if there are no registered users of type Root.
        Returns 2 if there are no users at all.
        """
        if self.verifyUsers(cursor):
            users = self.selectTable("users", cursor)
            for user in users:
                if user[1] == 0:
                    return True
            return False
        else:
            return 2

    def verifyAdmin(self, cursor):
        """Verify if there are admin users.

        Returns True if there are registered users of type Admin.
        Returns False if there are no registered users of type Admin.
        Returns 2 if there are no users at all.
        """
        if self.verifyUsers(cursor):
            users = self.selectTable("users", cursor)
            for user in users:
                if user[1] == 1:
                    return True
            return False
        else:
            return 2

    def verifyUser(self, username, cursor):
        """Verify the username passed is in the database.

        Input:
            - Username as string.
        Output:
            - Returns True if user is in the database.
            - Returns False if user is not in the database.
        """
        usernames = self.selectUsernames(cursor)
        print("usernames ", usernames)
        for x in usernames:
            print(x, " ", username)
            if x == username:
                return True
        return False

    def logEntry(self, userID, actionType, logData, cursor, username=None):
        """Entry log of a user action."""
        print("UserAction: ", actionType)
        if userID is None and username is not None:
            userID = self.getUser(username, cursor)[0]
        username = self.getUserById(userID, cursor)[2]
        if actionType == 0:
            action = "Registro de usuario"
            if logData[1] == 0:
                priv = "Root."
            elif logData[1] == 1:
                priv = "Admin."
            else:
                priv = "Regular."
            log = "Se registro al usuario {} con privilegios de usuario {}.".format(logData[0], priv)
        if actionType == 1:
            action = "Inicio de sesión"
            log = "El usuario {} inicio sesión.".format(username)
        if actionType == 2:
            action = "Cierre de sesión"
            log = "El usuario {} cerro sesión.".format(username)

        date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")
        data = [userID, username, action, log, date]

        columns = ["userID", "username", "actionType", "log", "date"]
        query = self.insertQuery("log", data, columns)
        cursor.execute(query[0], query[1])

    def getUser(self, username, cursor):
        """Verify if passed credentials are correct.

        Input:
        - Username.
        Output:
        - Returns the user data if the username matches any user on the db.
        - Returns False if there's no match in the database.
        """
        data = self.selectUser(username, cursor)
        if data is not False:
            return data
        else:
            return False

    def getUserById(self, userID, cursor):
        """Verify if passed credentials are correct.

        Input:
        - User ID.
        Output:
        - Returns the user data if the user ID matches any user on the db.
        - Returns False if there's no match in the database.
        """
        data = self.selectUserById(userID, cursor)
        if data is not False:
            return data
        else:
            return False

    def getRooms(self, cursor):
        """Return all rooms."""
        return self.selectQuery("rooms", "roomNo", cursor)

    def getRoomsByType(self, roomType, cursor):
        """Return the count of rooms of the roomType passed."""
        return self.selectCountWhere("rooms", "typeID", str(roomType), cursor)

    def getRoom(self, roomNo, cursor):
        """Return room data for roomNo."""
        return self.selectRoom(roomNo, cursor)

    def getRoomType(self, roomType, cursor):
        """Return roomType data of roomType."""
        return self.selectRoomType(roomType, cursor)

    def getRoomExtras(self, roomNo, cursor):
        """Return roomExtras of a room."""
        return self.selectRoomExtras(roomNo, cursor)

    def getReservation(self, rsvID, cursor):
        """Return reservation data for rsvID."""
        return self.selectReservation(rsvID, cursor)

    def getReservationExtras(self, rsvID, cursor):
        """Return rsvExtras of a reservation."""
        return self.selectReservationData(rsvID, "rsvExtras", cursor)

    def getReservationOGuests(self, rsvID, cursor):
        """Return rsvOtherGuests of a reservation."""
        return self.selectReservationData(rsvID, "rsvOtherGuests", cursor)

    def getReservationParking(self, rsvID, cursor):
        """Return rsvOtherGuests of a reservation."""
        return self.selectReservationData(rsvID, "rsvParking", cursor)

    def getReservationRoomsIDs(self, rsvID, cursor):
        """Return rsvOtherGuests of a reservation."""
        return self.selectReservationData(rsvID, "rsvRoomsIDs", cursor)

    def getReservationsForDay(self, date, cursor):
        """Return Non-Cancelled reservations occupying a room for the passed day."""
        return self.selectReservationsForDay(date, cursor)

    def getReservationRoom(self, rsvID, cursor):
        """Return the rooms occupied by a reservation."""
        return self.selectReservationRoom(rsvID, cursor)

    def getReservationRoomType(self, rsvID, cursor):
        """Return the rooms occupied by a reservation."""
        return self.selectReservationRoomType(rsvID, cursor)

    def getFreeRoomsForDate(self, date, cursor):
        """Return a list of available room slots by type.

        return {type: rooms, ...}
        """
        rsvs = self.getReservationsForDay(date, cursor)
        rooms = {}
        # roomTypes are user defined and therefore vary, this makes the function dynamic.
        roomTypes = self.selectCount("roomTypesDefs", "typeID", cursor) + 1
        for roomType in range(1, roomTypes):
            rooms[roomType] = self.getRoomsByType(roomType, cursor)
        for rsv in rsvs:
            for room in self.getReservationRoom(rsv[0], cursor):
                rooms[room[2]] -= room[3]
        return rooms

    def getGuests(self, cursor):
        """Return all guests data."""
        return self.getTableItems("guests", cursor)

    def getGuest(self, guestID, cursor):
        """Return guest data."""
        return self.selectiveQuery("guests", "*", "guestID", guestID)[0]

    def getCompanies(self, cursor):
        """Return all companies."""
        return self.getTableItems("companies", cursor)

    def getReservations(self, cursor):
        """Return all reservations."""
        return self.getTableItems("reservations", cursor)

    def getTodayCheckIns(self, cursor):
        """Return ID's of all reservations supposed to Check-In today."""
        today = datetime.datetime.today().date()
        return self.selectCheckIns(today, cursor)

    def getTodayCheckOuts(self, cursor):
        """Return ID's of all reservations supposed to Check-In today."""
        today = datetime.datetime.today().date()
        return self.selectCheckOuts(today, cursor)

    def getRoomsOfTypeInGroup(self, roomGroup, roomType, cursor):
        """Return number of available rooms of roomType in roomGroup."""
        return self.selectRoomsOfTypeInGroup(roomGroup, roomType, cursor)

    def getRoomsInGroup(self, roomGroup, cursor):
        """Return number of rooms in roomGroup."""
        return self.selectCountWhere("roomGroups", "groupID", roomGroup)

    def getRoomsGroupCount(self, cursor):
        """Return count of the number of existing roomGroup."""
        return self.selectCount("roomGroups", "groupID", cursor) + 1

    def getRoomsInRoomGroups(self, cursor):
        """Return dict of the number rooms each roomGroup has."""
        roomGroups = {}
        roomGroupsCount = self.getRoomsGroupCount(cursor)
        for roomGroup in range(1, roomGroupsCount):
            roomGroups[roomGroup] = self.selectCountWhere(
                "rooms", "roomGroup", [str(roomGroup)], cursor)
        return roomGroups

    def getRoomGroupsForDate(self, date, cursor):
        """Return a dict of group occupancy on a given date."""
        rsvs = self.getReservationsForDay(date, cursor)
        roomGroups = self.getRoomsInRoomGroups(cursor)
        for rsv in rsvs:
            for room in self.getReservationRoom(rsv[0], cursor):
                roomGroups[room[1]] -= 0 if room[0] is None else 1
        return roomGroups

    def getRoomGroupOccupancyForPeriod(self, dateIn, dateOut, cursor):
        """Return the percentage of occupancy of roomGroups during a period of time."""
        days = (dateOut - dateIn).days
        groups = self.getRoomsInRoomGroups(cursor)
        roomGroupsCount = self.getRoomsGroupCount(cursor)

        # this is to avoid getting a key error when initially filling the dict.
        groupsAfter = {x: None for x in range(1, roomGroupsCount)}

        # To get the group with the most occupied rooms in a range of days we need to
        # check day by day how many rooms where occupied on each group. We only need the
        # highest value of each group.
        for i in range(0, days):
            date = dateIn + datetime.timedelta(days=i)
            x = self.getRoomGroupsForDate(date, cursor)
            for roomGroup in range(1, roomGroupsCount):
                if groupsAfter[roomGroup] is None or x[roomGroup] < groupsAfter[roomGroup]:
                    groupsAfter[roomGroup] = x[roomGroup]
        groupsPercentage = {}
        for roomGroup in range(1, roomGroupsCount):
            groupsPercentage[roomGroup] = abs(
                (groupsAfter[roomGroup] / groups[roomGroup]) - 1)

        return groupsPercentage

    def getRoomsForPeriodAndType(self, dateIn, dateOut, roomType, cursor):
        """Return list of rooms of roomType for a period of time."""
        days = (dateOut - dateIn).days
        rooms = None
        for i in range(0, days):
            delta = datetime.timedelta(days=i)
            x = self.getFreeRoomsForDate(dateIn + delta, cursor)[roomType]
            if rooms is None or x < rooms:
                rooms = x
        return rooms

    def selectRoomOfTypeInGroup(self, roomType, roomGroup, cursor):
        """If available return a roomNo of a room in roomGroup of roomType."""
        query = """SELECT `roomNo` FROM rooms WHERE roomGroup = ? AND typeID = ? AND
            statusID != 2 OR (roomGroup = ? AND typeID = ? AND statusID != 3);"""
        cursor.execute(query, [roomGroup, roomType[0], roomGroup, roomType[0]])
        item = cursor.fetchall()
        return item

    def getRoomOfTypeInGroup(self, roomType, roomGroup, cursor):
        """If available return a roomNo of a room in roomGroup of roomType.

        If not available return None.
        """
        room = self.selectRoomOfTypeInGroup(roomType, roomGroup, cursor)
        if len(room) > 0:
            return room[0][0]
        else:
            return None

    def updateRoomStatus(self, roomNo, newStatus, cursor):
        """Update the statusID of roomNo to newStatus on the database."""
        query = "UPDATE rooms SET statusID = ? WHERE roomNo = ?;"
        cursor.execute(query, [newStatus, roomNo])

    def getBestRoom(self, dateIn, dateOut, roomType, cursor):
        """Return roomNo of the best room choice."""
        groups = self.getRoomGroupOccupancyForPeriod(dateIn, dateOut, cursor)

        # make a list of roomGroups ordered from most occupied to least.
        orderedGroups = []
        for i in range(len(groups)):
            x = None
            y = None
            for group, value in groups.items():
                if x is None or value > x:
                    x = value
                    y = group
            groups.pop(y)
            orderedGroups.append(y)

        # Try and get a free room of roomType in the most occupied roomGroup.
        for group in orderedGroups:
            room = self.getRoomOfTypeInGroup(roomType, group, cursor)
            if room is not None:
                break
        if room is None:
            # How come there are no rooms!???
            print("WTF!")
            raise AttributeError
        else:
            # If all went well you  need to change the room status to the correct one.
            self.updateRoomStatus(room, 2, cursor)
            return room
        print("Why are you here!??")
        raise AttributeError

    def getRoomGroupsForDateAndType(self, date, roomType, cursor):
        """Return dict of groups occupancy of roomType on a given date."""
        # I actually think this method is useless.
        rsvs = self.getReservationsForDay(date, cursor)
        roomsGroups = {}
        # roomGroups are user defined and therefore vary, this makes the function dynamic.
        roomGroupsCount = self.getRoomsGroupCount(cursor)
        for roomGroup in range(1, roomGroupsCount):
            # We get the count of rooms of the passed type in each group
            roomsGroups[roomGroup] = self.getRoomsOfTypeInGroup(
                roomGroup, roomType, cursor)
        for rsv in rsvs:
            # now we must check the reservations that are using a room on that day
            # and decrease the amount of available rooms by the ones they are occupying.
            for room in self.getReservationRooms(rsv[0], cursor):
                # rsvRoom[ID, rsvID, roomType, roomsAmount]
                roomsGroups[room[2]] -= room[3]
        return roomsGroups

    # def insertQuery(self, table, items, columns=None):
    #     """Insert escaped query.
    #
    #     Return a parameterized query and the values for it.
    #     If you are not passing values for all the table columns
    #         then you must also pass which columns you are passing.
    #     """
    #     # Queries that get input from a user are dangerous.
    #     # Stay safe by parameterizing them.
    #     # for each value there must be a '?'.
    #     parameters = "?"
    #     if len(items) > 1:
    #         for value in range((len(items) - 1)):
    #             parameters += ", ?"
    #
    #     if columns:
    #         columns = ", ".join(columns)
    #         query = "INSERT INTO {} ({}) VALUES({});".format(
    #             table, columns, parameters)
    #     else:
    #         query = "INSERT INTO {} VALUES({});".format(table, parameters)
    #
    #     values = []
    #     for value in items:
    #         values.append(value)
    #     return [query, values]

    def newUserTypeDef(self, cursor, data):
        """Insert user data in database."""
        query = self.insertQuery("userTypesDefs", data)
        cursor.execute(query[0], query[1])

    def newUser(self, cursor, data, columns=None):
        """Insert user data in database."""
        query = self.insertQuery("users", data, columns)
        cursor.execute(query[0], query[1])

    def newRoomStatusDef(self, cursor, data):
        """Insert room status definition in database."""
        query = self.insertQuery("roomStatusDefs", data)
        cursor.execute(query[0], query[1])

    def newRoomTypeDef(self, cursor, data):
        """Insert room type definition in database."""
        query = self.insertQuery("roomTypesDefs", data)
        cursor.execute(query[0], query[1])

    def newRoomExtraDef(self, cursor, data):
        """Insert room extra definition in database."""
        query = self.insertQuery("roomExtrasDefs", data)
        cursor.execute(query[0], query[1])

    def newRoom(self, cursor, data):
        """Insert room data in database."""
        query = self.insertQuery("rooms", data)
        cursor.execute(query[0], query[1])

    def newRoomGroup(self, cursor, data):
        """Insert room group data in database."""
        query = self.insertQuery("roomGroups", data)
        cursor.execute(query[0], query[1])

    def newRoomExtra(self, cursor, data):
        """Insert room extras in database."""
        columns = ["roomNo", "extraID"]
        query = self.insertQuery("roomExtras", data, columns)
        cursor.execute(query[0], query[1])

    def newRsvExtraDef(self, cursor, data):
        """Insert reservation extra definition in database."""
        query = self.insertQuery("rsvExtrasDefs", data)
        cursor.execute(query[0], query[1])

    def newRsvStatusDef(self, cursor, data):
        """Insert reservation extra definition in database."""
        query = self.insertQuery("rsvStatusDefs", data)
        cursor.execute(query[0], query[1])

    def newGuest(self, cursor, data):
        """Insert guest data in database."""
        columns = [
            "name", "lastName", "age", "notes", "registerDate", "userID"
            ]
        query = self.insertQuery("guests", data, columns)
        cursor.execute(query[0], query[1])
        # We need the ID to add to it's extras.
        lastID = cursor.lastrowid
        return lastID

    def newGuestAddress(self, cursor, data):
        """Insert guest address data in database."""
        columns = [
            "guestID", "country", "region", "city", "street", "zone",
            "extNumber", "intNumber", "cp"
            ]
        query = self.insertQuery("guestAddresses", data, columns)
        cursor.execute(query[0], query[1])

    def newGuestPhone(self, cursor, data):
        """Insert guest phone data in database."""
        columns = [
            "guestID", "countryCode", "regionCode", "phone", "ext", "name"
            ]
        query = self.insertQuery("guestPhones", data, columns)
        cursor.execute(query[0], query[1])

    def newGuestEmail(self, cursor, data):
        """Insert guest email data in database."""
        columns = ["guestID", "email", "name"]
        query = self.insertQuery("guestEmails", data, columns)
        cursor.execute(query[0], query[1])

    def newGuestIDD(self, cursor, data):
        """Insert guest identification data in database."""
        columns = ["guestID", "IDType", "IDNumber"]
        query = self.insertQuery("guestsIDDs", data, columns)
        cursor.execute(query[0], query[1])

    def newCompany(self, cursor, data):
        """Insert company data in database."""
        columns = [
            "businessName", "companyName", "RFC", "notes", "registerDate",
            "userID"
            ]
        query = self.insertQuery("companies", data, columns)
        cursor.execute(query[0], query[1])
        # We need the ID to add to it's extras.
        lastID = cursor.lastrowid

        return lastID

    def newCompanyAddress(self, cursor, data):
        """Insert company address data in database."""
        columns = [
            "companyID", "country", "region", "city", "street", "zone",
            "extNumber", "intNumber", "cp"
            ]
        query = self.insertQuery("companyAddresses", data, columns)
        cursor.execute(query[0], query[1])

    def newCompanyPhone(self, cursor, data):
        """Insert company phone data in database."""
        columns = [
            "companyID", "countryCode", "regionCode", "phone", "ext", "name"
            ]
        query = self.insertQuery("companyPhones", data, columns)
        cursor.execute(query[0], query[1])

    def newCompanyEmail(self, cursor, data):
        """Insert company email data in database."""
        columns = ["companyID", "email", "name"]
        query = self.insertQuery("companyEmails", data, columns)
        cursor.execute(query[0], query[1])

    def newCompanyContact(self, cursor, data):
        """Insert company contact data in database."""
        columns = ["companyID", "name", "lastName", "notes"]
        query = self.insertQuery("companyContacts", data, columns)
        cursor.execute(query[0], query[1])

    def newReservation(self, cursor, data):
        """Insert reservation data in database."""
        columns = [
            "guestID", "statusID", "userID", "companyID", "adults", "minors",
            "dateIn", "dateOut", "rate", "paid", "rsvgroup", "roomNo", "roomType",
            "notes", "registerDate"
            ]
        query = self.insertQuery("reservations", data, columns)
        cursor.execute(query[0], query[1])
        lastID = cursor.lastrowid

        return lastID

    def newRsvOGuest(self, cursor, data):
        """Insert reservation other guest data in database."""
        columns = ["rsvID", "name", "lastName", "notes"]

        query = self.insertQuery("rsvOtherGuests", data, columns)
        cursor.execute(query[0], query[1])

    def newRsvExtra(self, cursor, data):
        """Insert reservation extra data in database."""
        columns = ["rsvID", "extraID"]
        query = self.insertQuery("rsvExtras", data, columns)
        cursor.execute(query[0], query[1])

    def newRsvRoom(self, cursor, data):
        """Insert reservation rooms data in database."""
        columns = ["roomType"]
        query = self.insertQuery("reservations", data, columns)
        cursor.execute(query[0], query[1])

    def newRsvParking(self, cursor, data):
        """Insert reservation parking data in database."""
        columns = ["rsvID", "carModel", "plateNumber"]
        query = self.insertQuery("rsvParking", data, columns)
        cursor.execute(query[0], query[1])

    def newRsvRoomId(self, cursor, data):
        """Insert reservation room ID data in database."""
        columns = ["rsvID", "room"]
        query = self.insertQuery("rsvRoomsIDs", data, columns)
        cursor.execute(query[0], query[1])


class dummyDb(object):
    """Db."""

    def __init__(self):
        """Init."""
        # self.dummyDB()
        self.database = "database.db"

    def startConnection(self):
        """Connect to database an return a cursor object."""
        connection = sqlite3.connect(self.database)
        connection.execute("""PRAGMA foreign_keys = ON;""")
        cursor = connection.cursor()
        return [connection, cursor]

    def endConnection(self, connection):
        """Close db connection."""
        connection.commit()
        connection.close()

    def insertQuery(self, table, items, columns=None):
        """Insert escaped query.

        Return a parameterized query and the values for it.
        If you are not passing values for all the table columns
            then you must also pass which columns you are passing.
        """
        # Queries that get input from a user are dangerous.
        # Stay safe by parameterizing them.
        # for each value there must be a '?'.
        parameters = "?"
        if len(items) > 1:
            for value in range((len(items) - 1)):
                parameters += ", ?"

        if columns:
            columns = ", ".join(columns)
            query = "INSERT INTO {} ({}) VALUES({});".format(
                table, columns, parameters)
        else:
            query = "INSERT INTO {} VALUES({});".format(table, parameters)

        values = []
        for value in items:
            values.append(value)
        return [query, values]

    def newUserTypeDef(self, cursor, data):
        """Insert user data in database."""
        query = self.insertQuery("userTypesDefs", data)
        cursor.execute(query[0], query[1])

    def newUser(self, cursor, data, columns=None):
        """Insert user data in database."""
        query = self.insertQuery("users", data, columns)
        cursor.execute(query[0], query[1])

    def newRoomStatusDef(self, cursor, data):
        """Insert room status definition in database."""
        query = self.insertQuery("roomStatusDefs", data)
        cursor.execute(query[0], query[1])

    def newRoomTypeDef(self, cursor, data):
        """Insert room type definition in database."""
        query = self.insertQuery("roomTypesDefs", data)
        cursor.execute(query[0], query[1])

    def newRoomExtraDef(self, cursor, data):
        """Insert room extra definition in database."""
        query = self.insertQuery("roomExtrasDefs", data)
        cursor.execute(query[0], query[1])

    def newRoom(self, cursor, data):
        """Insert room data in database."""
        query = self.insertQuery("rooms", data)
        cursor.execute(query[0], query[1])

    def newRoomGroup(self, cursor, data):
        """Insert room group data in database."""
        query = self.insertQuery("roomGroups", data)
        cursor.execute(query[0], query[1])

    def newRoomExtra(self, cursor, data):
        """Insert room extras in database."""
        columns = ["roomNo", "extraID"]
        query = self.insertQuery("roomExtras", data, columns)
        cursor.execute(query[0], query[1])

    def newRsvExtraDef(self, cursor, data):
        """Insert reservation extra definition in database."""
        query = self.insertQuery("rsvExtrasDefs", data)
        cursor.execute(query[0], query[1])

    def newRsvStatusDef(self, cursor, data):
        """Insert reservation extra definition in database."""
        query = self.insertQuery("rsvStatusDefs", data)
        cursor.execute(query[0], query[1])

    def newGuest(self, cursor, data):
        """Insert guest data in database."""
        columns = [
            "name", "lastName", "age", "notes", "registerDate", "userID"
            ]
        query = self.insertQuery("guests", data, columns)
        cursor.execute(query[0], query[1])
        # We need the ID to add to it's extras.
        lastID = cursor.lastrowid
        return lastID

    def newGuestAddress(self, cursor, data):
        """Insert guest address data in database."""
        columns = [
            "guestID", "country", "region", "city", "street", "zone",
            "extNumber", "intNumber", "cp"
            ]
        query = self.insertQuery("guestAddresses", data, columns)
        cursor.execute(query[0], query[1])

    def newGuestPhone(self, cursor, data):
        """Insert guest phone data in database."""
        columns = [
            "guestID", "countryCode", "regionCode", "phone", "ext", "name"
            ]
        query = self.insertQuery("guestPhones", data, columns)
        cursor.execute(query[0], query[1])

    def newGuestEmail(self, cursor, data):
        """Insert guest email data in database."""
        columns = ["guestID", "email", "name"]
        query = self.insertQuery("guestEmails", data, columns)
        cursor.execute(query[0], query[1])

    def newGuestIDD(self, cursor, data):
        """Insert guest identification data in database."""
        columns = ["guestID", "IDType", "IDNumber"]
        query = self.insertQuery("guestsIDDs", data, columns)
        cursor.execute(query[0], query[1])

    def newCompany(self, cursor, data):
        """Insert company data in database."""
        columns = [
            "businessName", "companyName", "RFC", "notes", "registerDate",
            "userID"
            ]
        query = self.insertQuery("companies", data, columns)
        cursor.execute(query[0], query[1])
        # We need the ID to add to it's extras.
        lastID = cursor.lastrowid

        return lastID

    def newCompanyAddress(self, cursor, data):
        """Insert company address data in database."""
        columns = [
            "companyID", "country", "region", "city", "street", "zone",
            "extNumber", "intNumber", "cp"
            ]
        query = self.insertQuery("companyAddresses", data, columns)
        cursor.execute(query[0], query[1])

    def newCompanyPhone(self, cursor, data):
        """Insert company phone data in database."""
        columns = [
            "companyID", "countryCode", "regionCode", "phone", "ext", "name"
            ]
        query = self.insertQuery("companyPhones", data, columns)
        cursor.execute(query[0], query[1])

    def newCompanyEmail(self, cursor, data):
        """Insert company email data in database."""
        columns = ["companyID", "email", "name"]
        query = self.insertQuery("companyEmails", data, columns)
        cursor.execute(query[0], query[1])

    def newCompanyContact(self, cursor, data):
        """Insert company contact data in database."""
        columns = ["companyID", "name", "lastName", "notes"]
        query = self.insertQuery("companyContacts", data, columns)
        cursor.execute(query[0], query[1])

    def newReservation(self, cursor, data):
        """Insert reservation data in database."""
        columns = [
            "guestID", "statusID", "userID", "companyID", "adults", "minors",
            "dateIn", "dateOut", "rate", "paid", "rsvgroup", "roomNo", "roomType",
            "notes", "registerDate"
            ]
        query = self.insertQuery("reservations", data, columns)
        cursor.execute(query[0], query[1])
        lastID = cursor.lastrowid

        return lastID

    def newRsvOGuest(self, cursor, data):
        """Insert reservation other guest data in database."""
        columns = ["rsvID", "name", "lastName", "notes"]

        query = self.insertQuery("rsvOtherGuests", data, columns)
        cursor.execute(query[0], query[1])

    def newRsvExtra(self, cursor, data):
        """Insert reservation extra data in database."""
        columns = ["rsvID", "extraID"]
        query = self.insertQuery("rsvExtras", data, columns)
        cursor.execute(query[0], query[1])

    def newRsvRoom(self, cursor, data):
        """Insert reservation rooms data in database."""
        columns = ["roomType"]
        query = self.insertQuery("reservations", data, columns)
        cursor.execute(query[0], query[1])

    def newRsvParking(self, cursor, data):
        """Insert reservation parking data in database."""
        columns = ["rsvID", "carModel", "plateNumber"]
        query = self.insertQuery("rsvParking", data, columns)
        cursor.execute(query[0], query[1])

    def newRsvRoomId(self, cursor, data):
        """Insert reservation room ID data in database."""
        columns = ["rsvID", "room"]
        query = self.insertQuery("rsvRoomsIDs", data, columns)
        cursor.execute(query[0], query[1])

    def getTableItems(self, table):
        """Return all items from table."""
        connection = sqlite3.connect(self.database)
        connection.execute("""PRAGMA foreign_keys = ON;""")
        cursor = connection.cursor()

        query = """SELECT * FROM {};""".format(table)
        cursor.execute(query)
        items = cursor.fetchall()

        connection.commit()
        connection.close()

        return items

    def getTableMeta(self, table):
        """Return table columnt titles."""
        connection = sqlite3.connect(self.database)
        connection.execute("""PRAGMA foreign_keys = ON;""")
        cursor = connection.cursor()

        query = """PRAGMA table_info({});""".format(table)
        cursor.execute(query)
        items = cursor.fetchall()

        connection.commit()
        connection.close()

        return items

    def dummyDB(self):
        """Fill the database with dummy data."""
        generator = dummyGenerator()
        startConnection = self.startConnection()
        cursor = startConnection[1]
        connection = startConnection[0]

        # We need a root user to start the program.
        # First we create an admin user type.
        self.newUserTypeDef(cursor, [0, "root", "root"])
        # then we create the root user
        today = datetime.datetime.today().date()
        self.newUser(cursor, [0, 0, "root", "root", "raspberry", today, 0], [
            "userID", "typeID", "username", "name", "password", "registerDate",
            "registeredBy"
            ])
        # Now we populate the database with more dummy data
        roomStatusDefs = [[0, "LIBRE", "EL CUARTO ESTA LIBRE"], [
            1, "EN LIMPIEZA", "EL CUARTO ESTA LIBRE Y SE ESTA LIMPIANDO"
            ], [2, "OCUPADO", "EL CUARTO ESTA OCUPADO"], [
            3, "FUERA DE SERVICIO",
            "EL CUARTO ESTA FUERA DE SERVICIO Y NO SE PUEDE OCUPAR"
            ]]
        for status in roomStatusDefs:
            self.newRoomStatusDef(cursor, status)

        roomTypes = [(1, "SENCILLO", 1, 1, ""), (2, "DOBLE", 1, 2, ""),
                     (3, "TRIPLE", 2, 3, ""), (4, "QUEEN", 1, 2, ""),
                     (5, "KING", 1, 2, ""), (6, "DOBLE DOBLE", 2, 4, "")]
        for Type in roomTypes:
            self.newRoomTypeDef(cursor, Type)

        # extras = ["SERVIBAR", "AC", "TV", "CAJA FUERTE", "FUMAR"]
        roomExtras = [(0, "SERVIBAR", "", ""), (1, "AC", "", ""),
                      (2, "TV", "", ""), (3, "CAJA FUERTE", "",
                                          ""), (4, "FUMAR", "", "")]
        for extra in roomExtras:
            self.newRoomExtraDef(cursor, extra)

        for i in range(1, 11):
            self.newRoomGroup(cursor, (str(i), "g" + str(i), "h"))

        # We create rooms from randomly generated data
        for i in range(200):
            data = generator.dummyRoomData()
            self.newRoom(cursor, data[0])
            # we create the randomly generated extras of each room
            for rextra in data[1]:
                self.newRoomExtra(cursor, [data[0][0], rextra])

        # Now we will add reservations to the db, but the reservations need
        # some data before they can be created, so we must make that first.
        #
        # First, we create the reservation status definitions.
        rsvStatusDefs = [(0, "New", ""), (1, "Processed/Confirmed", ""),
                         (2, "Checked IN", ""), (3, "Checked Out",
                                                 ""), (4, "Cancelled", ""),
                         (5, "No Show", ""), (6, "Guaranteed",
                                              ""), (7, "Early Checkout", "")]
        for status in rsvStatusDefs:
            self.newRsvStatusDef(cursor, status)

        rsvExtrasDefs = [(0, "SERVIBAR", "", ""), (1, "AC", "", ""),
                         (2, "TV", "", ""), (3, "CAJA FUERTE", "",
                                             ""), (4, "FUMAR", "", "")]

        for extra in rsvExtrasDefs:
            self.newRsvExtraDef(cursor, extra)

        # now we will create the reservations
        for i in range(1000):
            # first we set a registry date.
            today = datetime.datetime.today()
            day = today - datetime.timedelta(days=30)
            date = generator.randomDate(day)
            # then we randomly create or not a company.
            companyID = None
            if random.random() > 0.9:
                companyData = generator.dummyCompanyData()
                companyData[0].append(date)  # we add the date of register.
                companyData[0].append(0)  # we add the user that registered.
                # we add the guest to the db and we get the guestID
                companyID = self.newCompany(cursor, companyData[0])

                # we now create the company data that doesn't fit in the company table.
                #
                # First the company contact
                # We set the contact companyID to the current companyID
                companyData[1][0] = companyID
                self.newCompanyContact(cursor, companyData[1])

                # Then the company phones.
                # We set the companyID to the current companyID
                for phone in companyData[2]:
                    phone[0] = companyID
                    self.newCompanyPhone(cursor, phone)

                # Then the company addresses.
                # We set the companyID to the current companyID
                for address in companyData[3]:
                    address[0] = companyID
                    self.newCompanyAddress(cursor, address)

                # finally, the company emails.
                # We set the companyID to the current companyID
                for email in companyData[4]:
                    email[0] = companyID
                    self.newCompanyEmail(cursor, email)
                """contact, phones, addresses, emails"""

            # # then we create a guest for the reservation.
            guestData = generator.dummyGuestData()
            guestData[0].append(date)  # we add the date of register.
            guestData[0].append(0)  # we add the user that registered.
            # we add the guest to the db and we get the guestID
            guestID = self.newGuest(cursor, guestData[0])

            # we now create the guest data that doesn't fit in the guests table.
            #
            # First the guest identification.
            # We set the guest guestID to the current guestID
            guestData[1][0] = guestID
            self.newGuestIDD(cursor, guestData[1])

            # Then the cuest phones.
            # We set the companyID to the current companyID
            for phone in guestData[2]:
                phone[0] = guestID
                self.newGuestPhone(cursor, phone)

            # Then the guest addresses.
            # We set the guestID to the current guestID
            for address in guestData[3]:
                address[0] = guestID
                self.newGuestAddress(cursor, address)

            # finally, the guest emails.
            # We set the guestID to the current guestID
            for email in guestData[4]:
                email[0] = guestID
                self.newGuestEmail(cursor, email)

            # Now we create the reservation.
            reservationData = generator.dummyRsvData(date)

            # We are going to create multiple reservations for group reservations, so for
            # them to have the randomly generated room data we create them individually
            # and assign them a room type from the list, rsvRoomNo is the iterator for
            # that list.
            rsvRoomNo = 0
            for room in range(len(reservationData[1])):
                reservationData[0][0] = guestID
                reservationData[0][1] = 0
                reservationData[0][2] = 0
                if companyID:
                    reservationData[0][3] = companyID
                reservationData[0].append(date)
                reservationData[0][12] = reservationData[2][rsvRoomNo]
                rsvID = self.newReservation(cursor, reservationData[0])

                if reservationData[3]:
                    for otherGuest in reservationData[3]:
                        otherGuest[0] = rsvID
                        self.newRsvOGuest(cursor, otherGuest)

                if reservationData[4]:
                    for extra in reservationData[4]:
                        extras = (rsvID, extra)
                        self.newRsvExtra(cursor, extras)

                if reservationData[5]:
                    for parking in reservationData[5]:
                        parking[0] = rsvID
                        self.newRsvParking(cursor, parking)
                rsvRoomNo += 1

        self.endConnection(connection)


class dummyGenerator(object):
    """Dummy data generator."""

    def __init__(self):
        """Init."""
        pass

    def dummyName(self):
        """Return random name."""
        return self.dummyLastName() + ", " + self.dummyFirstName()

    def dummyFirstName(self):
        """Return random first name."""
        names = [
            "Antonio", "Ana", "Brenda", "Carlos", "Cecilia", "Daniela",
            "David", "Diana", "Edgar", "Esteban", "Enya", "Fabiola",
            "Gabriela", "Ines", "Juan", "Jose", "Jesus", "Jimena", "Jorge",
            "Maria", "Maricela", "Mario", "Miguel", "Antonieta", "Luis",
            "Luisa", "Regina", "Renata", "Alejandro", "Alejandra", "Francisco",
            "Salvador", "Ignacio", "Walter", "Arturo", "Hector", "Cristina"
            ]
        if random.random() > 0.8:
            return random.sample(names, 1)[0] + " " + random.sample(names,
                                                                    1)[0]
        else:
            return random.sample(names, 1)[0]

    def dummyLastName(self):
        """Return random last names."""
        lastNames = [
            "Aguilera", "Aguilar", "Casas", "Cossio", "Escobedo", "Antunez",
            "Solis", "Saravia", "Garcia", "Martinez", "Vizcarra", "Silerio",
            "Treviño", "Mesa", "Fernandez", "Ramos", "Russek", "Vargas",
            "Alvarado", "Saltijeral", "Rodriguez", "Barrera", "Hernandez",
            "Felix", "Diaz", "Belausteguigoitia", "Giacoman"
            ]

        return random.sample(lastNames, 1)[0] + " " + random.sample(
            lastNames, 1)[0]

    def dummyGroup(self):
        """Return random group."""
        lastName = [
            "Aguilera", "Aguilar", "Casas", "Cossio", "Escobedo", "Antunez",
            "Solis", "Saravia", "Garcia", "Martinez", "Vizcarra", "Silerio",
            "Treviño", "Mesa", "Fernandez", "Ramos", "Russek", "Vargas",
            "Alvarado", "Saltijeral", "Rodriguez", "Barrera", "Hernandez",
            "Felix", "Diaz", "Belausteguigoitia", "Giacoman"
            ]
        activity = [
            "Boda", "Reunion", "Familia", "Fiesta", "Tertulia",
            "Primera Comunión", "Club"
            ]

        words = [
            "Splatoon", "INC", "Coral", "Fox", "Canal", "Banda", "PC", "Coca",
            "THC", "Gema", "Plateros", "BirdWatchers", "Ciclistas", "Motos",
            "Panamericana"
            ]

        if random.random() > 0.7:
            return random.sample(words, 1)[0]
        else:
            return random.sample(activity, 1)[0] + " " + random.sample(
                lastName, 1)[0]

    def dummyDates(self, start):
        """Return random checkIn and checkOut dates.

        the 1st is randomly generated and the 2nd is offset by a random number
        of days from the 1st one.
        """
        date1 = self.randomDate(start)

        random_days = random.randint(1, 10)
        date2 = date1 + datetime.timedelta(days=random_days)

        return (date1, date2)

    def randomDate(self, start):
        """Return a random date."""
        # start = datetime.datetime(2018, 1, 1, hour=1, minute=30)
        end = start + datetime.timedelta(days=90)
        # end = datetime.datetime(2018, 2, 28, hour=23, minute=50)
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)

        return start + datetime.timedelta(seconds=random_second)

    def dummyNote(self):
        """Return a random string."""
        lastName = [
            "Aguilera", "Aguilar", "Casas", "Cossio", "Escobedo", "Antunez",
            "Solis", "Saravia", "Garcia", "Martinez", "Vizcarra", "Silerio",
            "Treviño", "Mesa", "Fernandez", "Ramos", "Russek", "Vargas",
            "Alvarado", "Saltijeral", "Rodriguez", "Barrera", "Hernandez",
            "Felix", "Diaz", "Belausteguigoitia", "Giacoman"
            ]
        activity = [
            "Boda", "Reunion", "Familia", "Fiesta", "Tertulia",
            "Primera Comunión", "Club"
            ]

        words = [
            "Splatoon", "INC", "Coral", "Fox", "Canal", "Banda", "PC", "Coca",
            "THC", "Gema", "Plateros", "BirdWatchers", "Ciclistas", "Motos",
            "Panamericana"
            ]
        lists = [lastName, activity, words]
        note = ""
        for i in range(random.randint(1, 100)):
            li = random.sample(lists, 1)[0]
            word = random.sample(li, 1)
            note = note + " " + word[0]
        return note.strip()

    def dummyEmail(self):
        """Return random first name."""
        names = [
            "Antonio", "Ana", "Brenda", "Carlos", "Cecilia", "Daniela",
            "David", "Diana", "Edgar", "Esteban", "Enya", "Fabiola",
            "Gabriela", "Ines", "Juan", "Jose", "Jesus", "Jimena", "Jorge",
            "Maria", "Maricela", "Mario", "Miguel", "Antonieta", "Luis",
            "Luisa", "Regina", "Renata", "Alejandro", "Alejandra", "Francisco",
            "Salvador", "Ignacio", "Walter", "Arturo", "Hector", "Splatoon",
            "INC", "Coral", "Fox", "Canal", "Banda", "PC", "Coca", "THC",
            "Gema", "Plateros", "BirdWatchers", "Ciclistas", "Motos",
            "Panamericana"
            ]
        esp = [
            "gmail.com", "hotmail.com", "hotmail.com.mx", "live.com",
            "live.com.mx", "hotmail.es"
            ]
        if random.random() > 0.6:
            return random.sample(names, 1)[0] + "." + random.sample(
                names, 1)[0] + "@" + random.sample(esp, 1)[0]
        else:
            return random.sample(names, 1)[0] + "@" + random.sample(esp, 1)[0]

    def dummyAddress(self):
        """Return a dummy address."""
        ownerID = None
        characters = [
            "A", "B", "C", "D", "E", "F", "0", "1", "2", "3", "4", "5", "6",
            "7", "8", "9"
            ]
        streets = [
            "CUITLAHUAC", "CUAUHTEMOC", "PATONI", "ZARAGOZA", "ARBOLES",
            "PALMAS", "PLANTAS", "VASOS", "CRISTAL", "GEMA", "CARRETE", "BUHO",
            "CABALLO", "CERRO", "CEDRO", "PICO", "HORIZABA", "POPOCATEPETL",
            "COATLICUE", "HIDALGO", "GATOS", "PERROS", "IGUANAS", "INGLATERRA",
            "FRANCIA", "MANDARIN", "VERDE", "AZUL", "AQUA", "GRIS", "FLORES",
            "MARGARITA", "AVIONES", "CARTON", "ESCALERA", "COLGANTE",
            "HOJUELA", "HOJAS"
            ]
        nationality = self.dummyNationality()
        country = nationality[0]
        region = nationality[1]
        city = nationality[2]
        street = random.sample(streets, 1)[0]
        zone = random.sample(streets, 1)[0]
        extNumber = "".join(random.choices(characters, k=5))
        intNumber = "".join(random.choices(characters, k=3))
        cp = "".join([str(random.randint(0, 9)) for i in range(5)])

        return [
            ownerID, country, region, city, street, zone, extNumber, intNumber,
            cp
            ]

    def dummyPhone(self):
        """Return random phone data."""
        ownerID = None

        countryCode = "+" + str("".join(
            [str(random.randint(0, 9)) for i in range(2)]))
        regionCode = int("".join(
            [str(random.randint(0, 9)) for i in range(3)]))
        phone = int("".join([str(random.randint(0, 9)) for i in range(7)]))
        if random.random() > 0.9:
            ext = int("".join([str(random.randint(0, 9)) for i in range(3)]))
        else:
            ext = ""
        name = self.dummyName()

        return [ownerID, countryCode, regionCode, phone, ext, name]

    def dummyParking(self):
        """Return dummy parking data."""
        characters = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
            ]
        plateNo = "".join(random.choices(characters, k=7))
        cars = [
            "Transdeet", "Tritned", "Dlunt", "Cippa", "Ragunk", "Znasot",
            "Resless", "Techore", "Congent", "Uezhoe", "Extranaw", "Stacize",
            "Cosso", "Kefo", "Knuhile", "Bizan", "Tranoom", "Parop",
            "Semigawn", "Uphi", "Resewous", "Intersad", "Pingi", "Flungi",
            "Gexoat", "Voleat", "Exog", "Deout", "Trantiq", "Iru",
            "Transfable", "Gallxain", "Mumpa", "Vuca", "Qafouse", "Luvty",
            "Duay", "Autoun", "Subxan", "Ija", "Comoming", "Irleet", "Dishu",
            "Smarsi", "Lebter", "Twabap", "Iroof", "Scaram", "Staxod", "Uthe"
            ]
        car = "".join(random.choices(cars, k=1))

        return (None, plateNo, car)

    def dummySimpleContact(self):
        """Return a simple contact with random data."""
        if random.random() > 0.95:
            note = self.dummyNote()
        else:
            note = None

        return [None, self.dummyName(), self.dummyLastName(), note]

    def dummyNationality(self):
        """Return dummy nationality data (Country, Region, city)."""
        countries = [
            "EUA", "COLOMBIA", "ARGENTINA", "CANADA", "FRANCIA", "NORUEGA",
            "ITALIA", "CHINA", "TURQUIA", "GRECIA", "POLONIA", "DOCLOIYA",
            "OPLOYZE", "WOWHYAE", "QECLYE", "SCIUCE", "SNAERHIEL", "ASKUS",
            "PLUE STRARIA", "PRAU SKEAU"
            ]
        regions = [
            "TUCHUYNGA", "UGROYSO", "PUWHYE", "XOFRA", "TRAEYAE", "CLIOCOR",
            "ACHYAE", "OPLIL", "SWUOM STIA", "SKIOV CHARIA", "ESPEDOZA",
            "SAJÁN", "ABAZOS", "HUARAGUA", "SÃO LEOTÃO", "RECITANO", "CURIBEL",
            "CABREROS", "SAN JOSCADA", "CAAZAGUATAY", "PUTIGUA", "HUÁNUDÍN",
            "TOSANDÚ", "PACHO", "KIRKEHOLM", "MOSEHOLM", "TÜVERE", "RAKDUU",
            "ÄÄNEKO", "TURRINA", "AKUVERFI", "NESJAHSANDUR", "ALOLI",
            "AISALACA", "ŠIRNELIAI", "RUDIŠGALA", "DRØKANGER", "FOSSUND",
            "STRÖMHOLM", "VETTORP", "YEMEMERI", "GARDENEA", "SAN ANGACES",
            "MATILE", "TENANCAGUA", "ANTINANGO", "ANTITAPA", "GUASTALONGA",
            "NACAONOPE", "LEJANOPE", "TIZAS", "DIPIPANECA", "LA ESNAZAS",
            "LOS ALCUMEN"
            ]

        states = [
            "DURANGO", "COAHUILA", "SONORA", "PUEBLA", "SINALOA", "HIDALGO",
            "CHIHUAHUA", "NAYARIT", "ZACATECAS", "CHIAPAS", "CDMX", "MONTERREY"
            ]

        if random.random() > 0.80:
            country = random.sample(countries, 1)[0]
            region = random.sample(regions, 1)[0]
            city = random.sample(regions, 1)[0]
        else:
            country = "MÉXICO"
            region = random.sample(states, 1)[0]
            city = random.sample(regions, 1)[0]

        return (country, region, city)

    def dummyRsvStatus(self, dateIn, dateOut):
        """Reservation status codes.

        status = {
            0: "New",
            1: "Processed/Confirmed",
            2: "Checked IN"
            3: "Checked Out",
            4: "Cancelled",
            5: "No Show",
            6: "Guaranteed",
            7: "Early Checkout"
        }
        """
        today = datetime.datetime.today()
        # check-in today
        if dateIn == today:
            status = 1

        # Already Checked In
        if dateIn < today and dateOut > today:
            status = 2
            if random.random() > 0.97:
                status = 7

        # Future check-in
        if dateIn > today:
            status = 1
            if random.random() > 0.7:
                status = 0
            elif random.random() > 0.95:
                status = 6

        # Already checked out
        if dateOut < today:
            status = 3

        # random no-show
        if random.random() > 0.97:
            status = 5

        # random cancellation
        if random.random() > 0.97:
            status = 4

        return status

    def dummyRoomData(self):
        """Return random room data."""
        # tipo = [id, "description", beds, maxCapacity]
        tipo = [(1, "SENCILLO", 1, 1), (2, "DOBLE", 1, 2), (3, "TRIPLE", 2, 3),
                (4, "QUEEN", 1, 2), (5, "KING", 1, 2), (6, "DOBLE DOBLE", 2,
                                                        4)]
        characters = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Ñ"
            ]
        # stats = ["LIBRE", "EN LIMPIEZA", "OCUPADO", "FUERA DE SERVICIO"]
        # For testing, 5% of rooms will be out of service.
        if random.random() < 0.95:
            stat = random.randint(0, 1)
        else:
            stat = 3

        # extras = ["SERVIBAR", "AC", "TV", "CAJA FUERTE", "FUMAR"]
        exNo = random.randint(0, 4)  # random number of extras in room.
        roomExtras = random.sample(range(5), exNo)
        roomExtras.sort()

        # type setup
        tipoNo = random.randrange(len(tipo))
        tipo = tipo[tipoNo]

        # note setup
        if random.random() > 0.95:
            note = self.dummyNote()
        else:
            note = None

        numero = random.sample(characters, 3)[:]
        numero = "".join(numero)

        roomGroup = random.randint(1, 10)

        return [(numero, tipo[0], stat, 0, note, roomGroup), roomExtras]

    def dummyGuestData(self):
        """Return random guest data."""
        name = self.dummyFirstName()
        lastName = self.dummyLastName()

        # self.guestID is a pyisical ID and can be a passport, driving license etc.
        # self.guestID must be formatted [idType, idNumber]
        ids = ["PASAPORTE", "LICENCIA DE MANEJO", "INE", "INSEN", "IFE"]
        ID = random.sample(ids, 1)[0]

        characters = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
            ]
        IDNo = "".join(random.choices(characters, k=13))
        guestIDD = [None, ID, IDNo]

        age = random.randrange(18, 100)

        if random.random() < 0.8:
            addresses = [self.dummyAddress()]
        else:
            addresses = [self.dummyAddress(), self.dummyAddress()]
        if random.random() < 0.8:
            phones = [self.dummyPhone()]
        else:
            phones = [self.dummyPhone(), self.dummyPhone()]
        if random.random() < 0.8:
            emails = [[None, self.dummyEmail(), self.dummyName()]]
        else:
            emails = [[None, self.dummyEmail(),
                       self.dummyName()],
                      [None, self.dummyEmail(),
                       self.dummyName()]]

        if random.random() > 0.95:
            note = self.dummyNote()
        else:
            note = None

        return [[name, lastName, age, note], guestIDD, phones, addresses,
                emails]

    def dummyCompanyData(self):
        """Return random company data."""
        names = [
            "Fairy Security", "Prodigy Industries", "Great White Media",
            "Riverecords", "Spiritechnologies", "Smartechnologies",
            "Cliffoods", "Happyshadow", "Globalbooks", "Starsun",
            "Bear Paw Brews", "Ridge Acoustics", "Angel Productions",
            "Equinetworks", "Neroductions", "Shadoworks", "Equinetworks",
            "Oceanking", "Silverdream", "Shadebridge", "Thunder Brews",
            "Zeus Softwares", "Cloud Acoustics", "Tucanterprises",
            "Rosecurity", "Oceanavigations", "Moondustries", "Redfly",
            "Blossomwheels", "Coremart"
            ]

        characters = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
            ]

        businessName = random.sample(names, 1)[0]
        companyName = random.sample(names, 1)[0] + " SA de CV"

        if random.random() < 0.8:
            addresses = [self.dummyAddress()]
        else:
            addresses = [self.dummyAddress(), self.dummyAddress()]
        if random.random() < 0.8:
            phones = [self.dummyPhone()]
        else:
            phones = [self.dummyPhone(), self.dummyPhone()]
        if random.random() < 0.8:
            emails = [[None, self.dummyEmail(), self.dummyName()]]
        else:
            emails = [[None, self.dummyEmail(),
                       self.dummyName()],
                      [None, self.dummyEmail(),
                       self.dummyName()]]

        RFC = random.sample(characters, 13)[:]
        RFC = "".join(RFC)

        contact = self.dummySimpleContact()

        if random.random() > 0.95:
            note = self.dummyNote()
        else:
            note = None

        return [[businessName, companyName, RFC, note], contact, phones,
                addresses, emails]

    def dummyUserData(self):
        """Return random user data."""
        Type = 0  # [ADMIN=0, USER=1]]

        name = self.dummyFirstName()
        lastName = self.dummyLastName()

        if random.random() > 0.95:
            note = self.dummyNote()
        else:
            note = None

        today = datetime.datetime.today().date()

        return (0, Type, name, lastName, note, "password", today, 0)

    def dummyRsvData(self, start):
        """Return random reservation data."""
        if random.random() > 0.7:
            adults = random.randint(1, 10)
            minors = random.randint(0, 5)
        else:
            adults = random.randint(1, 3)
            minors = random.randint(0, 2)

        # rooms = [(number of rooms, room type),]
        if adults + minors > 5:
            rooms = [random.randint(1, 6)]
            roomTypes = [random.randint(1, 6) for x in range(len(rooms))]
            group = self.dummyGroup()
        else:
            roomTypes = [random.randint(1, 6)]
            rooms = [random.randint(1, 6)]
            group = None

        dates = self.dummyDates(start)
        dateIn = dates[0]
        dateOut = dates[1]

        rate = random.randint(1000, 3000)

        status = self.dummyRsvStatus(dateIn, dateOut)

        today = datetime.datetime.today()

        paid = None

        if status == 3 or status == 7:
            days = (dateOut - dateIn).days
            paid = rate * days

        if status == 2:
            days = (today - dateIn).days
            paid = rate * days

        # if paid is None:
        #     paid = 0

        # extras = ["SERVIBAR", "AC", "TV", "CAJA FUERTE", "FUMAR", "PARKING"]
        exNo = random.randint(0, 4)  # random number of extras in room.
        extras = random.sample(range(5), exNo)
        extras.sort()

        if random.random() > 0.65:
            note = self.dummyNote()
        else:
            note = None

        # TODO: The other guest list must be an array with a list per room on group
        if adults + minors > 1:
            otherGuests = []
            for i in range((adults + minors) - 1):
                otherGuests.append(self.dummySimpleContact())
        else:
            otherGuests = None
        if status not in [2, 3, 7]:
            otherGuests = None

        guestID = None
        statusID = 0
        userID = 0
        companyID = None
        if 5 in extras:
            if group:
                parking = [self.dummyParking(), self.dummyParking()]
            else:
                parking = [self.dummyParking()]
        else:
            parking = None

        roomNo = None
        roomType = None
        return [[
            guestID, statusID, userID, companyID, adults, minors,
            dateIn.date(),
            dateOut.date(), rate, paid, group, roomNo, roomType, note
            ], rooms, roomTypes, otherGuests, extras, parking]


# db = Db()
# startConnection = db.startConnection()
# connection = startConnection[0]
# cursor = startConnection[1]
#
# dateIn = datetime.datetime.today().date()
# dateOut = dateIn + datetime.timedelta(days=30)
# rooms = db.getRoomOfTypeInGroup(3, 1, cursor)
#
# db.endConnection(connection)
# print(rooms)
# #
# db = Db()
# dummy = dummyDb()
# dummy.dummyDB()

# dummy = dummyGenerator()
# tries = []
# for i in range(1000):
#     x = 0
#     for i in range(100):
#         dumy = dummy.dummyRsvData()
#         if dumy[6] == 4:
#             x += 1
#     tries.append(x)
# allsum = 0
# for tri in tries:
#     allsum += tri
# print(allsum / len(tries))
# rooms = {}
# for i in range(10):
#     rooms[i] = dummy.dummyRoomData()
#
# for i in rooms.items():
#     print(i)
