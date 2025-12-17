# tasks/admin.py
from django.contrib import admin
from .models import Task ,TaskNotify

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

    exclude = ('created_by',)

    def department_code(self, obj):
        return obj.department.code
    department_code.short_description = 'Department code'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TaskNotify)
class TaskNotifyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'task',
        'user',
        'channel',
        'is_sent',
        'created_at',
    )

    list_filter = (
        'channel',
        'is_sent',
        'created_at',
    )

    search_fields = (
        'task__title',
        'user__username',
        'user__email',
    )

    readonly_fields = (
        'task',
        'user',
        'channel',
        'is_sent',
        'error_message',
        'created_at',
    )

    ordering = ('-created_at',)

    autocomplete_fields = (
        'task',
        'user',
    )

    fieldsets = (
        ('Asosiy maʼlumotlar', {
            'fields': (
                'task',
                'user',
                'channel',
            )
        }),
        ('Holati', {
            'fields': (
                'is_sent',
                'error_message',
            )
        }),
        ('Texnik maʼlumotlar', {
            'fields': (
                'created_at',
            )
        }),
    )

    # ❌ yangi qo‘shishni to‘xtatish
    def has_add_permission(self, request):
        return False

    # ❌ mavjudini o‘zgartirishni to‘xtatish
    def has_change_permission(self, request, obj=None):
        return False

    # ❌ delete qilmaslik
    def has_delete_permission(self, request, obj=None):
        return False
