from rest_framework.permissions import BasePermission

from app.models import User


class RequireLoginPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return isinstance(request.user, User)
