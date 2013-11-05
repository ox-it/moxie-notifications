from flask import jsonify
from flask.helpers import url_for

from moxie.core.representations import HALRepresentation


class HALAlertRepresentation(object):

    def __init__(self, alert, endpoint):
        self.alert = alert
        self.endpoint = endpoint

    def as_json(self):
        return jsonify(self.as_dict())

    def as_dict(self):
        representation = HALRepresentation(self.alert)
        representation.add_link('self', url_for(self.endpoint, ident=self.alert.get('ident')))
        return representation.as_dict()
