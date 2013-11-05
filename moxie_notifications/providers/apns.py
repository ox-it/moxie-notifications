from moxie_notifications.providers import NotificationsProvider
from moxie_notifications.services import iOS


class APNSProvider(NotificationsProvider):
    provider_set = 'apns-device-tokens'

    def __init__(self, address, cert_file, key_file=None, passphrase=None):
        self.address = address
        self.cert_file = cert_file
        self.key_file = key_file
        self.passphrase = passphrase

    def handles(self, platform):
        if platform is iOS:
            return True
        else:
            return False
