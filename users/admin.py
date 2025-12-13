from django.contrib import admin
from rest_framework_simplejwt.tokens import OutstandingToken , BlacklistedToken
from .models import CustomUser , ModelPermissions , OTP , TwoFactorOTP , PendingEmailChange


@admin.register(ModelPermissions)
class ModelPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'app_label', 'model_name', 'permission')
    list_filter = ('app_label', 'model_name', 'permission')