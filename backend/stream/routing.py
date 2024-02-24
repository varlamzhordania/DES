from django.urls import path
from .consumers import StreamConsumer,AdminConsumer

websocket_urlpatterns = [
    path('ws/stream/', StreamConsumer.as_asgi()),
    path('ws/stream/<int:room_id>/', StreamConsumer.as_asgi()),
    path('ws/admin/', AdminConsumer.as_asgi())
]
