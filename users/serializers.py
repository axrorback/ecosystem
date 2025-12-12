from rest_framework import serializers

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


class ChangeProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25, required=False)
    last_name = serializers.CharField(max_length=25, required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=13, required=False)

    def validate(self, data):
        if not any([
            data.get('first_name'),
            data.get('last_name'),
            data.get('email'),
            data.get('phone_number')
        ]):
            raise serializers.ValidationError("At least one field is required.")
        return data


class ChangeEmailVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6,required=True)

    def validate(self,data):
        if data['code'] is None:
            raise serializers.ValidationError('Code cannot be empty')
        return data