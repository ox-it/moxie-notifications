from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

from moxie.core.service import ProviderService
from moxie.core.db import db

from .domain import Alert
from moxie_notifications.domain import FollowUp

ANDROID = 'android'
iOS = 'iOS'


class NotificationsService(ProviderService):
    KV_PREFIX = 'notification_'

    def register(self, token, platform):
        provider = self.get_provider(platform)
        return provider.add_token(token)

    def get_alert_by_id(self, ident):
        try:
            return Alert.query.filter(Alert.uuid == ident).one()
        except NoResultFound:
            return None

    def get_active_alerts(self):
        now = datetime.now()
        return Alert.query.filter(Alert.from_date <= now).filter(Alert.display_until >= now)

    def get_all_alerts(self):
        return Alert.query.all()

    def add_alert(self, alert):
        return self._db_persist(alert)

    def update_alert(self, alert):
        return self._db_merge(alert)

    def delete_alert(self, alert):
        self._db_delete(alert)

    def add_push(self, alert, message):
        # TODO should store the push as well?
        errors = []
        # Each provider can fail independently so collect all possible errors
        for provider in self.providers:
            try:
                provider.notify(message, alert)
            except Exception as err:
                msg = "%s: %s" % (provider.__class__.__name__, err.message)
                errors.append(msg)
        return errors

    def add_followup(self, alert, followup):
        assert alert in db.session
        alert.followups.append(followup)
        self._db_merge(alert)

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
