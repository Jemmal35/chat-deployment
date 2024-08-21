"""
ASGI config for chatapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

application = get_asgi_application()

from chat import routing
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # "websocket": AuthMiddlewareStack(
    # URLRouter(
    #     routing.websocket_urlpatterns
    # ),
    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
        )
})