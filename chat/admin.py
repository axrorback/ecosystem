from django.contrib import admin
from .models import TaskChatRoom , TaskChatMessage

admin.site.register(TaskChatMessage)
admin.site.register(TaskChatRoom)
