from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from .models import Department
from .serializers import DepartmentSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny


class DepartmentList(GenericAPIView):
    serializer_class = DepartmentSerializer
    http_method_names = ['get']
    @swagger_auto_schema(tags=['Department'])
    def get(self, request):
        queryset = (
            Department.objects
            .select_related('created_by')
            .prefetch_related('members')
            .order_by('-created_at')
        )
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Success',
            'data': {
                'departments': serializer.data,
            },
            'total_department_count': queryset.count(),
            'timestamp': datetime.now(),
        }, status=status.HTTP_200_OK)