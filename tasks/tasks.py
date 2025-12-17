from celery import shared_task
from tasks.models import TaskNotify
from tasks.services.telegram import send_task_telegram
from tasks.services.email import send_task_email


from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

@shared_task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=30,
    retry_kwargs={'max_retries': 5},
)
def send_task_notification(self, notify_id):
    try:
        notify = TaskNotify.objects.select_related(
            'user', 'task'
        ).get(id=notify_id)
    except TaskNotify.DoesNotExist:
        return  # bu retry qilinmasligi kerak

    if notify.channel == 'telegram':
        send_task_telegram(notify.user, notify.task)
    elif notify.channel == 'email':
        send_task_email(notify.user, notify.task)

    notify.is_sent = True
    notify.save(update_fields=['is_sent'])

