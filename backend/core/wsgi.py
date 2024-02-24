"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from .settings.settings import DEBUG

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
    print("ASGI: Django loaded up in setting mode : Development")
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
    print("ASGI: Django loaded up in setting mode : Production")

application = get_wsgi_application()
