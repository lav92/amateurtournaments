import asyncio
import smtplib
from email.message import EmailMessage

from app.config import settings

from app.tasks.celery_config import celery_app
from app.stats.services import get_match_stats


def create_email(
        subject,
        message,
        email_to
):
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = 'tournaments'
    email['To'] = email_to
    email.set_content(message)
    return email


@celery_app.task
def get_stats(user_id: int, match_id: str, steam_id: int, user_email: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_match_stats(user_id, match_id, steam_id))
    message = f'Report of match {match_id} succeeded. You can view details in your profile in our site'
    msg_content = create_email(subject='Match report', message=message, email_to=user_email)
    with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465) as server:
        server.login(user=settings.SMPT_LOGIN, password=settings.SMTP_PASSWORD)
        server.send_message(msg_content)
