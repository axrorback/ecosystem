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
    permission_classes = [AllowAny]
    http_method_names = ['get']
    serializer_class = DepartmentSerializer
    @swagger_auto_schema(tags=['Department'])
    def get(self,request):
        departments = DepartmentSerializer(Department.objects.all(),many=True).data
        return Response({
            'status':True,
            'statusCode':status.HTTP_200_OK,
            'message': 'success',
            'data':{
                'departments':departments,
            },
            'total':Department.objects.count(),
            'timestamp':datetime.now()
        })