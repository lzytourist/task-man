from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView

from account.models import User
from account.permissions import HasPermission
from account.serializers import UserSerializer


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, HasPermission)
    required_permissions = ['create_user', 'view_user']
