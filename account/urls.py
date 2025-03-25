from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserListCreateAPIView,
    PermissionListAPIView,
    RoleListCreateAPIView,
    RoleRetrieveUpdateDestroyAPIView, AuthUserAPIView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('permissions/', PermissionListAPIView.as_view(), name='permission-list'),
    path('roles/', RoleListCreateAPIView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroyAPIView.as_view(), name='role-retrieve-update-delete'),
    path('user/', AuthUserAPIView.as_view(), name='auth-user'),
]