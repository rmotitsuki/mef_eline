Overview
========

|Experimental| |License| |Build| |Coverage| |Quality|


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
- kytos/topology


.. TAGs

.. |Experimental| image:: https://img.shields.io/badge/stability-experimental-orange.svg
   :target: https://github.com/kytos/mef_eline
.. |License| image:: https://img.shields.io/github/license/kytos/kytos.svg
   :target: https://github.com/kytos/mef_eline/blob/master/LICENSE
.. |Build| image:: https://scrutinizer-ci.com/g/kytos/mef_eline/badges/build.png?b=master
   :alt: Build status
   :target: https://scrutinizer-ci.com/g/kytos/kytos/?branch=master
.. |Coverage| image:: https://scrutinizer-ci.com/g/kytos/mef_eline/badges/coverage.png?b=master
   :alt: Code coverage
   :target: https://scrutinizer-ci.com/g/kytos/mef_eline/
.. |Quality| image:: https://scrutinizer-ci.com/g/kytos/mef_eline/badges/quality-score.png?b=master
   :alt: Code-quality score
   :target: https://scrutinizer-ci.com/g/kytos/mef_eline/