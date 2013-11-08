Configuration
=============

Database
--------

You do need to have a database configured, the key ``SQLALCHEMY_DATABASE_URI`` in the ``flask`` section should be documented.

See `SQLAlchemy documentation <http://docs.sqlalchemy.org/en/rel_0_8/core/engines.html>`_ for more information on engines.

::

    flask:
        SQLALCHEMY_DATABASE_URI: 'sqlite:////tmp/test.db'


NotificationsService
--------------------

There is no configuration required for the ``NotificationsService`` itself. Configuration is instead required for the individual providers themselves.

moxie_notifications.providers.gcm.GCMProvider:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

api_key
    API Key obtained from Google.

url
    (optional) URL to GCM Server.

moxie_notifications.providers.apns.APNSProvider:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

address
    Address to APNS server.

cert_file
    Path to the certificate file (PEM format) registered with APNS.

key_file
    (optional) Path to key in PEM format from file.

passphrase
    (optional) Passphrase for private key file.

moxie_notifications.providers.mail.EmailNotificationsProvider
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is mainly used for development purpose.

smtp_server
    Address of the SMTP server

sender_email
    Email address of the sender

send_to
    List of email addresses where notifications should be send to

Example Configuration
---------------------

::

    notifications:
        NotificationsService:
            providers:
              moxie_notifications.providers.gcm.GCMProvider:
                  api_key: 'APIKEY'
              moxie_notifications.providers.apns.APNSProvider:
                  address: 'push_sandbox'
                  cert_file: '/srv/moxie/foo.pem'
              moxie_notifications.providers.mail.EmailNotificationsProvider:
                   smtp_server: 'smtp.com'
                   sender_email: 'noreply@msmsms.com'
                   send_to: ['user@msmsmsms.com']

        KVService:
            backend_uri: 'redis://localhost:6379/4'
