from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            required_permissions = getattr(view, 'required_permissions', None)
            if required_permissions:
                permissions = request.user.role.permissions.value_list('codename', flat=True)
                return all(required_permissions in permission for permission in permissions)
            return True
        return False
