from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin and request.user.is_authenticated


class IsModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator and request.user.is_authenticated

