from channels.generic.websocket import AsyncWebsocketConsumer
import json


class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Set the room group name for this consumer
        self.room_group_name = 'chat_room'

        # Add the consumer to the group when connected
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

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
