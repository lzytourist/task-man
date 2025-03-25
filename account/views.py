from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from account.models import User, Permission, Role
from account.permissions import HasPermission
from account.serializers import UserSerializer, PermissionSerializer, RoleSerializer


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, HasPermission)
    required_permissions = ['create_user', 'view_user']


class PermissionListAPIView(ListAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    permission_classes = (IsAuthenticated, HasPermission)
    required_permissions = ['view_role', 'create_role']


class RoleListCreateAPIView(ListCreateAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.prefetch_related('permissions').all()
    permission_classes = (IsAuthenticated, HasPermission)
    required_permissions = ['create_role', 'view_role']


class RoleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = (IsAuthenticated, HasPermission)
    required_permissions = ['update_role', 'view_role']

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.required_permissions = ['delete_role']
        return super().get_permissions()
