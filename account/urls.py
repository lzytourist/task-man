from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserListCreateAPIView,
)

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
]