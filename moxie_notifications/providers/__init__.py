from moxie.core.kv import kv_store


class NotificationsProvider(object):
    provider_set = None

    def __init__(self, api_key):
        self.api_key = api_key

    def add_token(self, token):
        kv_store.sadd(self.provider_set, token)
        return True

    def handles(self, platform):
        return False
