from moxie.core.service import Service
from moxie.core.kv import kv_store


class NotificationsService(Service):

    def get_alert_by_id(self, ident):
        pass

    def get_active_alerts(self):
        pass

    def get_all_alerts(self):
        return kv_store.get('notifications')

    def update_alert(self, ident, payload):
        pass

    def delete_alert(self, ident):
        pass

    def add_alert(self, ident):
        pass

    def add_push(self, push_alert):
        pass

    def add_followup(self, alert_ident, payload):
        pass

    def update_followup(self, ident):
        pass

    def delete_followup(self, ident):
        pass