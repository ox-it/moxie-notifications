moxie-notifications
===================

Moxie module for generic notifications

See documentation: http://moxie-notifications.readthedocs.org/

Simple requests
---------------

Retrieve all alerts

    curl "http://127.0.0.1:5000/notifications/alerts"

Retrieve an alert by its ID

    curl "http://127.0.0.1:5000/notifications/alert/f441a2eb-5784-4950-8778-fd322b65a0f8"

Authenticated requests
----------------------

We include a simple bash script to help in building HMAC'd requests `auth_test.sh` which can be used in the following ways

Create a new alert

    ./auth_test.sh POST http://localhost:5000/notifications/alert myapikey mysharedsecret -d '{"message": "urgent message!"}'


Delete an alert

    ./auth_test.sh DELETE http://localhost:5000/notifications/alert/5203a863-40b3-45d4-b3a9-8e143ce6ea22 myapikey mysharedsecret
