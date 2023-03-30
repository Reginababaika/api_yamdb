from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.role == 'admin' and
            request.user.is_authenticated or
            request.user.is_superuser
        )

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.role == 'admin' and
            request.user.is_authenticated or
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
            request.user.role == 'moderator' and
            request.user.is_authenticated
        )
