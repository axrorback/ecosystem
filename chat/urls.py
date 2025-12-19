# chat/urls.py
from django.urls import path
from .views import TaskChatHistoryAPIView

urlpatterns = [
    path('tasks/<uuid:task_id>/history/', TaskChatHistoryAPIView.as_view(), name='task-chat-history'),
]
