from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='CODERBOYS',
        default_version='v1',
        description='API Documentation for CODERBOYS EcoSysTem',
        contact=openapi.Contact(email='info@axrorback.uz',name='Ahrorjon Ibrohimjonov'),
    ),
    public=True,
    permission_classes=[AllowAny],
)


from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/department/',include('department.urls')),
    path('api/v1/swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    path('api/v1/log/',include('log.urls')),
    path('api/v1/tasks/', include('tasks.urls')),

]
