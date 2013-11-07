import smtplib
import logging
from email.mime.text import MIMEText

from . import NotificationsProvider

logger = logging.getLogger(__file__)


class EmailNotificationsProvider(NotificationsProvider):

    def __init__(self, smtp_server, sender_email, send_to, email_subject='Push alert'):
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        self.send_to = send_to
        self.email_subject = email_subject

    def notify(self, message, alert):
        msg = self._get_email(message, alert)

        try:
            s = smtplib.SMTP(self.smtp_server)
            s.sendmail(self.sender_email, self.send_to, msg.as_string())
            s.quit()
        except:
            logger.error("Error when sending email", exc_info=True)
            return False
        else:
            return True

    def _get_email(self, message, alert):
        msg_text = self._get_email_text(message, alert)
        msg = MIMEText(msg_text)

        msg['Subject'] = self.email_subject
        msg['From'] = self.sender_email
        msg['To'] = ", ".join(self.send_to)
        return msg

    def _get_email_text(self, message, alert):
        """
        Prepare the text of the email message
        :param message: Message domain object
        :return: string with message
        """
        return """New push alert!

Message of the push alert: '{push}'

Alert ID: {alert_id}

Alert message: {alert_message}
        """.format(push=message,
                   alert_id=alert.uuid,
                   alert_message=alert.message)