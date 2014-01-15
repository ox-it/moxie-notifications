Endpoint
========

Format
------

Dates are expressed as YYYY-mm-DDTHH:mm:ss (e.g. ``2013-11-08T16:00:00``)

Methods
-------

Endpoint to create and retrieve notifications

.. http:post:: /

    Create a new notification
    
    Requires authentication
    
    **Example request**:
    
    .. sourcecode:: http

        POST /notifications HTTP/1.1
        Host: api.m.ox.ac.uk
        X-Moxie-Key: d51459b5-d634-48f7-a77c-d87c77af37f1
        X-HMAC-Nonce: 12642
        Date: Fri, 10 Jan 2014 11:49:55 GMT
        Authorization: ccd61eddf0c6be849b13e524c171e4c14a0d571f
        Content-Type: application/json
    
        {
            "message": "Bomb threat at X",
        }

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 201 Created
        Location: /notifications/{uuid}

    :jsonparam string message: the message of the notification
    :jsonparam date timestamp: (optional) start date of the notification (defaults to current time)
    :jsonparam date expires: (optional) end date of the notification (defaults to one hour after current time)

    :statuscode 201: :http:statuscode:`201`: notification created
    :statuscode 400: :http:statuscode:`400`
    :statuscode 401: :http:statuscode:`401`

.. http:post:: /push

    Request a notification to be pushed to registered devices
    
    Requires authentication
    
    **Example request**:
    
    .. sourcecode:: http
    
        POST /push HTTP/1.1
        Host: api.m.ox.ac.uk
        X-Moxie-Key: d51459b5-d634-48f7-a77c-d87c77af37f1
        X-HMAC-Nonce: 12642
        Date: Fri, 10 Jan 2014 11:49:55 GMT
        Authorization: ccd61eddf0c6be849b13e524c171e4c14a0d571f
        Content-Type: application/json
        
        {
            "notification": "{uuid}",
            "message": "Bomb threat at X, avoid the area"
        }
        
    **Example response**:
    
    .. sourcecode:: http
    
        HTTP/1.1 202 Accepted
        
    :jsonparam string notification: unique identifier of the notification
    :jsonparam string message: message of the push notification
        
    :statuscode 202: :http:statuscode:`202`: push request queued
    :statuscode 400: :http:statuscode:`400`
    :statuscode 401: :http:statuscode:`401`

.. http:post:: /(string:uuid)

    Update a notification
    
    Requires authentication

    **Example request**:
    
    .. sourcecode:: http

        POST /notifications/X HTTP/1.1
        Host: api.m.ox.ac.uk
        X-Moxie-Key: d51459b5-d634-48f7-a77c-d87c77af37f1
        X-HMAC-Nonce: 12642
        Date: Fri, 10 Jan 2014 11:49:55 GMT
        Authorization: ccd61eddf0c6be849b13e524c171e4c14a0d571f
        Content-Type: application/json
    
        {
            "message": "Bomb threat at X, avoid the area!",
        }

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK
        Location: /notifications/{uuid}

    :param uuid: unique identifier of the notification
    :type uuid: string

    :jsonparam string message: the message of the notification
    :jsonparam date timestamp: (optional) start date of the notification
    :jsonparam date expires: (optional) end date of the notification

    :statuscode 200: :http:statuscode:`200`: update applied correctly
    :statuscode 400: :http:statuscode:`400`
    :statuscode 401: :http:statuscode:`401`
    :statuscode 404: :http:statuscode:`404`: notification not found

.. http:post:: /(string:uuid)/followup

    Add a follow up to an existing notification
    
    Requires authentication
    
    **Example request**:
    
    .. sourcecode:: http

        POST /notifications/X/followup HTTP/1.1
        Host: api.m.ox.ac.uk
        X-Moxie-Key: d51459b5-d634-48f7-a77c-d87c77af37f1
        X-HMAC-Nonce: 12642
        Date: Fri, 10 Jan 2014 11:49:55 GMT
        Authorization: ccd61eddf0c6be849b13e524c171e4c14a0d571f
        Content-Type: application/json
    
        {
            "message": "security services have arrived on scene",
        }

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 201 Created
        Location: /notifications/X/followup/1

    :param uuid: unique identifier of the notification
    :type uuid: string

    :jsonparam string message: the message of the follow up
    :jsonparam date timestamp: (optional) date of the follow up

    :statuscode 201: :http:statuscode:`201`: followup created
    :statuscode 400: :http:statuscode:`400`
    :statuscode 401: :http:statuscode:`401`
    :statuscode 404: :http:statuscode:`404`: notification not found

.. http:post:: /(string:uuid)/followup/(string:id)

    Update a follow up
    
    Requires authentication

    **Example request**:
    
    .. sourcecode:: http

        POST /notifications/X/followup/1 HTTP/1.1
        Host: api.m.ox.ac.uk
        X-Moxie-Key: d51459b5-d634-48f7-a77c-d87c77af37f1
        X-HMAC-Nonce: 12642
        Date: Fri, 10 Jan 2014 11:49:55 GMT
        Authorization: ccd61eddf0c6be849b13e524c171e4c14a0d571f
        Content-Type: application/json
    
        {
            "message": "Fire department working",
        }

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK
        Location: /notifications/{uuid}/followup/1

    :param uuid: unique identifier of the notification
    :type uuid: string
    :param id: identifier of the followup
    :type id: string

    :jsonparam string message: the message of the follow up
    :jsonparam date timestamp: (optional) date of the follow up

    :statuscode 200: :http:statuscode:`200`: update applied correctly
    :statuscode 400: :http:statuscode:`400`
    :statuscode 401: :http:statuscode:`401`
    :statuscode 404: :http:statuscode:`404`: notification not found or followup not found

.. http:delete:: /(string:uuid)

    Delete a notification
    
    Requires authentication

    **Example request**:
    
    .. sourcecode:: http

        DELETE /notifications/X HTTP/1.1
        Host: api.m.ox.ac.uk
        X-Moxie-Key: d51459b5-d634-48f7-a77c-d87c77af37f1
        X-HMAC-Nonce: 12642
        Date: Fri, 10 Jan 2014 11:49:55 GMT
        Authorization: ccd61eddf0c6be849b13e524c171e4c14a0d571f

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK

    :param uuid: unique identifier of the notification
    :type uuid: string

    :statuscode 200: :http:statuscode:`200`: notification deleted
    :statuscode 401: :http:statuscode:`401`
    :statuscode 404: :http:statuscode:`404`: notification not found

.. http:delete:: /(string:uuid)/followup/(string:id)

    Delete a follow up
    
    Requires authentication

    **Example request**:
    
    .. sourcecode:: http

        DELETE /notifications/X/followup/1 HTTP/1.1
        Host: api.m.ox.ac.uk
        X-Moxie-Key: d51459b5-d634-48f7-a77c-d87c77af37f1
        X-HMAC-Nonce: 12642
        Date: Fri, 10 Jan 2014 11:49:55 GMT
        Authorization: ccd61eddf0c6be849b13e524c171e4c14a0d571f

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK

    :param uuid: unique identifier of the notification
    :type uuid: string
    :param id: identifier of the follow up
    :type id: string

    :statuscode 200: :http:statuscode:`200`: follow up deleted
    :statuscode 401: :http:statuscode:`401`
    :statuscode 404: :http:statuscode:`404`: notification not found or follow up not found

.. http:get:: /

    Get ongoing notifications

    **Example request**:
    
    .. sourcecode:: http

        GET /notifications HTTP/1.1
        Host: api.m.ox.ac.uk
        Accept: application/json

    **Example response**:
    
    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json
        
        {
            "notifications": [
                {
                    "uuid": "X",
                    "timestamp": "2013-02-08T12:30",
                    "message": "Bomb threat at X",
                    "expires": "2013-02-08:16:00",
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

    :query history: boolean value ("true", "True", "1", "t") to display all notifications (defaults to false)

    :statuscode 200: :http:statuscode:`200`

.. http:get:: /(string:uuid)

    Get a notification

    **Example request**:
    
    .. sourcecode:: http

        GET /notifications/X HTTP/1.1
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
            "expires": "2013-02-08:16:00",
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
    :statuscode 404: :http:statuscode:`404`: notification not found
    
