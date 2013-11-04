from flask import Blueprint, request
from flask.helpers import make_response

from moxie.core.representations import HALRepresentation


def create_blueprint(blueprint_name, conf):
    notifications_blueprint = Blueprint(blueprint_name, __name__, **conf)

    notifications_blueprint.add_url_rule('/', view_func=get_routes)

    return notifications_blueprint


def get_routes():
    path = request.path
    representation = HALRepresentation({})
    representation.add_curie('hl', 'http://moxie.readthedocs.org/en/latest/http_api/notifications.html#{rel}')
    representation.add_link('self', '{bp}'.format(bp=path))
    response = make_response(representation.as_json(), 200)
    response.headers['Content-Type'] = "application/json"
    return response
