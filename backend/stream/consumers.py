from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from .serializers import SafeUserSerializer, OrderSerializer, UserRoomSerializer
from rest_framework.renderers import JSONRenderer
from checkout.models import Order
from .models import UserRoom
from django.core.management import call_command
import json


call_command("deactivate_rooms")


class StreamConsumer(AsyncWebsocketConsumer):
    user_room = None
    room_group_name = None
    user = None
    room_id = None

    async def connect(self):
        self.user = await self.get_user()
        if self.user.is_anonymous:
            await self.close()

        self.room_id = self.scope['url_route']['kwargs'].get('room_id', None)

        if self.room_id:
            self.user_room = await self.get_room_by_id(self.room_id)
            await self.update_busy_status(self.user_room, True)
        else:
            self.user_room, created = await self.get_or_create_user_room(self.user)
            await self.update_room_status(self.user_room, True)

        self.room_group_name = f'chat_room_{self.user_room.id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.room_id:
            await self.update_busy_status(self.user_room, False)
        else:
            await self.update_room_status(self.user_room, False)

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

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
        dict_data = event['dict_data']

        await self.send(
            text_data=json.dumps(dict_data)
        )

    async def send_reject(self, event):
        dict_data = event['dict_data']
        message = {
            "action": "reject-call",
            "message": dict_data
        }
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_user(self):
        return self.scope["user"] if self.scope and "user" in self.scope else AnonymousUser()

    @database_sync_to_async
    def update_room_status(self, room, value):
        room.is_active = value
        room.save()
        return True

    @database_sync_to_async
    def update_busy_status(self, room, value):
        room.is_busy = value
        room.save()
        return True

    @database_sync_to_async
    def get_or_create_user_room(self, user):
        return UserRoom.objects.get_or_create(user=user)

    @database_sync_to_async
    def get_room_by_id(self, room_id):
        return UserRoom.objects.get(id=room_id)


class AdminConsumer(AsyncWebsocketConsumer):
    user = AnonymousUser()
    admin_room = 'admin_room'

    async def connect(self):
        """
         Connects the WebSocket for admin users, adding them to a group.
        """
        if await self.has_permission():
            self.user = self.scope['user']
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
        if action == 'room_list':
            await self.channel_layer.group_send(self.admin_room, {'type': 'send.room_list', 'dict_data': {}})
        if action == 'reject_call':
            room_name = f'chat_room_{message["id"]}'
            await self.channel_layer.group_send(room_name, {'type': 'send.reject', 'dict_data': dict_data['message']})
        pass

    async def send_room_list(self, event):
        rooms = await self.get_rooms()
        message = {
            'action': 'room_list',
            'results': rooms,
        }
        await self.send(text_data=json.dumps(message))

    async def send_user_list(self, event):
        users = await self.get_users()
        message = {
            'action': 'user_list',
            'results': users,
        }
        await self.send(text_data=json.dumps(message))

    async def send_order_list(self, event):
        orders = await self.get_orders()
        message = {
            "action": "order_list",
            "results": orders,
        }
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_rooms(self):
        rooms = UserRoom.objects.filter(is_active=True)
        return self.get_serializer_data_to_dict(UserRoomSerializer(rooms, many=True))

    @database_sync_to_async
    def get_orders(self):
        orders = Order.objects.filter(
            status__in=[Order.OrderStatusChoices.PENDING, Order.OrderStatusChoices.PROCESSING]
        )[:15]
        return self.get_serializer_data_to_dict(OrderSerializer(orders, many=True))

    @database_sync_to_async
    def get_users(self):
        users = get_user_model().objects.all().exclude(id=self.user.id)
        return self.get_serializer_data_to_dict(SafeUserSerializer(users, many=True))

    @database_sync_to_async
    def has_permission(self):
        return self.scope['user'].is_staff or self.scope['user'].is_superuser or self.scope['user'].groups.filter(
            name="Manager"
        ).exists()

    def get_serializer_data_to_dict(self, serializer):
        serialized_data = JSONRenderer().render(serializer.data)
        return json.loads(serialized_data.decode())
