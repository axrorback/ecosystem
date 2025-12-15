from django.shortcuts import render
from rest_framework.views import GenericView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from .serializers import TaskSerializer
from drf_yasg.utils import swagger_auto_schema
from tasks.models import Task
from django.db.models import Q



class TaskList(GenericView):
    http_method_names = ['get']
    serializer_class = TaskSerializer
    data = Task.objects.all()
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(department__members=user))