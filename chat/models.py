from django.db import models
import uuid
from users.models import CustomUser

class TaskChatRoom(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    task = models.OneToOneField('tasks.Task',on_delete=models.CASCADE,related_name='chat_room')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat for {self.task.title}"


class TaskChatMessage(models.Model):
    room = models.ForeignKey(
        TaskChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    attachment = models.FileField(upload_to='chat/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']



class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)