import uuid
from datetime import datetime, timedelta

from moxie.core.db import db


class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, index=True, unique=True)
    message = db.Column(db.String)
    from_date = db.Column(db.DateTime)
    display_until = db.Column(db.DateTime)
    followups = db.relationship("FollowUp")

    def __init__(self, message, ident=None, from_date=None, display_until=None):
        if not ident:
            alert_uuid = uuid.uuid4()
            self.uuid = str(alert_uuid)
        else:
            self.uuid = ident
        self.message = message
        self.from_date = from_date or datetime.now()
        self.display_until = display_until or datetime.now() + timedelta(hours=1)

    def __repr__(self):
        return "<Alert('{uuid}')>".format(uuid=self.uuid)

    def as_dict(self):
        values = {'message': self.message}
        if self.uuid:
            values['ident'] = self.uuid
        if self.from_date:
            values['fromDate'] = self.from_date.isoformat()
        if self.display_until:
            values['displayUntil'] = self.display_until.isoformat()
        return values


class FollowUp(db.Model):
    __tablename__ = 'followups'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    alert_id = db.Column(db.Integer, db.ForeignKey(Alert.__tablename__+'.id'))

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return "<FollowUp('{id}')>".format(id=self.id)

    def as_dict(self):
        values = {'message': self.message}
        return values


class PushAlert(db.Model):
    __tablename__ = 'pushalerts'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    alert_id = db.Column(db.Integer, db.ForeignKey(Alert.__tablename__+'.id'))
    alert = db.relationship("Alert")

    def __init__(self, message, alert):
        self.message = message
        self.alert = alert

    def __repr__(self):
        return "<PushAlert('{id}')>".format(id=self.id)
