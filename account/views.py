from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User, Permission, Role, Notification
from account.permissions import HasPermission
from account.serializers import UserSerializer, PermissionSerializer, RoleSerializer, AuthUserSerializer, \
    NotificationSerializer
from account.tasks import send_user_email


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, HasPermission)
    required_permissions = ['create_user', 'view_user']

    def get_permissions(self):
        if self.request.method == 'GET':
            self.required_permissions = ['view_user']
        return super().get_permissions()


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

    def get_permissions(self):
        if self.request.method == 'GET':
            self.required_permissions = ['view_role']
        return super().get_permissions()


class RoleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = (IsAuthenticated, HasPermission)
    required_permissions = ['update_role', 'view_role']

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.required_permissions = ['delete_role']
        elif self.request.method == 'GET':
            self.required_permissions = ['view_role']
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


class MarkSeenAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        notification_ids = request.data.get('ids')

        errors = []
        if notification_ids is None:
            errors.append('notification id(s) are required')
        elif not isinstance(notification_ids, list):
            errors.append('notification id(s) should be a list')
        elif len(notification_ids) == 0:
            errors.append('notification id(s) should not be empty')

        if len(errors):
            return Response(
                data={'notification_ids': errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        (Notification.objects
         .filter(user_id=request.user)
         .filter(id__in=notification_ids)
         .update(seen=True))

        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationDestroyAPIView(DestroyAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class SendEmailAPIView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permissions = ['send_email']

    def post(self, request, *args, **kwargs):
        to = request.data.get('to', None)
        subject = request.data.get('subject', None)
        message = request.data.get('message', None)

        if not to or not subject or not message:
            return Response(
                data={'error': 'missing required fields'},
                status=status.HTTP_400_BAD_REQUEST
            )

        send_user_email.delay([to], subject, message)
        return Response(status=status.HTTP_204_NO_CONTENT)