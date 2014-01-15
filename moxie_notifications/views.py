from datetime import datetime
import logging

from flask import request, jsonify
from flask.helpers import url_for
from moxie.core.exceptions import NotFound, BadRequest
from moxie.core.views import accepts, ServiceView
from moxie.core.representations import HAL_JSON, JSON
from moxie.authentication import HMACView

from moxie_notifications.domain import FollowUp, Notification
from moxie_notifications.services import NotificationsService, ANDROID, iOS
from moxie_notifications.representations import (HALFollowUpRepresentation, HALNotificationRepresentation,
                                                 HALNotificationsRepresentation)


logger = logging.getLogger(__name__)


class AuthenticatedView(HMACView):

    def handle_request(self):
        service = NotificationsService.from_context()
        try:
            api_key = request.headers['x-moxie-key']
            secret = service.get_secret(api_key)
        except KeyError:
            raise NotFound()
        self.check_auth(secret)


class PushView(AuthenticatedView):

    methods = ['OPTIONS', 'POST']

    MESSAGE_MIN_LENGTH = 3
    MESSAGE_MAX_LENGTH = 250

    def handle_request(self):
        super(PushView, self).handle_request()
        service = NotificationsService.from_context()
        message_json = request.get_json(force=True, silent=True, cache=True)

        if not message_json or 'notification' not in message_json or 'message' not in message_json:
            raise BadRequest("You must pass a JSON document with properties 'notification' and 'message'")

        message = message_json['message'].strip()
        message_len = len(message)
        if not self.MESSAGE_MIN_LENGTH <= message_len <= self.MESSAGE_MAX_LENGTH:
            raise BadRequest("'message' must be between {min} and {max} characters".format(min=self.MESSAGE_MIN_LENGTH,
                                                                                           max=self.MESSAGE_MAX_LENGTH))

        notification = service.get_notification_by_id(message_json['notification'])
        if not notification:
            raise BadRequest("Notification '{uuid}' not found".format(uuid=message_json['notification']))

        errors = service.add_push(notification, message)
        if errors:
            logging.error("Error pushing to all providers: %s" % errors)
            return errors
        else:
            return 'success'

    @accepts(JSON, HAL_JSON)
    def as_json(self, result):
        if result and result == 'success':
            response = jsonify({'status': 'success'})
            response.status_code = 202      # Accepted
        else:
            response = jsonify({'status': 'error', 'errors': result})
            response.status_code = 500
        return response


class NotificationsView(AuthenticatedView):

    methods = ['OPTIONS', 'GET', 'POST']

    def handle_request(self):
        if request.method == 'GET':
            return self._handle_GET()
        elif request.method == 'POST':
            super(NotificationsView, self).handle_request()
            return self._handle_POST()

    def _handle_GET(self):
        history = request.args.get("history", False)
        service = NotificationsService.from_context()
        if history in ('true', 'True', 't', '1'):
            return 'notifications', service.get_all_notifications()
        else:
            return 'notifications', service.get_active_notifications()

    def _handle_POST(self):
        service = NotificationsService.from_context()
        message_json = request.get_json(force=True, silent=True, cache=True)
        if not _validate_notification_json(message_json):
            raise BadRequest("You must pass a JSON document with property 'message'")
        notification = Notification(message_json['message'])
        if 'timestamp' in message_json:
            notification.timestamp = _str_to_datetime(message_json['timestamp'])
        if 'expires' in message_json:
            notification.expires = _str_to_datetime(message_json['expires'])
        if 'url' in message_json:
            notification.url = message_json['url']
        result = service.add_notification(notification)
        return 'notification', result

    @accepts(JSON, HAL_JSON)
    def as_json(self, result):
        if result[0] == 'notifications':
            return HALNotificationsRepresentation(result[1], request.url_rule.endpoint).as_json()
        elif result[0] == 'notification':
            if result[1]:
                response = jsonify({'status': 'created'})
                response.headers.add('Location', url_for('notifications.notification_details', ident=result[1].uuid))
                response.status_code = 201
                return response
            else:
                response = jsonify({'status': 'error'})
                response.status_code = 500
                return response


class NotificationDetailsView(AuthenticatedView):

    methods = ['GET', 'POST', 'DELETE']

    def handle_request(self, ident):
        service = NotificationsService.from_context()
        notification = service.get_notification_by_id(ident)
        if not notification:
            raise NotFound()
        if request.method == "GET":
            return notification

        # POST and DELETE need to be authenticated
        super(NotificationDetailsView, self).handle_request()
        if request.method == "POST":
            message_json = request.get_json(force=True, silent=True)
            if not message_json:
                raise BadRequest("You must pass a JSON document with properties to be updated on the notification.")
            if 'message' in message_json:
                notification.message = message_json['message']
            if 'timestamp' in message_json:
                notification.timestamp = _str_to_datetime(message_json['timestamp'])
            if 'expires' in message_json:
                notification.expires = _str_to_datetime(message_json['expires'])
            if 'url' in message_json:
                notification.url = message_json['url']
            notification = service.update_notification(notification)
            return notification
        elif request.method == "DELETE":
            service.delete_notification(notification)
            return "deleted"
        else:
            raise BadRequest("Method not suitable (allowed: {methods})".format(methods=','.join(self.METHODS)))

    @accepts(JSON, HAL_JSON)
    def as_json(self, result):
        if result == "deleted":
            return jsonify({'status': 'deleted'})
        else:
            return HALNotificationRepresentation(result, request.url_rule.endpoint).as_json()


class NotificationAddFollowUpView(AuthenticatedView):

    methods = ['OPTIONS', 'POST']

    def handle_request(self, ident):
        super(NotificationAddFollowUpView, self).handle_request()
        service = NotificationsService.from_context()
        notification = service.get_notification_by_id(ident)
        if not notification:
            raise NotFound("Notification not found")
        message_json = request.get_json(force=True, silent=True)
        if not _validate_followup_json(message_json):
            raise BadRequest("You must pass a JSON document with property 'message'")
        fu = FollowUp(message_json['message'])
        service.add_followup(notification, fu)
        return True

    @accepts(JSON, HAL_JSON)
    def as_json(self, response):
        return jsonify({'status': 'created'})


class FollowUpDetailsView(AuthenticatedView):

    methods = ['OPTIONS', 'GET', 'POST', 'DELETE']

    def handle_request(self, ident, id):
        self.service = NotificationsService.from_context()
        self.notification = self.service.get_notification_by_id(ident)
        if self.notification:
            self.followup = self.service.get_followup_by_id(id)
            if not self.followup:
                raise NotFound("FollowUp not found")
        else:
            raise NotFound("Notification not found")

        if request.method == "GET":
            return self._handle_GET()

        # POST and DELETE need to be authenticated
        super(FollowUpDetailsView, self).handle_request()
        if request.method == "POST":
            return self._handle_POST()
        elif request.method == "DELETE":
            return self._handle_DELETE()
        else:
            raise BadRequest("Method {method} not valid".format(method=request.method))

    def _handle_GET(self):
        return self.followup

    def _handle_POST(self):
        message_json = request.get_json(force=True, silent=True)
        if not _validate_followup_json(message_json):
            raise BadRequest("You must pass a JSON document with property 'message'")
        self.followup.message = message_json['message']
        self.service.update_followup(self.followup)
        return self.followup

    def _handle_DELETE(self):
        self.service.delete_followup(self.followup)
        return 'deleted'

    @accepts(JSON, HAL_JSON)
    def as_json(self, response):
        if response == "deleted":
            return jsonify({'status': 'deleted'})
        else:
            return HALFollowUpRepresentation(response, self.notification, request.url_rule.endpoint).as_json()


class Register(ServiceView):
    methods = ['POST', 'OPTIONS']

    platform = None
    post_data_key = None

    def handle_request(self):
        super(Register, self).handle_request()
        notification_service = NotificationsService.from_context()
        data = request.get_json(force=True, silent=True)
        # Handle missing/invalid JSON
        if data is None:
            response = jsonify(error="Expected JSON in POST data")
            response.status_code = 400
            return response
        try:
            token = data[self.post_data_key]
        except KeyError:
            response = jsonify(error="Expected key: %s" % self.post_data_key)
            response.status_code = 400
            return response
        success = notification_service.register(token, self.platform)
        response = jsonify(success=success)
        if success:
            # Accepted
            response.status_code = 202
        else:
            response.status_code = 500
        return response

    @accepts(HAL_JSON, JSON)
    def as_hal_json(self, response):
        return response


class RegisterGCM(Register):
    platform = ANDROID
    post_data_key = 'registration_id'


class RegisterAPNS(Register):
    platform = iOS
    post_data_key = 'device_token'


def _validate_notification_json(obj):
    if not obj or 'message' not in obj:
        return False
    return True


def _validate_followup_json(obj):
    if not obj or 'message' not in obj:
        return False
    return True


def _str_to_datetime(obj):
    try:
        return datetime.strptime(obj, "%Y-%m-%dT%H:%M:%S")
    except ValueError as e:
        raise BadRequest("Wrong date value: {msg}".format(msg=e.message))
