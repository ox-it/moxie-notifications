import smtplib
import logging
from email.mime.text import MIMEText

from . import NotificationsProvider

logger = logging.getLogger(__file__)


class EmailNotificationsProvider(NotificationsProvider):

    def __init__(self, smtp_server, sender_email, send_to, email_subject='Push notification'):
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        self.send_to = send_to
        self.email_subject = email_subject

    def notify(self, message, notification):
        msg = self._get_email(message, notification)

        try:
            s = smtplib.SMTP(self.smtp_server)
            s.sendmail(self.sender_email, self.send_to, msg.as_string())
            s.quit()
        except:
            logger.error("Error when sending email", exc_info=True)
            return False
        else:
            return True

    def _get_email(self, message, notification):
        msg_text = self._get_email_text(message, notification)
        msg = MIMEText(msg_text)

        msg['Subject'] = self.email_subject
        msg['From'] = self.sender_email
        msg['To'] = ", ".join(self.send_to)
        return msg

    def _get_email_text(self, message, notification):
        """
        Prepare the text of the email message
        :param message: Message domain object
        :return: string with message
        """
        return """New push notification!

Message of the push notification: '{push}'

Notification ID: {notification_id}

Notification message: {notification_message}
        """.format(push=message,
                   notification_id=notification.uuid,
                   notification_message=notification.message)