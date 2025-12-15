from django.db import models
import uuid
from io import BytesIO
from tasks.models import Task
from django.conf import settings

class Meeting(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4(),editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='meetings')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title






class Attendance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendances')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='meeting_qrcodes/')

    def __str__(self):
        return self.meeting