# frontDesk Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## V0.6.0
### Added
- Added color to the debug prints to be able to know what's going on.
- Added a way to turn off all prints so they only show when debugging.
- Added a way to write the error logs to a file after freezing.
- Added a way to create new dummy data for debugging every time the program starts.
- Added the name of the current version to the window title.

### Removed
- Removed the need to use data objects for the data to be passed around.
    ~ Removed People.py
    ~ Removed Reservation.py
    ~ Removed Room.py
    ~ Removed DataItems.py
    ~ Removed person.png

### Changed
- Changed the SideBar to a MenuBar so the layout makes more sense.
- Changed the way data is passed around after it is returned by the database.
- Changed the dashboard items classes to make them easier to debug.
- Changed the way the dashboard items are created.
- Changed the way the dashboard items get and use their information.
- Changed the way the dashboard room items layout, now it will be a masonry like layout.
- The dummy database now takes the date it is created on as a base for the reservations dates.
- Changed the overall visual style of the dashboard.
- Changed some behaviors of the main window layout.

## V0.5.0
### Changed
- Simplified the connections to the database. Now the same connection is used throghout
    the lifetime of the program.

## V0.4.0
### Added
- New module Dashboard. The dashboard will show lists with relevant room/reservation data
    (eg. today's check-in and check-out data).
    These lists items can be interactive.
- New module DataItems. Contains the class that is the base for the data representations
    of other modules that share some basic features.
- New modules Reservation and Room. Each containing its graphic and data representation.
- New module People. Contains Guest, Company, and User graphic and data representations.
- New module Db. Handles the communication with de database.
- New module Manager. handles the interactions between the UI and the database


## V0.3.0
### Added
- New SideBar module and SideBar class. The sidebar is a qwidget object that
    contains buttons, metadata and has a background to separate it visually
    from where it's placed.
- New SideBarBtn, it is a fixed size solid background button and can
    contain an icon and a label.

## V0.2.0
### Added
- The program now works with sessions that must be started with user data.
    User data is not being used, it is just a placeholder for now.

## V0.1.0
### Added
- Changelog.md
- main.py added and filled with the most basic PyQt5 empty window.

### Changed
-README.md was changed to show more information about the project.
