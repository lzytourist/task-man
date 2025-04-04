from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User, Permission, Role, Notification
from account.permissions import HasPermission
from account.serializers import UserSerializer, PermissionSerializer, RoleSerializer, AuthUserSerializer, \
    NotificationSerializer


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, HasPermission)
    required_permissions = ['create_user', 'view_user']


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, HasPermission)
    required_permissions = ['view_user']

    def get_permissions(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            self.required_permissions = ['update_user']
        elif self.request.method == 'DELETE':
            self.required_permissions = ['delete_user']
        return super().get_permissions()


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


class AuthUserAPIView(APIView):
    serializer_class = AuthUserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user, context={'request': request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=request.user,
            data=request.data,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                'message': 'Account information has been updated.',
                'user': serializer.data
            }
        )


class NotificationListAPIView(ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-created_at')
