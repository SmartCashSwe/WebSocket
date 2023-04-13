from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import json

class PrnConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_layer = get_channel_layer()
        await self.channel_layer.group_add(
            'pcRegister_group', # Group name
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to pcRegister
        await self.channel_layer.group_send(
            'pcRegister_group', # Group name
            {
                'type': 'pcRegister_message',
                'message': message,
                'reply_channel': self.channel_name,
            }
        )

        # Wait for response from pcRegister
        response = await self.wait_for_response()

        await self.send(json.dumps(response))

    async def wait_for_response(self):
        while True:
            message = await self.channel_layer.receive(self.channel_name)
            if message.get('type') == 'pcRegister_message':
                return message

    async def pcRegister_message(self, event):
        message = event['message']
        reply_channel = event['reply_channel']

        # Implement your message handling logic here

        response = {
            'message': 'Response message goes here'
        }

        # Send response to Prn
        await self.channel_layer.send(
            reply_channel,
            {
                'type': 'prn_message',
                'message': response,
            }
        )

    async def prn_message(self, event):
        message = event['message']
        await self.send(json.dumps(message))