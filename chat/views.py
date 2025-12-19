# chat/views.py
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from tasks.models import Task
from .models import TaskChatMessage
from .serializers import TaskChatMessageSerializer
from django.shortcuts import get_object_or_404

class TaskChatHistoryAPIView(GenericAPIView):
    serializer_class = TaskChatMessageSerializer

    @swagger_auto_schema(
        operation_description="Task chat historyni olish",
        tags=['Chat'],
    )
    def get(self, request, task_id, *args, **kwargs):
        user = request.user

        # Faqatgina user department azolari yoki task creator bo'lsa
        task = get_object_or_404(
            Task.objects.prefetch_related('department__members'),
            id=task_id
        )

        if user not in task.department.members.all() and user != task.created_by:
            return Response({
                'status': False,
                'statusCode': status.HTTP_403_FORBIDDEN,
                'message': 'Siz bu task chatini ko‘ra olmaysiz.',
                'data': [],
            }, status=status.HTTP_403_FORBIDDEN)

        queryset = TaskChatMessage.objects.filter(room__task=task).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():
            return Response({
                'status': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Hali xabar yo‘q',
                'data': [],
            })

        return Response({
            'status': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Task chat history',
            'data': serializer.data,
        })
