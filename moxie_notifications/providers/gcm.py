from moxie_notifications.providers import NotificationsProvider
from moxie_notifications.services import ANDROID


class GCMProvider(NotificationsProvider):
    provider_set = 'gcm-registration-ids'

    def handles(self, platform):
        if platform is ANDROID:
            return True
        else:
            return False
