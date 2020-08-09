from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

from tpousers.token_auth import TokenAuthMiddleware
from tpousers.consumers import TransactionsConsumer

application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddleware(
        URLRouter([
            path("", TransactionsConsumer),
        ]),
    ),

})