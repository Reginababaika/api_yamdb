from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated and
            request.user.role == 'admin' or
            request.user.is_superuser
        )

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.user.role == 'admin' or
            request.user.is_superuser
        )

class IsUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated
        )

class IsModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated and
            request.user.role == 'moderator' or
            request.user.role == 'admin' or
            request.user.is_superuser
        )