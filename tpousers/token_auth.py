from urllib import parse

from channels.auth import UserLazyObject
from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async


@database_sync_to_async
def get_token_user(scope):
    query = parse.parse_qs(scope['query_string'].decode("utf-8"))['token'][0]
    try:
        token_key = query
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    """
    Token authorization middleware for Django Channels 2
    """

    def populate_scope(self, scope):
        # Make sure we have a session
        if 'token' not in dict(parse.parse_qs(scope['query_string'].decode("utf-8"))):
            raise ValueError(
                "TokenAuthMiddleware cannot find Token in scope."
            )
        # Add it to the scope if it's not there already
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        scope["user"]._wrapped = await get_token_user(scope)


# TokenAuthMiddlewareStack = lambda inner: AuthMiddlewareStack(TokenAuthMiddleware(inner))
