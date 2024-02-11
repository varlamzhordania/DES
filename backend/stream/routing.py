from django.urls import path
from .consumers import StreamConsumer,AdminConsumer

websocket_urlpatterns = [
    path('stream/', StreamConsumer.as_asgi()),
    path('admin/', AdminConsumer.as_asgi())
]
