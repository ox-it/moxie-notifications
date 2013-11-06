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

    def persist_alert(self, alert):
        db.session.add(alert)
        db.session.commit()
        return alert

    def delete_alert(self, alert):
        db.session.delete(alert)
        db.session.commit()

    def add_push(self, alert, message):
        for provider in self.providers:
            provider.notify(message, alert)

    def add_followup(self, alert_ident, payload):
        pass

    def update_followup(self, ident):
        pass

    def delete_followup(self, ident):
        pass
