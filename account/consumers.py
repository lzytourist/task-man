import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from account.models import User


class NotificationConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None

    def connect(self):
        print(repr(self.scope))
        try:
            access_token = self.scope['url_route']['kwargs']['access_token']
            if access_token is None:
                raise TokenError("No access token")

            validated_token = AccessToken(access_token)

            user = User.objects.get(id=validated_token.get('user_id'))
            self.group_name = f'inbox_{user.id}'

            self.accept()
        except (TokenError, User.DoesNotExist) as e:
            self.close(reason=str(e))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.close()

    def notify_user(self, message):
        self.send(text_data=json.dumps(message))
