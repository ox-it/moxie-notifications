from sqlalchemy.orm.exc import NoResultFound

from moxie.core.service import ProviderService
from moxie.core.db import db

from .domain import Alert

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
        pass

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
        for provider in self.providers:
            provider.notify(message, alert)

    def add_followup(self, alert, followup):
        assert alert in db.session
        alert.followups.append(followup)
        self._db_merge(alert)

    def update_followup(self, followup):
        pass

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
        val = db.session.merge(obj)
        db.session.commit()
        return val

    def _db_delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
