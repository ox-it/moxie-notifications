from moxie.core.kv import kv_store


class NotificationsProvider(object):
    provider_set = None

    def remove_token(self, token):
        return kv_store.srem(self.provider_set, token)

    def add_token(self, token):
        return kv_store.sadd(self.provider_set, token)

    def handles(self, platform):
        return False


class DummyNotificationsProvider(NotificationsProvider):
    """Output all notifications t
    """

    provider_set = 'dummy'

    def handles(self, platform):
        # do not register any device with this provider
        return False

    def notify(self, message, notification):
        print message
