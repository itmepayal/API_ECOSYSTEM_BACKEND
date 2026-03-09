# =============================================================
# Third Party
# =============================================================
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# =============================================================
# Django
# =============================================================
from django.conf import settings

# =============================================================
# Logger
# =============================================================
import logging

logger = logging.getLogger(__name__)


# =============================================================
# SendGrid Email Sender
# =============================================================
def send_email(
    *,
    to_email: str,
    template_id: str,
    dynamic_data: dict,
    subject: str | None = None,
):

    try:

        mail = Mail(
            from_email=settings.EMAIL_FROM,
            to_emails=to_email,
        )

        if subject:
            mail.subject = subject

        mail.template_id = template_id
        mail.dynamic_template_data = dynamic_data

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

        response = sg.send(mail)

        if response.status_code not in (200, 202):
            logger.error(
                f"SendGrid failed | status={response.status_code} body={response.body}"
            )
        else:
            logger.info(
                f"SendGrid success | to={to_email} template={template_id}"
            )

        return response

    except Exception as e:
        logger.exception("SendGrid template email error")
        raise RuntimeError("Failed to send email via SendGrid") from e
    