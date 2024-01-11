from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from spa import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/match/', consumers.MatchConsumer.as_asgi()),
    ]),
})
