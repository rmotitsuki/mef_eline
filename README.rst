Overview
========

**WARNING: As previously announced on our communication channels, the Kytos
project will enter the "shutdown" phase on May 31, 2021. After this date,
only critical patches (security and core bug fixes) will be accepted, and the
project will be in "critical-only" mode for another six months (until November
30, 2021). For more information visit the FAQ at <https://kytos.io/faq>. We'll
have eternal gratitude to the entire community of developers and users that made
the project so far.**

|Experimental| |License| |Build| |Coverage| |Quality|


.. attention::

    THIS NAPP IS STILL EXPERIMENTAL AND IT'S EVENTS, METHODS AND STRUCTURES MAY
    CHANGE A LOT ON THE NEXT FEW DAYS/WEEKS, USE IT AT YOUR OWN DISCERNEMENT

This Napp allows a user to create a point to point L2 Ethernet Virtual Circuit.

When fully implemented, this napp will provide a REST API to create/modify/delete circuits. For now, the list of installed circuits is kept in memory,
but it should be later kept in a permanent storage.
Circuits will be installed at the time of request or at a predefined time, and can also have a time to be deleted.
The Napp also will listen for PortStatus events, modifying circuits that use a port that went down.

The cookie flow field is used to identify to which EVC the flow belongs. The first two bytes of the cookie is a prefix identifying the NApp using it,
and the remaining 14 bytes are the EVC id.

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