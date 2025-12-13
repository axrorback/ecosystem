from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from .models import Department
from .serializers import DepartmentSerializer



class DepartmentList(GenericAPIView):
    http_method_names = ['get']
    serializer_class = DepartmentSerializer
    def get(self,request):
        departments = DepartmentSerializer(Department.objects.all(),many=True).data
        return Response({
            'status':True,
            'statusCode':status.HTTP_200_OK,
            'data':{
                'departments':departments,
            },
            'message':'success',
            'total':Department.objects.count(),
            'timestamp':datetime.now()
        })