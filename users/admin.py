from django.contrib import admin
from .models import CustomUser ,  OTP , TwoFactorOTP , PendingEmailChange
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'first_name','email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-id',)

    # Admin change page da department qo‘shish uchun
    filter_horizontal = ('department',)  # ManyToMany uchun chiroyli widget

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password','first_name','last_name', 'department')  # <-- qo‘shildi
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active', 'departments'),  # <-- qo‘shildi
        }),
    )


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