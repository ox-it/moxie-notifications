Models
======

A ``notification`` is the top-level object which MAY contain a number of ``followup``.

Notification
------------

**Properties**:

* ``message``: main content of the notification
* ``timestamp``: date when the notification has been created
* ``expires``: notification valid until given date

**Relations**:

* list of ``followup``

Follow up
---------

**Properties**:

* ``message``: message of the follow up
* ``timestamp``: date of the follow up

**Relations**:

* ``notification``: parent notification of the follow up

Push notification
-----------------

**Properties**:

* ``message``: message of the push notification (restricted to X characters)

**Relations**:

* ``notification``: related notification for this push notification
