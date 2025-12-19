from django.urls import path
from .consumers import TaskChatConsumer , NotificationConsumer

websocket_urlpatterns = [
    path(
        'ws/tasks/<uuid:task_id>/chat/',
        TaskChatConsumer.as_asgi()
    ),
    path('ws/notifications/', NotificationConsumer.as_asgi())
]
