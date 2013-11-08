import logging

from gcmclient import GCM, JSONMessage, GCMAuthenticationError

from moxie.core.kv import kv_store
from moxie_notifications.providers import NotificationsProvider
from moxie_notifications.services import ANDROID
from moxie_notifications.tasks import retry_gcm

logger = logging.getLogger(__name__)


class GCMProvider(NotificationsProvider):
    provider_set = 'gcm-registration-ids'

    def __init__(self, api_key, url=None):
        if url:
            self._gcm = GCM(api_key, url=url)
        else:
            self._gcm = GCM(api_key)

    def handles(self, platform):
        if platform is ANDROID:
            return True
        else:
            return False

    def _get_all_registration_ids(self):
        return kv_store.smembers(self.provider_set)

    def _update_with_result(self, result):
        # Sent notification but we need to update our DB
        for reg_id, new_reg_id in result.canonical.items():
            logger.info("GCM updated registration id. Old: %s New: %s" % (
                reg_id, new_reg_id))
            kv_store.srem(self.provider_set, reg_id)
            kv_store.sadd(self.provider_set, new_reg_id)

        # likely uninstalled app
        for reg_id in result.not_registered:
            logger.info("GCM user uninstalled - %s" % (reg_id))
            kv_store.srem(self.provider_set, reg_id)

        # Failed for other reasons
        for reg_id, err_code in result.failed.items():
            logger.warning("GCM Error %s - Registration ID %s" % (err_code,
                reg_id))
            kv_store.srem(self.provider_set, reg_id)

    def notify(self, message, alert, registration_ids=[], all_devices=True,
            retry_count=0):
        if all_devices:
            registration_ids = self._get_all_registration_ids()

        # Return if we don't have any registration_ids to push to
        if not registration_ids:
            logger.warning("GCM: No registration_ids to push to")
            return False

        # Build basic message
        json_message = JSONMessage(registration_ids,
                data={
                    "message": message
                })
        try:
            result = self._gcm.send(json_message)
        except GCMAuthenticationError:
            logger.exception("GCMAuthenticationError: Incorrect API Key?")
        except ValueError as e:
            logger.exception("Invalid message or response %s" % e.args[0])
        else:
            self._update_with_result(result)
            if result.needs_retry():
                # Place task on queue to retry later
                retry_count = retry_count + 1
                delay = result.delay(retry=retry_count)
                retry_message = result.retry()
                logger.info("Queuing %s devices for retry in %s seconds."
                        % (len(retry_message.registration_ids), delay))
                retry_gcm.apply_async(
                    (message, retry_message.registration_ids),
                    {'retry_count': retry_count},
                    countdown=delay)
