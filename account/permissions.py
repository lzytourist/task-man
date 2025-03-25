from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    def has_permission(self, request, view):
        required_permissions = getattr(view, 'required_permissions', None)
        if required_permissions:
            permissions = request.user.role.permissions.values_list('codename', flat=True)
            return all(permission in permissions for permission in required_permissions)
        raise ValueError('required_permissions should be defined HasPermission')
