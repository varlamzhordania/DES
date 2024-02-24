"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .settings.settings import DEBUG

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
    print("ASGI: Django loaded up in setting mode : Development")
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
    print("ASGI: Django loaded up in setting mode : Production")


django.setup()

import stream.routing as chat_routes

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                chat_routes.websocket_urlpatterns
            )
        )
    }
)
