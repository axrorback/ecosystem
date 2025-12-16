from django.urls import path
from .views import TaskList

urlpatterns = [
    path('list/', TaskList.as_view()),
]