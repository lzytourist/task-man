from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Task

@shared_task
def send_task_assigned_email(to: [str], task_id: int):
    task = Task.objects.get(id=task_id)
    email = EmailMessage(
        to=to,
        subject=f'Task Assigned #{task.id}: {task.title}',
        body=render_to_string(
            'emails/task_assigned.html',
            context={'task': task},
        )
    )
    email.content_subtype = 'html'
    email.send(fail_silently=False)
