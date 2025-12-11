from rest_framework import serializers
from users.models import CustomUser


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=15,required=True)
    password = serializers.CharField(max_length=25,required=True)

    def validate(self,data):
        if data['username'] is None or data['password'] is None:
            raise serializers.ValidationError('Username or Password cannot be empty')
        return data


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
