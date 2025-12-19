from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .serializers import TaskSerializer
from drf_yasg.utils import swagger_auto_schema
from tasks.models import Task


class TaskList(GenericAPIView):
    http_method_names = ['get']
    serializer_class = TaskSerializer

    @swagger_auto_schema(tags=['Tasks'])
    def get(self, request):
        user = request.user

        queryset = (
            Task.objects
            .select_related('department', 'created_by')
            .prefetch_related('department__members')
            .filter(department__members=user)
            .distinct()
            .order_by('-created_at')
        )

        if not queryset.exists():
            return Response({
                'status': True,
                'statusCode': status.HTTP_200_OK,
                'message': (
                    "You don't have any tasks yet. or you are not a member of any department."
                ),
                'data': {
                    'tasks': []
                },
                'total_tasks': 0,
                'timestamp': datetime.now(),
            })

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Tasks List',
            'data': {
                'tasks': serializer.data
            },
            'total_tasks': queryset.count(),
            'timestamp': datetime.now(),
        })


class TaskDetail(GenericAPIView):
    http_method_names = ['get']
    serializer_class = TaskSerializer

    @swagger_auto_schema(tags=['Tasks'])
    def get(self, request, pk):
        user = request.user

        # Taskni olish
        task_qs = (
            Task.objects
            .select_related('department', 'created_by')
            .prefetch_related('department__members')
            .filter(id=pk)
        )

        task = task_qs.first()
        if not task:
            return Response({
                'status': False,
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'Task not found.',
                'data': {},
                'timestamp': datetime.now(),
            }, status=status.HTTP_404_NOT_FOUND)
        if user == task.created_by and user not in task.department.members.all():
            return Response({
                'status':False,
                'statusCode':status.HTTP_400_BAD_REQUEST,
                'message':f'You created this task but you are not a member of this {task.department} department.',
                'timestamp':datetime.now()
            })

        serializer = self.get_serializer(task)

        return Response({
            'status': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Task Detail',
            'data': serializer.data,
            'timestamp': datetime.now(),
        })

