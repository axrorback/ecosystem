# tasks/admin.py
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'department_code',
        'status',
        'priority',
        'deadline',
        'created_by',
        'created_at',
    )

    list_filter = ('status', 'priority', 'department__code')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

    def department_code(self,obj):
        return obj.department.code
    department_code.short_description = 'Department code'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

