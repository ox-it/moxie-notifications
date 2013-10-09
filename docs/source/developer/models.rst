Models
======

An ``alert`` is the top-level object which MAY contain a number of ``followup``.

Alert
-----

**Properties**:

* ``message``: main content of the alert
* ``initialDate``: date when the alert has been created
* ``displayUntil``: alert valid until given date

**Relations**:

* list of ``followup``

Follow up
---------

**Properties**:

* ``message``: message of the follow up
* ``timestamp``: date of the follow up

**Relations**:

* ``alert``: parent alert of the follow up

Push
----

**Properties**:

* ``message``: message of the push alert (restricted to X characters)

**Relations**:

* ``alert``: 

