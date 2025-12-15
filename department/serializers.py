from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = (
            'id',
            'code',
            'name',
            'is_active',
            'created_at',
            'created_by',
            'members_count',
        )

    def get_created_by(self, obj):
        if obj.created_by:
            return {
                'username': obj.created_by.username,
            }
        return None

    def get_members_count(self, obj):
        return obj.members.count()
