from django.urls import path
from .views import *

urlpatterns = [
    path('users/user-stat/',UserCountView.as_view()),
]
