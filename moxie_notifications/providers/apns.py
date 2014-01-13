import logging

from datetime import timedelta
from apnsclient import Session, APNs, Message

from moxie.core.kv import kv_store
from moxie_notifications.providers import NotificationsProvider
from moxie_notifications.services import iOS

logger = logging.getLogger(__name__)

DEFAULT_EXPIRY = timedelta(hours=2)


class APNSProvider(NotificationsProvider):
    provider_set = 'apns-device-tokens'

    def __init__(self, cert_file, push_address="push_production",
                 feedback_address="feedback_production"):
        self.cert_file = cert_file
        self.push_address = push_address
        self.feedback_address = feedback_address

        self.session = None

    def _feedback_connection(self):
        return Session.new_connection(self.feedback_address,
                                      cert_file=self.cert_file)

    def feedback_server(self, timeout=10):
        con = self._feedback_connection()
        return APNs(con, tail_timeout=timeout)

    def _push_connection(self):
        if not self.session:
            self.session = Session()
        return self.session.get_connection(self.push_address,
                                           cert_file=self.cert_file)

    def push_server(self, timeout=0.5):
        con = self._push_connection()
        return APNs(con, tail_timeout=timeout)

    def handles(self, platform):
        if platform is iOS:
            return True
        else:
            return False

    def _get_all_device_tokens(self):
        return kv_store.smembers(self.provider_set)

    def notify(self, message, alert, device_tokens=None, all_devices=True,
               expiry=DEFAULT_EXPIRY):
        """Send a push notification through APNs, this can be to specific
        devices or all devices we have stored in ``self.provider_set``

        APNs queues push notifications as devices become available unlike GCM
        This means you attach an expiry on each push notification. So if a push
        notification becomes irrelevant it has can be considered expired.
        """
        if all_devices:
            device_tokens = self._get_all_device_tokens()

        logger.info("APNS: Push notification to {0} clients. Message: {1}"
                    .format(len(device_tokens), message))

        # Return if there are no device tokens to push to
        if not device_tokens:
            logger.warning("APNs: No device_tokens to push to")
            return False
        message = Message(device_tokens, alert=message, expiry=expiry)

        server = self.push_server()
        result = server.send(message)
        # Check failures. Check codes in APNs reference docs.
        for token, reason in result.failed.items():
            code, errmsg = reason
            logger.warning("APNs: Device failed: {0}, reason: {1}".format(
                token, errmsg))
        # Check failures not related to devices.
        for code, errmsg in result.errors:
            logger.warning("APNs: Error: {0}".format(errmsg))

    def feedback(self):
        """Feedback is a process through which APNs notifies you of clients
        becoming unavailable to receiving push notifications. Most likely this
        means they have uninstalled the app.
        """
        server = self.feedback_server()
        for token, since in server.feedback():
            kv_store.srem(self.provider_set, token)
            logger.info("APNs: Token {0} is unavailable since {1}".format(
                token, since))
