from datetime import datetime
from flask import request, jsonify
from flask.helpers import url_for
from moxie.core.exceptions import NotFound, BadRequest

from moxie.core.views import ServiceView, accepts
from moxie.core.representations import HAL_JSON, JSON
from moxie_notifications.domain import FollowUp
from moxie_notifications.representations import HALFollowUpRepresentation
from .representations import HALAlertRepresentation, HALAlertsRepresentation
from .services import NotificationsService, ANDROID, iOS
from .domain import Alert


class AlertView(ServiceView):

    methods = ['OPTIONS', 'POST']

    def handle_request(self):
        service = NotificationsService.from_context()
        message_json = request.get_json(force=True, silent=True, cache=True)
        if not _validate_alert_json(message_json):
            raise BadRequest("You must pass a JSON document with property 'message'")
        alert = Alert(message_json['message'])
        if 'fromDate' in message_json:
            alert.from_date = _str_to_datetime(message_json['fromDate'])
        if 'displayUntil' in message_json:
            alert.display_until = _str_to_datetime(message_json['displayUntil'])
        result = service.add_alert(alert)
        return result

    @accepts(JSON, HAL_JSON)
    def as_json(self, alert):
        if alert:
            response = jsonify({'status': 'created'})
            response.headers.add('Location', url_for('notifications.alert_details', ident=alert.uuid))
            response.status_code = 201
            return response
        else:
            response = jsonify({'status': 'error'})
            response.status_code = 500
            return response


class PushView(ServiceView):

    methods = ['OPTIONS', 'POST']

    MESSAGE_MIN_LENGTH = 3
    MESSAGE_MAX_LENGTH = 250

    def handle_request(self):
        service = NotificationsService.from_context()
        message_json = request.get_json(force=True, silent=True, cache=True)

        if not message_json or 'alert' not in message_json or 'message' not in message_json:
            raise BadRequest("You must pass a JSON document with properties 'alert' and 'message'")

        message = message_json['message'].strip()
        message_len = len(message)
        if not self.MESSAGE_MIN_LENGTH <= message_len <= self.MESSAGE_MAX_LENGTH:
            raise BadRequest("'message' must be between {min} and {max} characters".format(min=self.MESSAGE_MIN_LENGTH,
                                                                                           max=self.MESSAGE_MAX_LENGTH))

        alert = service.get_alert_by_id(message_json['alert'])
        if not alert:
            raise BadRequest("Alert '{uuid}' not found".format(uuid=message_json['alert']))

        try:
            service.add_push(alert, message)
            return 'success'
        except Exception as err:
            return err.message

    @accepts(JSON, HAL_JSON)
    def as_json(self, result):
        if result and result == 'success':
            response = jsonify({'status': 'success'})
            response.status_code = 202      # Accepted
        else:
            response = jsonify({'status': result})
            response.status_code = 500
        return response


class AlertsView(ServiceView):

    methods = ['OPTIONS', 'GET']

    def handle_request(self):
        history = request.args.get("history", False)
        service = NotificationsService.from_context()
        if history in ('true', 'True', 't', '1'):
            return service.get_all_alerts()
        else:
            return service.get_active_alerts()

    @accepts(JSON, HAL_JSON)
    def as_json(self, alerts):
        return HALAlertsRepresentation(alerts, request.url_rule.endpoint).as_json()


class AlertDetailsView(ServiceView):

    methods = ['GET', 'POST', 'DELETE']

    def handle_request(self, ident):
        service = NotificationsService.from_context()
        alert = service.get_alert_by_id(ident)
        if not alert:
            raise NotFound()
        if request.method == "GET":
            return alert
        elif request.method == "POST":
            message_json = request.get_json(force=True, silent=True)
            if not _validate_alert_json(message_json):
                raise BadRequest("You must pass a JSON document with property 'message'")
            alert.message = message_json['message']
            if 'fromDate' in message_json:
                alert.from_date = _str_to_datetime(message_json['fromDate'])
            if 'displayUntil' in message_json:
                alert.display_until = _str_to_datetime(message_json['displayUntil'])
            alert = service.update_alert(alert)
            return alert
        elif request.method == "DELETE":
            service.delete_alert(alert)
            return "deleted"
        else:
            raise BadRequest("Method not suitable (allowed: {methods})".format(methods=','.join(self.METHODS)))

    @accepts(JSON, HAL_JSON)
    def as_json(self, result):
        if result == "deleted":
            return jsonify({'status': 'deleted'})
        else:
            return HALAlertRepresentation(result, request.url_rule.endpoint).as_json()


class AlertAddFollowUpView(ServiceView):

    methods = ['OPTIONS', 'POST']

    def handle_request(self, ident):
        service = NotificationsService.from_context()
        alert = service.get_alert_by_id(ident)
        if not alert:
            raise NotFound("Alert not found")
        message_json = request.get_json(force=True, silent=True)
        if not _validate_followup_json(message_json):
            raise BadRequest("You must pass a JSON document with property 'message'")
        fu = FollowUp(message_json['message'])
        service.add_followup(alert, fu)
        return True

    @accepts(JSON, HAL_JSON)
    def as_json(self, response):
        return jsonify({'status': 'created'})


class FollowUpDetailsView(ServiceView):

    methods = ['OPTIONS', 'GET', 'POST', 'DELETE']

    def handle_request(self, ident, id):
        self.service = NotificationsService.from_context()
        self.alert = self.service.get_alert_by_id(ident)
        if self.alert:
            self.followup = self.service.get_followup_by_id(id)
            if not self.followup:
                raise NotFound("FollowUp not found")
        else:
            raise NotFound("Alert not found")

        if request.method == "GET":
            return self._handle_GET()
        elif request.method == "POST":
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
            return HALFollowUpRepresentation(response, self.alert, request.url_rule.endpoint).as_json()


class Register(ServiceView):
    methods = ['POST', 'OPTIONS']

    platform = None
    post_data_key = None

    def handle_request(self):
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


def _validate_alert_json(obj):
    if not obj or 'message' not in obj:
        return False
    return True


def _validate_followup_json(obj):
    if not obj or 'message' not in obj:
        return False
    return True


def _str_to_datetime(obj):
    return datetime.strptime(obj, "%Y-%m-%dT%H:%M:%S")