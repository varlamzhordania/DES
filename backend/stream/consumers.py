from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, OrderSerializer
from rest_framework.renderers import JSONRenderer
from checkout.models import Order
import json


class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await self.get_user()
        self.room_group_name = f'chat_room'
        # Add the consumer to the group when connected
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        if user.is_anonymous:
            # Handle authentication failure, for example, close the connection
            await self.close()
        else:
            print(f"Connected: {user}")

    async def disconnect(self, close_code):
        # Remove the consumer from the group when disconnected
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        # Parse received JSON data
        dict_data = json.loads(text_data)
        message = dict_data['message']
        action = dict_data['action']

        # Check the action type
        if action == 'new-offer' or action == 'new-answer':
            receiver_channel_name = dict_data['message']['receiver_channel_name']
            dict_data['message']['receiver_channel_name'] = self.channel_name

            # Send the SDP message to the specified receiver
            await self.channel_layer.send(receiver_channel_name, {'type': 'send.sdp', 'dict_data': dict_data})

        # Set the sender's channel name in the message
        dict_data['message']['receiver_channel_name'] = self.channel_name

        # Broadcast the message to the entire group
        await self.channel_layer.group_send(self.room_group_name, {'type': 'send.sdp', 'dict_data': dict_data})

    async def send_sdp(self, event):
        # Send the SDP message to the client
        dict_data = event['dict_data']
        await self.send(
            text_data=json.dumps(dict_data)
        )

    @database_sync_to_async
    def get_user(self):
        return self.scope["user"] if self.scope and "user" in self.scope else AnonymousUser()


class AdminConsumer(AsyncWebsocketConsumer):
    user = AnonymousUser()
    admin_room = None

    async def connect(self):
        """
         Connects the WebSocket for admin users, adding them to a group.
        """
        if self.has_permission:
            self.user = self.scope['user']
            self.admin_room = f'admin_room'
            await self.channel_layer.group_add(self.admin_room, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """
        Disconnects the WebSocket for admin users, removing them from the group.
        """
        await self.channel_layer.group_discard(self.admin_room, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """
        Handles incoming WebSocket messages.
        """
        dict_data = json.loads(text_data)
        message = dict_data['message']
        action = dict_data['action']
        if action == 'user_list':
            await self.channel_layer.group_send(self.admin_room, {'type': 'send.user_list', 'dict_data': {}})
        if action == 'order_list':
            await self.channel_layer.group_send(self.admin_room, {'type': 'send.order_list', 'dict_data': {}})
        pass

    async def send_user_list(self, event):
        users = await self.get_users()
        message = {
            'action': 'user_list',
            'users': users,
        }
        await self.send(text_data=json.dumps(message))

    async def send_order_list(self, event):
        orders = await self.get_orders()
        message = {
            "action": "order_list",
            "orders": orders,
        }
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_orders(self):
        orders = Order.objects.filter(
            status__in=[Order.OrderStatusChoices.PENDING, Order.OrderStatusChoices.PROCESSING]
        )
        return self.get_serializer_data_to_dict(OrderSerializer(orders, many=True))

    @database_sync_to_async
    def get_users(self):
        users = get_user_model().objects.all().exclude(id=self.user.id)
        return self.get_serializer_data_to_dict(UserSerializer(users, many=True))

    def get_serializer_data_to_dict(self, serializer):
        serialized_data = JSONRenderer().render(serializer.data)
        return json.loads(serialized_data.decode())

    @database_sync_to_async
    def has_permission(self):
        return self.scope['user'].is_staff or self.scope['user'].is_superuser or self.scope['user'].groups.filter(
            name="Manager"
        ).exists()
