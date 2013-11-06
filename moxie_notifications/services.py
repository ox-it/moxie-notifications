import uuid
from flask.json import loads, dumps
from sqlalchemy.orm.exc import NoResultFound

from moxie.core.service import ProviderService
from moxie.core.kv import kv_store
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

    def update_alert(self, ident, alert):
        kv_store.set(self.KV_PREFIX + ident, dumps(alert))

    def delete_alert(self, ident):
        kv_store.delete(self.KV_PREFIX + ident)

    def add_alert(self, alert):
        """Add an alert
        :param alert: Alert domain object
        :return uuid of the alert
        """
        alert_uuid = uuid.uuid4()
        alert_uuid = str(alert_uuid)
        alert.uuid = alert_uuid
        db.session.add(alert)
        db.session.commit()
        return alert_uuid

    def add_push(self, alert, message):
        for provider in self.providers:
            provider.notify(message, alert)

    def add_followup(self, alert_ident, payload):
        pass

    def update_followup(self, ident):
        pass

    def delete_followup(self, ident):
        pass
