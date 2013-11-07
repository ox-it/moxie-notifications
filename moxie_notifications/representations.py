from flask import jsonify
from flask.helpers import url_for

from moxie.core.representations import HALRepresentation


class HALFollowUpRepresentation(object):

    def __init__(self, fu, alert, endpoint):
        self.followup = fu
        self.alert = alert
        self.endpoint = endpoint

    def as_dict(self):
        representation = HALRepresentation(self.followup.as_dict())
        representation.add_link('self', url_for(self.endpoint,
                                                ident=self.alert.uuid,
                                                id=self.followup.id))
        return representation.as_dict()

    def as_json(self):
        return jsonify(self.as_dict())


class HALAlertRepresentation(object):

    def __init__(self, alert, endpoint):
        self.alert = alert
        self.endpoint = endpoint

    def as_json(self):
        return jsonify(self.as_dict())

    def as_dict(self):
        representation = HALRepresentation(self.alert.as_dict())
        followups = [HALFollowUpRepresentation(fu, self.alert, 'notifications.followp_details').as_dict() for fu in self.alert.followups]
        if followups:
            representation.add_embed('followups', followups)
        representation.add_link('self', url_for(self.endpoint, ident=self.alert.uuid))
        return representation.as_dict()


class HALAlertsRepresentation(object):

    def __init__(self, alerts, endpoint):
        """HAL representation of a list of alerts
        :param alerts: list of alerts
        :param endpoint: endpoint
        """
        self.alerts = alerts
        self.endpoint = endpoint

    def as_json(self):
        return jsonify(self.as_dict())

    def as_dict(self):
        representation = HALRepresentation({})
        halified = []
        for alert in self.alerts:
            halified.append(HALAlertRepresentation(alert, 'notifications.alert_details').as_dict())
        representation.add_embed('alerts', halified)
        representation.add_link('self', url_for(self.endpoint))
        return representation.as_dict()