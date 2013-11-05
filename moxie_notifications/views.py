from flask import request, jsonify
from flask.helpers import url_for
from moxie.core.exceptions import NotFound, BadRequest

from moxie.core.views import ServiceView, accepts
from moxie.core.representations import HAL_JSON, JSON
from moxie_notifications.representations import HALAlertRepresentation
from .services import NotificationsService
from .domain import Alert, PushAlert


class AlertView(ServiceView):

    methods = ['OPTIONS', 'POST']

    def handle_request(self):
        service = NotificationsService.from_context()
        message_json = request.get_json(force=True, silent=True, cache=True)
        alert = Alert.from_json(message_json)
        result = service.add_alert(alert)
        return result

    @accepts(JSON, HAL_JSON)
    def as_json(self, ident):
        if ident:
            response = jsonify({'status': 'created'})
            response.headers.add('Location', url_for('notifications.alert_details', ident=ident))
            response.status_code = 201
            return response
        else:
            return jsonify({'status': 'error'}), 500


class PushView(ServiceView):

    methods = ['OPTIONS', 'POST']

    def handle_request(self):
        service = NotificationsService.from_context()
        message_json = request.get_json(force=True, silent=True, cache=True)
        push = PushAlert.from_json(message_json)
        result = service.add_push(push)
        return result

    @accepts(JSON, HAL_JSON)
    def as_json(self, response):
        if response:
            if type(response) is tuple:
                return response
            else:
                return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'error'}), 500


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
            return alert
        elif request.method == "POST":
            alert = service.update_alert(ident, request.get_json(force=True, silent=True))
            return alert
        elif request.method == "DELETE":
            service.delete_alert(ident)
            return (jsonify({'status': 'deleted'}), 200)
        else:
            raise BadRequest("Method not suitable (allowed: {methods})".format(methods=','.join(self.METHODS)))

    @accepts(JSON, HAL_JSON)
    def as_json(self, response):
        if type(response) is tuple:
            return response
        else:
            return HALAlertRepresentation(response, request.url_rule.endpoint)


class FollowUpDetailsView(ServiceView):

    methods = ['OPTIONS', 'GET']