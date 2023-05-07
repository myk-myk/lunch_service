from rest_framework import permissions


class UserIsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'create']:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        else:
            return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve' or request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        elif view.action in ['update', 'partial_update', 'destroy']:
            return bool(obj == request.user or request.user.is_superuser)
        else:
            return request.user.is_superuser


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve' or request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        else:
            return request.user.is_superuser


class IsStaffOrOwnerOrAuthenticatedOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'create'] or request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        else:
            return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve' or request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        elif view.action in ['update', 'partial_update', 'destroy']:
            return bool(obj.user == request.user or request.user.is_superuser)
        else:
            return request.user.is_superuser
