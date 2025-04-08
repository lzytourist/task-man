from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = scope["url_route"]["kwargs"]["access_token"]
        if token is None:
            for key, value in scope['headers']:
                if key == b'authorization':
                    token = value.decode('utf-8').split(' ')[-1]
                    break

        scope['user'] = AnonymousUser()
        if token is not None:
            try:
                validated_token = AccessToken(token)
                user = await get_user(validated_token.get('user_id'))
                scope['user'] = user
                # print(repr(scope))
            except (TokenError, User.DoesNotExist) as e:
                pass

        return await self.inner(scope, receive, send)
