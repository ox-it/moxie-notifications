Endpoint
========

Format
------

Dates are expressed as YYYY-mm-DDTHH:mm:ss (e.g. ``2013-11-08T16:00:00``)

Methods
-------

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

    :jsonparam string message: the message of the alert
    :jsonparam date initialDate: (optional) start date of the alert (defaults to current time)
    :jsonparam date displayUntil: (optional) end date of the alert (defaults to one hour after current time)

    :statuscode 201: :http:statuscode:`201`: alert created
    :statuscode 400: :http:statuscode:`400`
    :statuscode 401: :http:statuscode:`401`

.. http:post:: /push

    Request an alert to be pushed to registered devices
    
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
        
    :jsonparam string alert: unique identifier of the alert
    :jsonparam string message: message of the push alert
        
    :statuscode 202: :http:statuscode:`202`: push request queued
    :statuscode 400: :http:statuscode:`400`
    :statuscode 401: :http:statuscode:`401`

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

    :jsonparam string message: the message of the alert
    :jsonparam date initialDate: (optional) start date of the alert
    :jsonparam date displayUntil: (optional) end date of the alert

    :statuscode 200: :http:statuscode:`200`: update applied correctly
    :statuscode 400: :http:statuscode:`400`
    :statuscode 401: :http:statuscode:`401`
    :statuscode 404: :http:statuscode:`404`: alert not found

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

    :jsonparam string message: the message of the follow up
    :jsonparam date timestamp: (optional) date of the follow up

    :statuscode 201: :http:statuscode:`201`: followup created
    :statuscode 400: :http:statuscode:`400`
    :statuscode 401: :http:statuscode:`401`
    :statuscode 404: :http:statuscode:`404`: alert not found

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

    :jsonparam string message: the message of the follow up
    :jsonparam date initialDate: (optional) date of the follow up

    :statuscode 200: :http:statuscode:`200`: update applied correctly
    :statuscode 400: :http:statuscode:`400`
    :statuscode 401: :http:statuscode:`401`
    :statuscode 404: :http:statuscode:`404`: alert not found or followup not found

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

    :statuscode 200: :http:statuscode:`200`: alert deleted
    :statuscode 401: :http:statuscode:`401`
    :statuscode 404: :http:statuscode:`404`: alert not found

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

    :statuscode 200: :http:statuscode:`200`: follow up deleted
    :statuscode 401: :http:statuscode:`401`
    :statuscode 404: :http:statuscode:`404`: alert not found or follow up not found

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

    :query history: boolean value ("true", "True", "1", "t") to display all alerts (defaults to false)

    :statuscode 200: :http:statuscode:`200`

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
        
    :statuscode 200: :http:statuscode:`200`
    :statuscode 404: :http:statuscode:`404`: alert not found
    