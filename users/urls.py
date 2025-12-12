from django.urls import path
from users.views import LoginView , VerifyOTPView , SendOTPView , ForgotPasswordView , VerifyForgotView , LogoutView,ProfileView,ChangePasswordView , ChangeProfileView,VerifyNewEmailView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('send-verify-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('verify-forgot-otp/', VerifyForgotView.as_view()),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    path('logout/',LogoutView.as_view()),
    path('change-profile/',ChangeProfileView.as_view(),name='change_profile'),
    path('verify-new-email/',VerifyNewEmailView.as_view(),name='verify_new_email'),
    path('refresh-token/',TokenRefreshView.as_view(),name='token_refresh'),
]