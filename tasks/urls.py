from django.urls import path
from .views import TaskList , TaskDetail

urlpatterns = [
    path('list/', TaskList.as_view()),
    path('detail/<uuid:pk>/',TaskDetail.as_view())
]