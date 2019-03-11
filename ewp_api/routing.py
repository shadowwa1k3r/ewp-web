from channels.routing import ProtocolTypeRouter, URLRouter
from chat.jwttokenauth import TokenAuthMiddleWareStack
import chat.routing
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': TokenAuthMiddleWareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})
