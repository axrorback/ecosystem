from django.contrib import admin
from .models import CustomUser ,  OTP , TwoFactorOTP , PendingEmailChange
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'first_name', 'email','role','get_departments', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-id',)
    filter_horizontal = ('department',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'department')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active', 'department')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'email', 'last_login', 'date_joined')
        return ()

    def get_departments(self, obj):
        return ", ".join([dept.name for dept in obj.department.all()])

    get_departments.short_description = 'Departments'


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'purpose',
        'otp',
        'is_used',
        'created_at',
    )

    list_filter = (
        'purpose',
        'is_used',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    ordering = ('-created_at',)

    readonly_fields = (
        'otp',
        'created_at',
        'user',
        'otp',
        'is_used',
        'created_at',
        'purpose',
    )

@admin.register(PendingEmailChange)
class PendingEmailChangeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'new_email',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'new_email',
    )

    ordering = ('-created_at',)

    readonly_fields = (
        'user',
        'new_email',
        'code',
        'created_at',
    )