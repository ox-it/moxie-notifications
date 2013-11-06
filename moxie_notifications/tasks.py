import logging

from moxie import create_app
from moxie.worker import celery

from .services import NotificationsService, ANDROID

logger = logging.getLogger(__name__)
BLUEPRINT_NAME = 'notifications'


@celery.task
def retry_gcm(message, registration_ids, retry=0):
    app = create_app()
    with app.blueprint_context(BLUEPRINT_NAME):
        notifications_service = NotificationsService.from_context()
        gcm = notifications_service.get_provider(ANDROID)
        gcm.notify(message, None, registration_ids=registration_ids)
