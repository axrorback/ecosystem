import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from tasks.models import Task
from .models import TaskChatRoom, TaskChatMessage


class TaskChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.room_group_name = f"task_chat_{self.task_id}"

        if not self.user.is_authenticated:
            await self.close()
            return

        allowed = await self.is_user_allowed()
        if not allowed:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')

        if not message:
            return

        room = await self.get_room()
        if not room.is_active:
            return

        msg = await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': self.user.username,
                'message': msg.message,
                'created_at': str(msg.created_at)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    # ===== DB helpers =====

    @database_sync_to_async
    def is_user_allowed(self):
        return Task.objects.filter(
            id=self.task_id,
            department__members=self.user
        ).exists()

    @database_sync_to_async
    def get_room(self):
        return TaskChatRoom.objects.get(task_id=self.task_id)

    @database_sync_to_async
    def save_message(self, message):
        room = TaskChatRoom.objects.get(task_id=self.task_id)
        return TaskChatMessage.objects.create(
            room=room,
            user=self.user,
            message=message
        )


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_notifications_{user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'title': event['title'],
            'body': event['body'],
            'task_id': event.get('task_id')
        }))