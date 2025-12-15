from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    department_code = serializers.CharField(source='department.code')
    read_only = True
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'department',
            'department_code',
            'status',
            'priority',
            'deadline',
            'created_by',
            'created_at',
        )
        read_only_fields = ('created_by',)
