import django_filters
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .serializers import UserCountSerializer
from .permissions import IsDev, IsCEO, IsManager, IsSuperUser, IsSimpleUser

class UserCountView(GenericAPIView):
    http_method_names = ['get']
    permission_classes = [IsCEO or IsSuperUser]
    @swagger_auto_schema(tags=['Log'],)
    def get(self, request):
        all_count = CustomUser.objects.all().count()
        active_count = CustomUser.objects.filter(is_active=True).count()
        not_active_count = CustomUser.objects.filter(is_active=False).count()
        staff_count = CustomUser.objects.filter(is_staff=True).count()
        ceo_count = CustomUser.objects.filter(role='ceo').count()
        sup_count = CustomUser.objects.filter(role='super').count()
        manager_count = CustomUser.objects.filter(role='manager').count()
        simple_count = CustomUser.objects.filter(role='simpleuser').count()
        dev_count = CustomUser.objects.filter(role='dev').count()

        data = {
            'all_users': all_count,
            'active_users': active_count,
            'inactive_user': not_active_count,
            'staff_users': staff_count,
            'roles': {
                'ceo': ceo_count,
                'manager': manager_count,
                'simple_user': simple_count,
                'dev': dev_count,
                'super': sup_count
            }
        }

        return Response({
            'status': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Barcha foydalanuvchilar soni',
            'data': data,
            'timestamp': datetime.now(),
        })