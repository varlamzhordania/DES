from django.urls import path
from .consumers import StreamConsumer,AdminConsumer

websocket_urlpatterns = [
    path('stream/', StreamConsumer.as_asgi()),
    path('stream/<int:room_id>/', StreamConsumer.as_asgi()),
    path('admin/', AdminConsumer.as_asgi())
]
