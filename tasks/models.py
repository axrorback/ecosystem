from django.db import models
from django.conf import settings
import uuid
from django.db.models import SET_NULL , CASCADE
from department.models import Department
STATUS_CHOICES = (
    ('pending','Pending'),
    ('in_progress','In Progress'),
    ('done','Done')
)

PRIORITY_CHOICES = (
    ('low','Low'),
    ('medium','Medium'),
    ('high','High'),
    ('critical','Critical')
)

class Task(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=CASCADE,related_name='tasks')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=SET_NULL,null=True,related_name='created_tasks')
    status = models.CharField(max_length=12,choices=STATUS_CHOICES,default='pending')
    priority = models.CharField(max_length=12,choices=PRIORITY_CHOICES,default='medium')
    deadline = models.DateTimeField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} --> {self.department}'




CHANNEL_CHOICE = (
    ('telegram','Telegram'),
    ('email','Email')
)



class TaskNotify(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    task = models.ForeignKey(Task,on_delete=CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    channel = models.CharField(max_length=12,choices=CHANNEL_CHOICE)

    is_sent = models.BooleanField(default=False)

    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
