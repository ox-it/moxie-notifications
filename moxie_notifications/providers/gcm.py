from moxie_notifications.providers import NotificationsProvider
from moxie_notifications.services import ANDROID


class GCMProvider(NotificationsProvider):
    provider_set = 'gcm-registration-ids'

    def __init__(self, api_key, url=None):
        self.api_key = api_key
        self.url = url

    def handles(self, platform):
        if platform is ANDROID:
            return True
        else:
            return False
