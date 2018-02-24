# frontDesk Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased
### Added

### Removed

### Changed
- Changed the SideBar to a MenuBar so the layout makes more sense.

### Fixed

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
