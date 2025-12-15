from rest_framework import serializers
from users.models import CustomUser, OTP, TwoFactorOTP, PendingEmailChange




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'telegram_id',
            'is_staff',
            'is_active',
            'role'
        ]
