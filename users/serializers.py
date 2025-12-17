from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()
from django.contrib.auth.models import update_last_login
from django.utils import timezone
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "detail": "Username or password is incorrect"
            })

        if not user.is_active:
            raise serializers.ValidationError({
                "detail": "User is not active"
            })

        if not user.check_password(password):
            raise serializers.ValidationError({
                "detail": "Username or password is incorrect"
            })
        update_last_login(None,user)
        local_time = timezone.localtime(user.last_login)
        refresh = RefreshToken.for_user(user)

        refresh['role'] = str(user.role)
        refresh['username'] = user.username
        refresh['first_name'] = user.first_name
        refresh['last_name'] = user.last_name
        refresh['email'] = user.email
        refresh['phone_number'] = user.phone_number
        refresh['date_joined'] = str(user.date_joined)
        refresh['last_login'] = str(local_time.strftime('%Y-%m-%d %H:%M:%S'))
        refresh['created_departments'] = [
            {"id": str(dept.id), "code": dept.code, "name": dept.name}
            for dept in user.created_departments.all()
        ]
        refresh['member_departments'] = [
            {"id": str(dept.id), "code": dept.code, "name": dept.name}
            for dept in user.department.all()
        ]
        return {
            "user": user,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }


class VerifyAccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15,required=True)

    def validate(self,data):
        if data['username'] is None:
            raise serializers.ValidationError('Username cannot be empty')
        return data

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6,required=True)

    def validate(self,data):
        if data['otp'] is None:
            raise serializers.ValidationError('OTP cannot be empty')
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=25,required=True)
    new_password = serializers.CharField(max_length=25,required=True)
    confirm_password = serializers.CharField(max_length=25,required=True)

    def validate(self,data):
        if data['old_password'] is None or data['new_password'] is None or data['confirm_password'] is None:
            raise serializers.ValidationError('All fields are required')
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError('New password cannot be the same as old password')
        return data

class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15,required=True)

    def validate(self,data):
        if data['username'] is None:
            raise serializers.ValidationError('Username cannot be empty')
        return data

class VerifyOTPForForgotPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6,required=True)
    new_password = serializers.CharField(max_length=25,required=True)
    confirm_password = serializers.CharField(max_length=25,required=True)

    def validate(self,data):
        if data['otp'] is None or data['new_password'] is None or data['confirm_password'] is None:
            raise serializers.ValidationError('All fields are required')
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data


class ChangeProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25, required=False)
    last_name = serializers.CharField(max_length=25, required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=13, required=False)
    telegram_id = serializers.CharField(max_length=13, required=False)

    def validate(self, data):
        if not any([
            data.get('first_name'),
            data.get('last_name'),
            data.get('email'),
            data.get('phone_number'),
            data.get('telegram_id')
        ]):
            raise serializers.ValidationError("At least one field is required.")
        return data


class ChangeEmailVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6,required=True)

    def validate(self,data):
        if data['code'] is None:
            raise serializers.ValidationError('Code cannot be empty')
        return data