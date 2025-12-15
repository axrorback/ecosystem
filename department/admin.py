from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'created_by',
        'members_count',
        'is_active',
    )

    search_fields = ('code', 'name')
    list_filter = ('is_active',)

    fieldsets = (
        ('Department Details', {
            'fields': ('code', 'name', 'is_active')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('code',)
        return ()

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def members_count(self, obj):
        return obj.members.count()
    members_count.short_description = 'Members'