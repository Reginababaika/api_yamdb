from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class IsUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
        ):
            return True
        return bool(
            obj.author == request.user
            and request.user.is_user
        )
