from rest_framework.permissions import BasePermission

class IsCEO(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'ceo'

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'super'

class IsManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'manager'

class IsSimpleUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'simpleuser'

class IsDev(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'dev'