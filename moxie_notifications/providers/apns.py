from moxie_notifications.providers import NotificationsProvider
from moxie_notifications.services import iOS


class APNSProvider(NotificationsProvider):
    provider_set = 'apns-device-tokens'

    def handles(self, platform):
        if platform is iOS:
            return True
        else:
            return False
