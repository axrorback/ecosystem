from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)

        new_paths = {}
        for path, path_item in schema.paths.items():
            new_paths[f"/api/v1{path}"] = path_item
        schema.paths = new_paths

        schema.servers = [{'url': '/api/v1'}]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title='CODERBOYS',
        default_version='v1',
        description='API Documentation for CODERBOYS EcoSysTem',
        contact=openapi.Contact(email='info@axrorback.uz',name='Ahrorjon Ibrohimjonov',telegram='@axrorback'),
    ),
    public=True,
    generator_class=CustomSchemaGenerator,
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
    path('api/v1/chat/',include('chat.urls')),

]
