# frontDesk Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).
___

## Unreleased 0.8.0 Alpha
### Added
- main.py:
  - Added the method changeDisplay to use whenever the display must be changed.
  - Added the method getVersion to get the current version from the changelog file.
  - Added the logout method to allow logging out of a session.

### Removed
- main.py:
  - Removed the restart method because it was redundant.

### Modified
- main.py:
  - Modified to get the version number from the changelog file.
  - Modified to use a function to change what is displayed.
  - Modified to pass itself as an argument to its children so they can make use of its methods easier.

- Session.py
  - Modified the class to require the main window be passed on instantiation so it can use it's methods and pass it to the children easier.
  - Modified to make use of the getVersion method of the main window.

- MenuBar.py:
  - Modified to require the main window be passed on instantiation so it can make use of it's methods.
  - Modified to start adding signals functionality to the buttons.
  - Modified to stop using icons.

- Buttons.py:
  - MenuBarBtn was modified to stop creating null QPixmaps when no icon is passed to it.

- CHANGELOG.md:
  - Modified to add a line separator in between versions.

___
## V0.7.0
### Added
- Added Login.py, it is a login window widget that starts the program.
- Added ICG.py, it is an Initial Credentials Generator for the first time the program runs.
- Added Dialogs, it is where the pop up dialogs code is found.
- Added Validators.py, it contains functions to validate input data.

### Modified
- Modified main.py to prompt for the creation of a root and admin users when there are no registered users in the program (First time it runs.)
- Modified main.py to show the login widget before showing the dashboard.
- Modified Db.py to add functions to get data from the database.
- Modified Session.py to get the user data and show it on the window name.
- Modified dbVisualizer.py to show user data for testing.
- Modified CHANGELOG.md to say 'Modified' instead of changed, also fixed a typo.

___
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

### Modified
- Changed the SideBar to a MenuBar so the layout makes more sense.
- Changed the way data is passed around after it is returned by the database.
- Changed the dashboard items classes to make them easier to debug.
- Changed the way the dashboard items are created.
- Changed the way the dashboard items get and use their information.
- Changed the way the dashboard room items layout, now it will be a masonry like layout.
- The dummy database now takes the date it is created on as a base for the reservations dates.
- Changed the overall visual style of the dashboard.
- Changed some behaviors of the main window layout.

___
## V0.5.0
### Modified
- Simplified the connections to the database. Now the same connection is used throughout
    the lifetime of the program.

___
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

___
## V0.3.0
### Added
- New SideBar module and SideBar class. The sidebar is a qwidget object that
    contains buttons, metadata and has a background to separate it visually
    from where it's placed.
- New SideBarBtn, it is a fixed size solid background button and can
    contain an icon and a label.

___
## V0.2.0
### Added
- The program now works with sessions that must be started with user data.
    User data is not being used, it is just a placeholder for now.

___
## V0.1.0
### Added
- Changelog.md
- main.py added and filled with the most basic PyQt5 empty window.

### Modified
-README.md was changed to show more information about the project.
