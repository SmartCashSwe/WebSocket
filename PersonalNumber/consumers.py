import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Pc_user, Mobile_user


class MobileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.personal_number = self.scope['url_route']['kwargs']['personal_number']
        self.pc_identifier = self.scope['url_route']['kwargs']['pc_identifier']

        await self.check_mobile_user_exists()
        await self.check_pc_user_exists()

        await self.channel_layer.group_add(
            self.pc_identifier,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.pc_identifier,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.pc_identifier,
            {
                'type': 'forward_message',
                'message': message,
                'personal_number': self.personal_number
            }
        )

    async def forward_message(self, event):
        if event['personal_number'] in self.allowed_mobile_users:
            message = event['message']
            await self.send(text_data=json.dumps({
                'message': message
            }))

    @database_sync_to_async
    def check_mobile_user_exists(self):
        try:
            self.mobile_user = Mobile_user.objects.get(personal_number=self.personal_number)
            self.allowed_mobile_users = self.mobile_user.pc_user.mobile_users
        except Mobile_user.DoesNotExist:
            self.mobile_user = None

    @database_sync_to_async
    def check_pc_user_exists(self):
        try:
            self.pc_user = Pc_user.objects.get(pcIdentifier=self.pc_identifier)
        except Pc_user.DoesNotExist:
            self.pc_user = None


class PcConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pc_identifier = self.scope['url_route']['kwargs']['pc_identifier']
        await self.check_pc_user_exists()

        await self.channel_layer.group_add(
            self.pc_identifier,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.pc_identifier,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        personal_number = text_data_json['personal_number']

        if personal_number in self.allowed_mobile_users:
            await self.channel_layer.group_send(
                self.pc_identifier,
                {
                    'type': 'forward_message',
                    'message': message
                }
            )

    async def forward_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def check_pc_user_exists(self):
        try:
            self.pc_user = Pc_user.objects.get(pcIdentifier=self.pc_identifier)
            self.allowed_mobile_users = self.pc_user.mobile_users
        except Pc_user.DoesNotExist:
            self.pc_user = None