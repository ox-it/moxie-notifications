import uuid
from datetime import datetime, timedelta

from moxie.core.db import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, index=True, unique=True)
    message = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    expires = db.Column(db.DateTime)
    url = db.Column(db.String)
    followups = db.relationship("FollowUp")

    def __init__(self, message, ident=None, timestamp=None, expires=None, url=None):
        if not ident:
            self.uuid = str(uuid.uuid4())
        else:
            self.uuid = ident
        self.message = message
        self.timestamp = timestamp or datetime.now()
        self.expires = expires or datetime.now() + timedelta(hours=1)
        self.url = url

    def __repr__(self):
        return "<Notification('{uuid}')>".format(uuid=self.uuid)

    def as_dict(self):
        values = {'message': self.message}
        if self.uuid:
            values['ident'] = self.uuid
        if self.timestamp:
            values['timestamp'] = self.timestamp.isoformat()
        if self.expires:
            values['expires'] = self.expires.isoformat()
        if self.url:
            values['url'] = self.url
        return values


class FollowUp(db.Model):
    __tablename__ = 'followups'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'))

    def __init__(self, message):
        self.message = message
        self.timestamp = datetime.now()

    def __repr__(self):
        return "<FollowUp('{id}')>".format(id=self.id)

    def as_dict(self):
        values = {'message': self.message,
                  'timestamp': self.timestamp.isoformat()}
        return values


class PushNotification(db.Model):
    __tablename__ = 'pushnotifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'))
    notification = db.relationship("Notification")

    def __init__(self, message, notification):
        self.message = message
        self.notification = notification
        self.timestamp = datetime.now()

    def __repr__(self):
        return "<PushNotification('{id}')>".format(id=self.id)
