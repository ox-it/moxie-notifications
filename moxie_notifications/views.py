from flask import request, jsonify
from flask.helpers import url_for
from moxie.core.exceptions import NotFound, BadRequest

from moxie.core.views import ServiceView, accepts
from moxie.core.representations import HAL_JSON, JSON
from moxie_notifications.representations import HALAlertRepresentation
from .services import NotificationsService


class AlertView(ServiceView):

    methods = ['OPTIONS', 'POST']

    def handle_request(self):
        service = NotificationsService.from_context()
        message_json = request.get_json(force=True, silent=True, cache=True)
        if not message_json or 'message' not in message_json:
            raise BadRequest("You must pass a JSON document with property 'message'")
        result = service.add_alert(message_json)
        return result

    @accepts(JSON, HAL_JSON)
    def as_json(self, ident):
        if ident:
            response = jsonify({'status': 'created'})
            response.headers.add('Location', url_for('notifications.alert_details', ident=ident))
            response.status_code = 201
            return response
        else:
            response = jsonify({'status': 'error'})
            response.status_code = 500
            return response


class PushView(ServiceView):

    methods = ['OPTIONS', 'POST']

    def handle_request(self):
        service = NotificationsService.from_context()
        message_json = request.get_json(force=True, silent=True, cache=True)
        if not message_json or 'alert' not in message_json or 'message' not in message_json:
            raise BadRequest("You must pass a JSON document with properties 'alert' and 'message'")
        result = service.add_push(message_json)
        return result

    @accepts(JSON, HAL_JSON)
    def as_json(self, result):
        if result:
            return jsonify({'status': 'success'})
        else:
            response = jsonify({'status': 'error'})
            response.status_code = 500
            return response


class AlertsView(ServiceView):

    methods = ['OPTIONS', 'GET']

    def handle_request(self):
        service = NotificationsService.from_context()
        return service.get_active_alerts()

    @accepts(JSON, HAL_JSON)
    def as_json(self, response):
        pass


class AlertDetailsView(ServiceView):

    methods = ['GET', 'POST', 'DELETE']

    def handle_request(self, ident):
        service = NotificationsService.from_context()
        alert = service.get_alert_by_id(ident)
        if not alert:
            raise NotFound()
        if request.method == "GET":
            alert['ident'] = ident
            return alert
        elif request.method == "POST":
            message_json = request.get_json(force=True, silent=True)
            alert = service.update_alert(ident, message_json)
            message_json['ident'] = ident
            return message_json
        elif request.method == "DELETE":
            service.delete_alert(ident)
            return "deleted"
        else:
            raise BadRequest("Method not suitable (allowed: {methods})".format(methods=','.join(self.METHODS)))

    @accepts(JSON, HAL_JSON)
    def as_json(self, result):
        if type(result) is str and result == "deleted":
            return jsonify({'status': 'deleted'})
        else:
            return HALAlertRepresentation(result, request.url_rule.endpoint).as_json()


class FollowUpDetailsView(ServiceView):

    methods = ['OPTIONS', 'GET']