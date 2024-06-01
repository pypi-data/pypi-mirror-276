Autonomous Bariloche Central DAQ (libABCD) v2.1
===============================================

This library handles two crucial aspects of any experiment that consists 
of multiple clients taking data: the communication between clients and 
the log information.

The main concept for the DAQ is that it orbits around a central server. 
Control and information run through this server allowing a permanent 
follow-up of what is happening. The raw data is handled by the clients 
themselves and is not seen by the DAQ. The central server is a MQTT 
broker. We recommend using [`mosquitto`](https://mosquitto.org/).

Logs are handled by each client, but the `ABCDHandler` logging handler 
sends the relevant information through MQTT, allowing for a centralized 
monitoring.

Installation
------------

The latest version can be installed from pip:
```bash
python3 -m pip install libabcd
```

Usage
-----

`libABCD` is a singleton object (i.e. a single instance runs per python
process). Start it by running:
```python
import libABCD
libABCD.init()  # see documentation in the docstring
```
You can then `publish`, `subscribe`, `unsubscribe` and `add_callback` 
using the same object. Documentation can be found in the docstrings.  

Best practice for handling your application log:
```python
import logging
logger = logging.getLogger('your_app_name')
logger.addHandler(logging.NullHandler()) # remove all other handlers
logger.info('I am an INFO message') # or warning, error, critical
```

Don't forget to close the connection at the end of the session
```python
libABCD.disconnect()
```

A full documentation of the available features is under way.

Questions, requests, feedback
-----------------------------

If you find a bug, want to know more about specific features or have feedback
of any kind, do not hesitate to email me at nicolaseavalos AT gmail DOT com.

License
-------

This project is licensed under the MIT license.

