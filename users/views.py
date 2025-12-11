from rest_framework.permissions import IsAuthenticated
from .models import CustomUser , OTP
from .serializers import *
from datetime import timezone , timedelta , datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken , OutstandingToken , BlacklistedToken
from .utils import generate_otp
from .tasks import mail_task
from rest_framework.permissions import AllowAny


class LoginView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    def post(self,request):
        serializer = LoginSerializers(data=request.data)
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

class SendOTPView(APIView):
    http_method_names = ['post']
    def post(self,request):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return Response({
                    'message': 'Agar siz bazamizda bolsangiz email boradi'
                })
            if user.is_active:
                return Response({
                    'message': 'User aktifdir'
                })
            otp = generate_otp()
            email  = user.email
            mail_task.delay(otp,email)
            OTP.objects.create(user=user,otp=otp,purpose='verify')
            return Response({
                'message':'Agar siz bazamizda bolsangiz email boradi'
            })

class VerifyOTPView(APIView):
    http_method_names = ['post']
    def post(self,request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.validated_data['otp']
            try:
                obj_otp = OTP.objects.filter(otp=otp,purpose='verify',is_used=False).first()
            except OTP.DoesNotExist:
                return Response({
                    'message': 'Invalid OTP'
                })
            if obj_otp.created_at > datetime.now() + timedelta(minutes=5):
                return Response({
                    'message': 'OTP eski'
                })
            user = obj_otp.user
            user.is_active = True
            user.save()
            obj_otp.is_used = True
            obj_otp.save()

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]   # to‘g‘rilandi
    http_method_names = ['post']

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            user = request.user

            # eski parolni tekshirish
            if not user.check_password(old_password):
                return Response({'message': 'Old password is incorrect'}, status=400)

            # yangi parolni yozish
            user.set_password(new_password)
            user.save()

            # 🔥 Barcha eski tokenlarni bekor qilish (logout from all devices)
            tokens = OutstandingToken.objects.filter(user=user)

            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response({
                'message': 'Password changed successfully. All sessions have been logged out.'
            })

class ForgotPasswordView(APIView):
    http_method_names = ['post']
    def post(self,request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return Response({
                    'message': 'User not found'
                })
            if not user.is_active:
                return Response({
                    'message': 'User is not active avval uzerni aktive qiling'
                })
            otp = generate_otp()
            email  = user.email
            mail_task.delay(otp,email)
            OTP.objects.create(user=user,otp=otp,purpose='forgot')
            return Response({
                'message':'Email jonatildi'
            })

class VerifyForgotView(APIView):
    http_method_names = ['post']
    def post(self,request):
        serializer = VerifyOTPForForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            try:
                obj_otp = OTP.objects.filter(otp=otp,purpose='forgot',is_used=False).first()
            except OTP.DoesNotExist:
                return Response({
                    'message': 'Invalid OTP'
                })
            if obj_otp.created_at > datetime.now() + timedelta(minutes=5):
                return Response({
                    'message': 'OTP eski'
                })
            user = obj_otp.user
            user.set_password(new_password)
            user.save()
            obj_otp.is_used = True
            obj_otp.save()
            return Response({
                'message':'Parol o`zgartirildi!'
            })

class LogoutView(APIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response({'message':'Logout successfull'})

class ProfileView(APIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
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