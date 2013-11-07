Typical scenario when using the API to create an alert
======================================================

Create a new alert
------------------

.. http:post:: /alert

    **Request**:
    
    .. sourcecode:: http

        POST /alert HTTP/1.1
        Host: api.ox.ac.uk
        Content-Type: application/json
    
        {
            "message": "Bomb threat at X",
            "displayUntil": "2013-11-08T16:00:00",
        }

    **Response**:
    
    .. sourcecode:: http

        HTTP/1.1 201 Created
        Location: /alert/16d4a94fc58111a323437ec363d71f5a


(Optionally) push the alert to registered devices
-------------------------------------------------

.. http:post:: /push

    **Request**:
    
    .. sourcecode:: http
    
        POST /push HTTP/1.1
        Host: api.ox.ac.uk
        Content-Type: application/json
        
        {
            "alert": "16d4a94fc58111a323437ec363d71f5a",
            "message": "Bomb threat at X, avoid the area"
        }
    
    **Response**:
    
    .. sourcecode:: http
    
        HTTP/1.1 202 Accepted


Add a follow up
---------------

.. http:post:: /alert/16d4a94fc58111a323437ec363d71f5a/followup

    **Request**:
    
    .. sourcecode:: http

        POST /alert/16d4a94fc58111a323437ec363d71f5a/followup HTTP/1.1
        Host: api.ox.ac.uk
        Content-Type: application/json
    
        {
            "message": "security services have arrived on scene",
        }

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 201 Created
        Location: /alert/16d4a94fc58111a323437ec363d71f5a/followup/1


Update the alert to be displayed until the end of the day
---------------------------------------------------------

.. http:post:: /alert/16d4a94fc58111a323437ec363d71f5a

    **Request**:
    
    .. sourcecode:: http

        POST /alert/16d4a94fc58111a323437ec363d71f5a HTTP/1.1
        Host: api.ox.ac.uk
        Content-Type: application/json
    
        {
            "displayUntil": "2013-02-08T18:00:00"
        }

    **Response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK
        Location: /alert/16d4a94fc58111a323437ec363d71f5a
