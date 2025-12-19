# chat/urls.py
from django.urls import path
from .views import TaskChatHistoryAPIView

urlpatterns = [
    path('history/<uuid:task_id>', TaskChatHistoryAPIView.as_view(), name='task-chat-history'),
]
