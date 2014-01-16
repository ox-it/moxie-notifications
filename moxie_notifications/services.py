from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from moxie.core.service import ProviderService
from moxie.core.db import db

from moxie_notifications.domain import Notification, FollowUp

ANDROID = 'android'
iOS = 'iOS'


class NotificationsService(ProviderService):

    def __init__(self, *args, **kwargs):
        """Users passed here should be a simple dictionary of
        apikey, sharedsecret pairs.
        """
        self._users = kwargs.pop('users', {})
        super(NotificationsService, self).__init__(*args, **kwargs)

    def get_secret(self, api_key):
        return self._users[api_key]

    def register(self, token, platform):
        provider = self.get_provider(platform)
        return provider.add_token(token)

    def get_notification_by_id(self, ident):
        try:
            return Notification.query.filter(Notification.uuid == ident).one()
        except NoResultFound:
            return None

    def get_active_notifications(self):
        now = datetime.now()
        return Notification.query.filter(Notification.timestamp <= now).filter(Notification.expires >= now)

    def get_all_notifications(self):
        return Notification.query.all()

    def add_notification(self, notification):
        return self._db_persist(notification)

    def update_notification(self, notification):
        return self._db_merge(notification)

    def delete_notification(self, notification):
        self._db_delete(notification)

    def add_push(self, notification, message):
        # TODO should store the push as well?
        errors = []
        # Each provider can fail independently so collect all possible errors
        for provider in self.providers:
            try:
                provider.notify(message, notification)
            except Exception as err:
                msg = "%s: %s" % (provider.__class__.__name__, err.message)
                errors.append(msg)
        return errors

    def add_followup(self, notification, followup):
        assert notification in db.session
        notification.followups.append(followup)
        self._db_merge(notification)

    def get_followup_by_id(self, id):
        try:
            return FollowUp.query.filter(FollowUp.id == id).one()
        except NoResultFound:
            return None

    def update_followup(self, followup):
        return self._db_merge(followup)

    def delete_followup(self, followup):
        self._db_delete(followup)

    def _db_persist(self, obj):
        """Attach the object to the session
        and commit
        :param obj: object to persist
        :return obj object attached to the session
        """
        db.session.add(obj)
        db.session.commit()
        return obj

    def _db_merge(self, obj):
        """Attach the object to the session, reconcilies
        data with state in session.
        :param obj: object to attach to the session
        :return obj object attached to the session
        """
        val = db.session.merge(obj)
        db.session.commit()
        return val

    def _db_delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
