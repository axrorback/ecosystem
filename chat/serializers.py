from rest_framework import serializers
from .models import TaskChatMessage

class TaskChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = TaskChatMessage
        fields = (
            'id',
            'username',
            'message',
            'attachment',
            'created_at'
        )