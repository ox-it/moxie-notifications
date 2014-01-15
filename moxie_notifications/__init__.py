from flask import Blueprint

from .views import (PushView, NotificationsView, NotificationDetailsView, RegisterGCM,
                    RegisterAPNS, NotificationAddFollowUpView, FollowUpDetailsView)


def create_blueprint(blueprint_name, conf):
    notifications_blueprint = Blueprint(blueprint_name, __name__, **conf)

    notifications_blueprint.add_url_rule('/', view_func=NotificationsView.as_view('notifications'))

    notifications_blueprint.add_url_rule('/push', view_func=PushView.as_view('push'))

    notifications_blueprint.add_url_rule('/<ident>', view_func=NotificationDetailsView.as_view('notification_details'))

    notifications_blueprint.add_url_rule('/<ident>/followup/<id>',
                                         view_func=FollowUpDetailsView.as_view('followp_details'))

    notifications_blueprint.add_url_rule('/<ident>/followup',
                                         view_func=NotificationAddFollowUpView.as_view('notification_add_followup'))

    notifications_blueprint.add_url_rule('/register/gcm', view_func=RegisterGCM.as_view('register-gcm'))

    notifications_blueprint.add_url_rule('/register/apns', view_func=RegisterAPNS.as_view('register-apns'))

    return notifications_blueprint
