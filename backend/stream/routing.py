from django.urls import path
from .consumers import StreamConsumer

websocket_urlpatterns = [
    path('stream/', StreamConsumer.as_asgi())
]
