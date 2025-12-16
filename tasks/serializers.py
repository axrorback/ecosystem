from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    department_code = serializers.CharField(source='department.code')
    created_by = serializers.SerializerMethodField()

    read_only = True
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'department_code',
            'status',
            'priority',
            'created_by',
            'deadline',
            'created_at',

        )
        read_only_fields = ('created_by',)

    def get_created_by(self, obj):
        if obj.created_by:
            return {
                'username': obj.created_by.username,
            }
        return None