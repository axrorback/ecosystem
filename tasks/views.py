from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from .serializers import TaskSerializer
from drf_yasg.utils import swagger_auto_schema
from tasks.models import Task
from django.db.models import Q



class TaskList(GenericAPIView):
    http_method_names = ['get']
    @swagger_auto_schema(tags=['Tasks'])
    def get(self, request):
        queryset = Task.objects.all()
        all_tasks = Task.objects.all().count()
        serializer = TaskSerializer(queryset, many=True)
        data = {
            'tasks': serializer.data,
        }
        return Response({
            'status': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Tasks List',
            'data': data,
            'total_tasks': all_tasks,
            'timestamp': datetime.now(),
        }
        )


