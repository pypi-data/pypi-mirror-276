# Changelog

Released versions of libABCD

## [2.1.0] - 2024-05-31

### Added

- gitlab CI/CD auto deploy to pypi

### Changed

- callbacks added with `libabcd.add_callback()` can now receive empty payloads

## [2.0] - 2024-03-27

### Added

- New logging handler (ABCDHandler) added to a root logger

### Removed

- ABCDLogger


## [1.0.0] - 2023-07-18

### Added

- installation instructions in README.md

### Changed

- "info" level of loggings now goes through MQTT


## [0.3.0] - 2023-03-16

### Added

- naming for unique clients
- logging handled by class ABCDlog

### Changed

- major change: most source files removed, all source code is in `__init__.py`
- libABCD objects now have two separate mqtt clients for publishing and listening
- new options for status reporting and ping/pong system
- new `add_callback()` function instead of old `add_handler()`

### Removed
- examples folder (is normally DAQ specific)


## [0.2.0] - 2021-04-27

### Changed

- major change: internal system now based on mqtt
- run.py config file experiment.json updated to new format

### Removed

- abcsServer is no longer needed as it is replaced by mosquitto

## [0.1.2] - 2020-10-30

### Added

- options to change stdout level of verbose
- function to change server
- added TODO about future code plans

## [0.1.1] - 2020-06-03

### Added

- CHANGELOG, following https://keepachangelog.com/ and updated to semantic versioning
- setup.py includes description from README
- added example monitoring code
- moved all example code to examples directory

### Changed

- pong messages from server changed to \_pong, now ignored by default

## [0.1] - 2020-06-02

### Added

- libABCD providing an init, logger, server connect, UDP broadcast server discovery, message handling, ping/pong system, watchdog system
- abcdServer.py example main server
- S.py example logger
- run.py example run manager (with damicm.json config file)
- exec-client.py cient accepting and executing python commands (highly unsecure!)
- send.py simple message sender example
- README, LICENSE, and pypi setup for pip(3)

[unreleased]: https://gitlab.com/bertou/libabcd/-/compare/v0.1.2...master
[2.1.0]: https://gitlab.com/bertou/libabcd/-/tags/v2.1.0
[2.0]: https://gitlab.com/bertou/libabcd/-/tags/v2.0
[1.0.0]: https://gitlab.com/bertou/libabcd/-/tags/v1.0.0
[0.3.0]: https://gitlab.com/bertou/libabcd/-/tags/v0.3.0
[0.2.0]: https://gitlab.com/bertou/libabcd/-/tags/v0.2.0
[0.1.2]: https://gitlab.com/bertou/libabcd/-/tags/v0.1.2
[0.1.1]: https://gitlab.com/bertou/libabcd/-/tags/v0.1.1
[0.1]: https://gitlab.com/bertou/libabcd/-/tags/v0.1
