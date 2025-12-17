from django.db.models.signals import post_save
from django.dispatch import receiver

from tasks.models import Task, TaskNotify
from .tasks import send_task_notification


@receiver(post_save, sender=Task)
def notify_department_members(sender, instance, created, **kwargs):
    if not created:
        return

    members = instance.department.members.all()

    for user in members:
        if getattr(user, 'telegram_id', None):
            channel = 'telegram'
        elif user.email:
            channel = 'email'
        else:
            continue

        notify = TaskNotify.objects.create(
            task=instance,
            user=user,
            channel=channel
        )

        # Celery job queue
        send_task_notification.delay(notify.id)
