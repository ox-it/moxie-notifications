Endpoint
========

Endpoint to create and retrieve notifications

.. http:post:: /alert

    Create a new alert
    
    Requires authentication
    
    **Example request**:
    
    .. sourcecode:: http

        POST /alert HTTP/1.1
        Host: api.m.ox.ac.uk
        Content-Type: application/json
    
        {
            "message": "Bomb threat at X",
        }

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 201 Created
        Location: /alert/{uuid}

    :statuscode 201: alert created
    :statuscode 400: bad request
    :statuscode 401: authentication error

.. http:post:: /push

    Request the alert to be pushed to registered devices
    
    Requires authentication
    
    **Example request**:
    
    .. sourcecode:: http
    
        POST /push HTTP/1.1
        Host: api.m.ox.ac.uk
        Content-Type: application/json
        
        {
            "alert": "{uuid}",
            "message": "Bomb threat at X, avoid the area"
        }
        
    **Example response**:
    
    .. sourcecode:: http
    
        HTTP/1.1 202 Accepted
        
    :statuscode 202: push request queued
    :statuscode 400: bad request
    :statuscode 401: authentication error

.. http:post:: /alert/(string:uuid)

    Update an alert
    
    Requires authentication

    **Example request**:
    
    .. sourcecode:: http

        POST /alert/X HTTP/1.1
        Host: api.m.ox.ac.uk
        Content-Type: application/json
    
        {
            "message": "Bomb threat at X, avoid the area!",
        }

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK
        Location: /alert/{uuid}

    :param uuid: unique identifier of the alert
    :type uuid: string

    :statuscode 200: update applied correctly
    :statuscode 400: bad request
    :statuscode 401: authentication error
    :statuscode 404: alert not found

.. http:post:: /alert/(string:uuid)/followup

    Add a follow up to an existing alert
    
    Requires authentication
    
    **Example request**:
    
    .. sourcecode:: http

        POST /alert/X/followup HTTP/1.1
        Host: api.m.ox.ac.uk
        Content-Type: application/json
    
        {
            "message": "security services have arrived on scene",
        }

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 201 Created
        Location: /alert/X/followup/1

    :param uuid: unique identifier of the alert
    :type uuid: string

    :statuscode 201: followup created
    :statuscode 400: bad request
    :statuscode 401: authentication error
    :statuscode 404: alert not found

.. http:post:: /alert/(string:uuid)/followup/(string:id)

    Update a follow up
    
    Requires authentication

    **Example request**:
    
    .. sourcecode:: http

        POST /alert/X/followup/1 HTTP/1.1
        Host: api.m.ox.ac.uk
        Content-Type: application/json
    
        {
            "message": "Fire department working",
        }

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK
        Location: /alert/{uuid}/followup/1

    :param uuid: unique identifier of the alert
    :type uuid: string
    :param id: identifier of the followup
    :type id: string

    :statuscode 200: update applied correctly
    :statuscode 400: bad request
    :statuscode 401: authentication error
    :statuscode 404: alert not found or followup not found

.. http:delete:: /alert/(string:uuid)

    Delete an alert
    
    Requires authentication

    **Example request**:
    
    .. sourcecode:: http

        DELETE /alert/X HTTP/1.1
        Host: api.m.ox.ac.uk

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK

    :param uuid: unique identifier of the alert
    :type uuid: string

    :statuscode 200: deleted
    :statuscode 401: authentication error
    :statuscode 404: non existing alert

.. http:delete:: /alert/(string:uuid)/followup/(string:id)

    Delete a follow up
    
    Requires authentication

    **Example request**:
    
    .. sourcecode:: http

        DELETE /alert/X/followup/1 HTTP/1.1
        Host: api.m.ox.ac.uk

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK

    :param uuid: unique identifier of the alert
    :type uuid: string
    :param id: identifier of the follow up
    :type id: string

    :statuscode 200: deleted
    :statuscode 401: authentication error
    :statuscode 404: alert not found or follow up not found

.. http:get:: /alerts

    Get ongoing alerts

    **Example request**:
    
    .. sourcecode:: http

        GET /alerts HTTP/1.1
        Host: api.m.ox.ac.uk
        Accept: application/json

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json
        
        {
            "alerts": [
                {
                    "uuid": "X",
                    "timestamp": "2013-02-08T12:30",
                    "message": "Bomb threat at X",
                    "displayUntil": "2013-02-08:16:00",
                    "followups": [
                        {
                            "timestamp": "2013-02-08T13:30",
                            "id": 1,
                            "message": "bla bla"
                        },
                        ...
                    ]
                }
            ]
        }

    :query history: display passed alerts (defaults to false)

    :statuscode 200: response ok

.. http:get:: /alert/(string:uuid)

    Get an alert

    **Example request**:
    
    .. sourcecode:: http

        GET /alert/X HTTP/1.1
        Host: api.m.ox.ac.uk
        Accept: application/json

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json
        
        {
            "uuid": "X",
            "timestamp": "2013-02-08T12:30",
            "message": "Bomb threat at X,
            "displayUntil": "2013-02-08:16:00",
            "followups": [
                {
                    "timestamp": "2013-02-08T13:30",
                    "id": 1,
                    "message": "bla bla"
                },
                ...
            ]
        }
        
    :statuscode 200: response ok
    :statuscode 404: alert not found
    