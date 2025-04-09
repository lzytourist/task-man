from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_user_email(to, subject, message):
    email = EmailMessage(
        to=to,
        subject=subject,
        body=message,
    )
    email.send(fail_silently=False)
