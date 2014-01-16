from flask import jsonify
from flask.helpers import url_for

from moxie.core.representations import HALRepresentation


class HALFollowUpRepresentation(object):

    def __init__(self, fu, notification, endpoint):
        self.followup = fu
        self.notification = notification
        self.endpoint = endpoint

    def as_dict(self):
        representation = HALRepresentation(self.followup.as_dict())
        representation.add_link('self', url_for(self.endpoint,
                                                ident=self.notification.uuid,
                                                id=self.followup.id))
        return representation.as_dict()

    def as_json(self):
        return jsonify(self.as_dict())


class HALNotificationRepresentation(object):

    def __init__(self, notification, endpoint):
        self.notification = notification
        self.endpoint = endpoint

    def as_json(self):
        return jsonify(self.as_dict())

    def as_dict(self):
        representation = HALRepresentation(self.notification.as_dict())
        followups = [HALFollowUpRepresentation(fu, self.notification, 'notifications.followp_details').as_dict()
                     for fu in self.notification.followups]
        if followups:
            representation.add_embed('followups', followups)
        representation.add_link('self', url_for(self.endpoint, ident=self.notification.uuid))
        return representation.as_dict()


class HALNotificationsRepresentation(object):

    def __init__(self, notifications, endpoint):
        """HAL representation of a list of notifications
        :param notifications: list of notifications
        :param endpoint: endpoint
        """
        self.notifications = notifications
        self.endpoint = endpoint

    def as_json(self):
        return jsonify(self.as_dict())

    def as_dict(self):
        representation = HALRepresentation({})
        halified = []
        for notification in self.notifications:
            halified.append(HALNotificationRepresentation(notification, 'notifications.notification_details').as_dict())
        representation.add_embed('notifications', halified)
        representation.add_link('self', url_for(self.endpoint))
        return representation.as_dict()