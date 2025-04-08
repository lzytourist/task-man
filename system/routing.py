from django.urls import re_path

from account.consumers import (
    NotificationConsumer,
)

websocket_urlpatterns = [
    re_path(r'ws/notifications/', NotificationConsumer.as_asgi()),
    # re_path(r"ws/notifications/(?P<access_token>\w+)/$", NotificationConsumer.as_asgi()),
]
