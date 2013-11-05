from flask import Blueprint, request
from flask.helpers import make_response

from moxie.core.representations import HALRepresentation

from .views import (AlertView, PushView, AlertsView, AlertDetailsView,
        RegisterGCM, RegisterAPNS)


def create_blueprint(blueprint_name, conf):
    notifications_blueprint = Blueprint(blueprint_name, __name__, **conf)

    notifications_blueprint.add_url_rule('/', view_func=get_routes)

    notifications_blueprint.add_url_rule('/alert', view_func=AlertView.as_view('alert'))

    notifications_blueprint.add_url_rule('/push', view_func=PushView.as_view('push'))

    notifications_blueprint.add_url_rule('/alert/<ident>', view_func=AlertDetailsView.as_view('alert_details'))

    notifications_blueprint.add_url_rule('/alerts', view_func=AlertsView.as_view('alerts'))

    notifications_blueprint.add_url_rule('/register/gcm', view_func=RegisterGCM.as_view('register-gcm'))

    notifications_blueprint.add_url_rule('/register/apns', view_func=RegisterAPNS.as_view('register-apns'))

    return notifications_blueprint


def get_routes():
    path = request.path
    representation = HALRepresentation({})
    representation.add_curie('hl', 'http://moxie.readthedocs.org/en/latest/http_api/notifications.html#{rel}')
    representation.add_link('self', '{bp}'.format(bp=path))
    response = make_response(representation.as_json(), 200)
    response.headers['Content-Type'] = "application/json"
    return response
