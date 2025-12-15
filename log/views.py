import django_filters
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status , filters
from users.models import CustomUser
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSerializer
from .permissions import IsCEO, IsSuperUser
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi

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

class UserSearchListView(GenericAPIView):
    http_method_names = ['get']
    permission_classes = [IsCEO | IsSuperUser]

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend
    ]

    search_fields = ['username', 'email']
    filterset_fields = ['is_active', 'is_staff']

    @swagger_auto_schema(
        tags=['Log'],
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Username yoki email bo‘yicha qidirish",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Faol userlar",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'is_staff',
                openapi.IN_QUERY,
                description="Staff userlar",
                type=openapi.TYPE_BOOLEAN
            ),
        ]
    )
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({
                'status': False,
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'Foydalanuvchi topilmadi',
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Foydalanuvchilar ro‘yxati',
            'count': queryset.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)

