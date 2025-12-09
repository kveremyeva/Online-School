from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModer(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class CanDeleteLesson(permissions.BasePermission):
    """Комбинированный permission для удаления уроков"""
    def has_permission(self, request, view):
        is_authenticated = request.user and request.user.is_authenticated
        is_not_moderator = not request.user.groups.filter(name="moderators").exists()
        return is_authenticated and is_not_moderator

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
