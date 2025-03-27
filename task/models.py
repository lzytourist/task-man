from django.db import models

from account.models import TimeStampedModel, User


class Task(TimeStampedModel):
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        CRITICAL = 'critical', 'Critical'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        IN_PROGRESS = 'in-progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(
        max_length=255,
        choices=Priority.choices,
        default=Priority.LOW
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    assigned_to = models.ForeignKey(
        to=User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='assigned_tasks'
    )

    class Meta:
        db_table = 'tasks'
