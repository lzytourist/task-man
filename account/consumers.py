import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None

    def connect(self):
        if self.scope['user'].is_authenticated:
            user = self.scope['user']

            self.group_name = f'inbox_{user.id}'
            async_to_sync(self.channel_layer.group_add)(
                self.group_name, self.channel_name
            )

            self.accept()
        else:
            self.close(reason='Authentication required')

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.close()

    def notify_user(self, message):
        self.send(text_data=json.dumps(message))
