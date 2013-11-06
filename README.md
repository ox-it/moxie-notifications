moxie-notifications
===================

Moxie module for generic notifications

See documentation: http://moxie-notifications.readthedocs.org/

Example requests
----------------

Retrieve all alerts

    curl "http://127.0.0.1:5000/notifications/alerts"

Create a new alert

    curl -i -X POST "http://127.0.0.1:5000/notifications/alert" -d '{"message": "Panic panic"}'

Retrieve an alert by its ID

    curl "http://127.0.0.1:5000/notifications/alert/f441a2eb-5784-4950-8778-fd322b65a0f8"

Delete an alert

    curl -X DELETE "http://127.0.0.1:5000/notifications/alert/f441a2eb-5784-4950-8778-fd322b65a0f8"
