"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .settings.settings import DEBUG
import stream.routing as chat_routes

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # Just HTTP for now. (We can add other protocols later.)
        'websocket': AuthMiddlewareStack(
            URLRouter(
                chat_routes.websocket_urlpatterns
            )
        )
    }
)
