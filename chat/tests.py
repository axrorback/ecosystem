# chat/tests/test_task_chat.py
import uuid
import pytest
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from tasks.models import Task
from department.models import Department
from chat.models import TaskChatRoom

User = get_user_model()

@database_sync_to_async
def create_user():
    return User.objects.create_user(username="testuser", password="password")

@database_sync_to_async
def create_department(user):
    dept = Department.objects.create(name="Test Dept", created_by=user)
    dept.members.add(user)
    return dept

@database_sync_to_async
def create_task(user, department):
    return Task.objects.create(
        id=uuid.uuid4(),  # UUID id
        title="Test Task",
        department=department,
        created_by=user
    )

@database_sync_to_async
def create_chat_room(task):
    room, _ = TaskChatRoom.objects.get_or_create(task=task)
    return room


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_task_chat(test_application):
    user = await create_user()
    department = await create_department(user)
    task = await create_task(user, department)
    room = await create_chat_room(task)

    ws_url = f"/ws/tasks/{task.id}/chat/"
    communicator = WebsocketCommunicator(test_application, ws_url)

    communicator.scope['user'] = user

    connected, _ = await communicator.connect()
    assert connected, "WebSocketga ulanib bo'lmadi"

    test_message = "Hello team!"
    await communicator.send_json_to({"message": test_message})

    response = await communicator.receive_json_from()
    assert response["message"] == test_message
    assert response["username"] == user.username

    await communicator.disconnect()
