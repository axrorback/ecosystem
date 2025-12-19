# chat/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from .models import TaskChatRoom

@receiver(post_save, sender=Task)
def create_task_chat(sender, instance, created, **kwargs):
    if created:
        TaskChatRoom.objects.create(task=instance)
