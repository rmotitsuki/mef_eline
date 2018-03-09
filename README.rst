Overview
========

.. attention::

    THIS NAPP IS STILL EXPERIMENTAL AND IT'S EVENTS, METHODS AND STRUCTURES MAY
    CHANGE A LOT ON THE NEXT FEW DAYS/WEEKS, USE IT AT YOUR OWN DISCERNEMENT

This Napp allows a user to create a point to point L2 Ethernet Virtual Circuit.

When fully implemented, this napp will provide a REST API to create/modify/delete circuits. For now, the list of installed circuits is kept in memory,
but it should be later kept in a permanent storage.
Circuits will be installed at the time of request or at a predefined time, and can also have a time to be deleted.
The Napp also will listen for PortStatus events, modifying circuits that use a port that went down.

Requirements
============
- kytos/flow_manager
- kytos/pathfinder
