from .models import CustomUser , OTP , PendingEmailChange
from .serializers import *
from datetime import  timedelta , datetime , timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken , OutstandingToken , BlacklistedToken
from .utils import generate_otp
from .tasks import mail_task , new_mail
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView


class LoginView(GenericAPIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]
    serializer_class = LoginSerializers
    @swagger_auto_schema(tags=['Authentication'])
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({
                'status':False,
                'statusCode':status.HTTP_400_BAD_REQUEST,
                'message': 'Bad Request',
                'timestamp':datetime.now()
            })
        if not user.is_active:
            return Response({
                'status':False,
                'statusCode':status.HTTP_400_BAD_REQUEST,
                'message': 'User is not active',
                'timestamp':datetime.now()
            })
        if not user.check_password(password):
            return Response({
                'status':False,
                'statusCode':status.HTTP_401_UNAUTHORIZED,
                'message': 'Username or Password is incorrect',
                'timestamp':datetime.now()
            })
        refresh = RefreshToken.for_user(user)
        refresh['role'] = str(user.role)
        refresh['username'] = str(user.username)
        refresh['first_name'] = str(user.first_name)
        refresh['last_name'] = str(user.last_name)
        refresh['email'] = str(user.email)
        refresh['date_joined'] = str(user.date_joined)
        return Response({
            'status':True,
            'statusCode':status.HTTP_200_OK,
            'message':'Login successfully',
            'refresh':str(refresh),
            'access':str(refresh.access_token),
            'timestamp':datetime.now()
        })

class SendOTPView(GenericAPIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer
    @swagger_auto_schema(tags=['Authentication'])
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return Response({
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'If you are in our Database we will send you an OTP',
                    'timestamp': datetime.now()
                })
            if user.is_active:
                return Response({
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'User allready verified'
                })
            otp = generate_otp()
            email  = user.email
            mail_task.delay(otp,email)
            OTP.objects.create(user=user,otp=otp,purpose='verify')
            return Response({
                'status': True,
                'statusCode': status.HTTP_200_OK,
                'message':'If you are in our Database we will send you an OTP',
                'timestamp':datetime.now(),
            })

class VerifyOTPView(GenericAPIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer
    @swagger_auto_schema(tags=['Authentication'])
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.validated_data['otp']
            try:
                obj_otp = OTP.objects.filter(otp=otp,purpose='verify',is_used=False).first()
            except OTP.DoesNotExist:
                return Response({
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid OTP',
                    'timestamp': datetime.now()
                })
            if timezone.now() - obj_otp.created_at >  timedelta(minutes=5):
                return Response({
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'OTP expired',
                    'timestamp': datetime.now()
                })
            user = obj_otp.user
            user.is_active = True
            user.save()
            obj_otp.is_used = True
            obj_otp.save()
            return Response({
                'status': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Your account verified successfully you can login now',
                'timestamp': datetime.now()
            })


class ChangePasswordView(GenericAPIView):
    http_method_names = ['post']
    serializer_class = ChangePasswordSerializer
    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            user = request.user

            if not user.check_password(old_password):
                return Response({
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'Old password is incorrect',
                    'timestamp': datetime.now()
                })

            user.set_password(new_password)
            user.save()

            tokens = OutstandingToken.objects.filter(user=user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response({
                'status': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Password changed successfully and all devices logged out',
                'timestamp': datetime.now()
            })

class ForgotPasswordView(GenericAPIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer
    @swagger_auto_schema(tags=['Authentication'])
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return Response({
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'User not found',
                    'timestamp': datetime.now(),

                })
            if not user.is_active:
                return Response({
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'User is not active',
                    'timestamp': datetime.now(),
                })
            otp = generate_otp()
            email  = user.email
            mail_task.delay(otp,email)
            OTP.objects.create(user=user,otp=otp,purpose='forgot')
            return Response({
                'status': True,
                'statusCode': status.HTTP_200_OK,
                'message':'Email sent successfully',
                'timestamp':datetime.now()
            })
class VerifyForgotView(GenericAPIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]
    @swagger_auto_schema(tags=['Authentication'])
    def post(self,request):
        serializer = VerifyOTPForForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            try:
                obj_otp = OTP.objects.filter(otp=otp,purpose='forgot',is_used=False).first()
            except OTP.DoesNotExist:
                return Response({
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid OTP',
                    'timestamp': datetime.now()
                })
            if timezone.now() - obj_otp.created_at >  timedelta(minutes=5):
                return Response({
                    'status': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'OTP is expired',
                    'timestamp': datetime.now()
                })
            user = obj_otp.user
            user.set_password(new_password)
            user.save()
            obj_otp.is_used = True
            obj_otp.save()
            return Response({
                'status':True,
                'statusCode':status.HTTP_200_OK,
                'message':'Password changed successfully',
                'timestamp':datetime.now()
            })

class LogoutView(GenericAPIView):
    http_method_names = ['post']
    @swagger_auto_schema(tags=['Authentication'])
    def post(self,request):
        request.user.auth_token.delete()
        return Response({
            'status':True,
            'statusCode':status.HTTP_200_OK,
            'message':'Logout successfully',
            'timestamp':datetime.now()
        })

class ProfileView(GenericAPIView):
    http_method_names = ['get']
    @swagger_auto_schema(tags=['Authentication'])
    def get(self,request):
        user = request.user
        return Response({
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'is_active':user.is_active,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'date_joined':user.date_joined,
        })

class ChangeProfileView(GenericAPIView):
    http_method_names = ['patch']
    serializer_class = ChangePasswordSerializer
    @swagger_auto_schema(tags=['Authentication'])
    def patch(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            data = serializer.validated_data
            if 'email' in data and data['email'] != user.email:
                email = data['email']
                code = generate_otp()
                PendingEmailChange.objects.filter(user=user).delete()

                PendingEmailChange.objects.create(user=user,new_email=email,code=str(code))
                new_mail.delay(email,code,user.id)
                return Response({
                    'status':True,
                    'statusCode':status.HTTP_200_OK,
                    'message':'Email changed successfully,Check your email for verification code',
                    'timestamp':datetime.now()
                })
            for field , value in data.items():
                setattr(user,field,value)
            user.save()
            return Response({
                'status':True,
                'statusCode':status.HTTP_200_OK,
                'message':'Profile changed successfully',
                'timestamp':datetime.now()
            })

class VerifyNewEmailView(GenericAPIView):
    http_method_names = ['post']
    serializer_class = ChangeEmailVerifySerializer
    @swagger_auto_schema(tags=['Authentication'])
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            code = serializer.validated_data['code']
            try:
                obj_otp = PendingEmailChange.objects.get(user=user)
            except PendingEmailChange.DoesNotExist:
                return Response({
                    'status':False,
                    'statusCode':status.HTTP_400_BAD_REQUEST,
                    'message':'Invalid code',
                    'timestamp':datetime.now()
                })
            if obj_otp.code != code:
                return Response({
                    'status':False,
                    'statusCode':status.HTTP_400_BAD_REQUEST,
                    'message':'Invalid code',
                })
            if timezone.now() - obj_otp.created_at >  timedelta(minutes=5):
                return Response({
                    'status':False,
                    'statusCode':status.HTTP_400_BAD_REQUEST,
                    'message':'Code is expired',
                    'timestamp':datetime.now()
                })
            user.email = obj_otp.new_email
            user.save()
            obj_otp.delete()
            return Response({
                'status':True,
                'statusCode':status.HTTP_200_OK,
                'message':'Email changed successfully',
                'timestamp':datetime.now()
            })