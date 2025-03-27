from django.core.mail import EmailMessage
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Task

previous_values = {}


@receiver(post_save, sender=Task)
def post_save_handler(sender, instance: Task, created, **kwargs):
    assigned_to = None
    if created:
        if instance.assigned_to_id is not None:
            assigned_to = instance.assigned_to
    elif instance.assigned_to_id is not None and instance.assigned_to_id != previous_values[instance.id].assigned_to_id:
        assigned_to = instance.assigned_to_id

    if assigned_to is not None:
        # TODO: Use background task to send email
        email = EmailMessage(
            to=[instance.assigned_to.email],
            subject=f'Task Assigned #{instance.title}',
            body=render_to_string(
                'emails/task_assigned.html',
                context={
                    'task': instance
                }
            )
        )
        email.content_subtype = 'html'
        email.send()


@receiver(pre_save, sender=Task)
def pre_save_handler(sender, instance: Task, **kwargs):
    if instance.pk:
        previous_values[instance.id] = Task.objects.get(id=instance.id)
