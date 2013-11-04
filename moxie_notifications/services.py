import uuid
from flask.json import loads, dumps

from moxie.core.service import ProviderService
from moxie.core.kv import kv_store

ANDROID = 'android'
iOS = 'iOS'


class NotificationsService(ProviderService):
    KV_PREFIX = 'notification_'

    def register(self, token, platform):
        provider = self.get_provider(platform)
        return provider.add_token(token)

    def get_alert_by_id(self, ident):
        json = kv_store.get(self.KV_PREFIX + ident)
        if json:
            return loads(json)
        else:
            return None

    def get_active_alerts(self):
        pass

    def get_all_alerts(self):
        return kv_store.get('notifications')

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
        self.update_alert(alert_uuid, alert)
        return alert_uuid

    def add_push(self, push_alert):
        pass

    def add_followup(self, alert_ident, payload):
        pass

    def update_followup(self, ident):
        pass

    def delete_followup(self, ident):
        pass
