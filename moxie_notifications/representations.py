from flask import jsonify
from flask.helpers import url_for

from moxie.core.representations import Representation, HALRepresentation


class AlertRepresentation(Representation):

    def __init__(self, alert):
        self.alert = alert

    def as_json(self):
        return jsonify(self.as_dict())

    def as_dict(self):
        return {
            'message': self.alert.message
        }


class HALAlertRepresentation(AlertRepresentation):

    def __init__(self, alert, ident, endpoint):
        super(HALAlertRepresentation, self).__init__(alert)
        self.endpoint = endpoint
        self.ident = ident

    def as_json(self):
        return jsonify(self.as_dict())

    def as_dict(self):
        base = super(HALAlertRepresentation, self).as_dict()
        representation = HALRepresentation(base)
        representation.add_link('self', url_for(self.endpoint, ident=self.ident))
        return representation.as_dict()
