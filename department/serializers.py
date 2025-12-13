from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Department
        fields = ['id','code','name','is_active','created_at','created_by_username']