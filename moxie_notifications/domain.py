from datetime import datetime, timedelta

from moxie.core.exceptions import BadRequest


PUSH_VALIDATION_MESSAGE = "You must pass a JSON document with properties 'alert' and 'message'."
ALERT_VALIDATION_MESSAGE = "You must pass a JSON document with property 'message'."


class PushAlert(object):
    """Represents a push alert
    """

    def __init__(self, notification_ident, message):
        self.notification_ident = notification_ident
        self.message = message

    @staticmethod
    def from_json(json):
        if not json or 'alert' not in json or 'message' not in json:
            raise BadRequest(PUSH_VALIDATION_MESSAGE)
        return PushAlert(json['alert'], json['message'])


class Alert(object):

    def __init__(self, message, initial_date=None, display_until=None):
        self.message = message
        self.initial_date = initial_date or datetime.now()
        self.display_until = display_until or datetime.now() + timedelta(hours=1)

    @staticmethod
    def from_json(json):
        if not json or 'message' not in json:
            raise BadRequest(ALERT_VALIDATION_MESSAGE)
        return Alert(json['message'],
                     initial_date=json.get('initialDate', None),
                     display_until=json.get('displayUntil', None))
