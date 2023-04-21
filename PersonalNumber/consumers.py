import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Pc_user, Mobile_user
from asgiref.sync import async_to_sync, sync_to_async


class MobileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        self.personal_number = self.scope['url_route']['kwargs']['personal_number']
        # self.pc_identifier = self.scope['url_route']['kwargs']['pc_identifier']
        print(self.scope["session"].items())
        await self.check_mobile_user_exists()
        # await self.check_pc_user_exists()

        await self.channel_layer.group_add(
            self.personal_number,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        print("hdsajkdhjsakhdjkashdjkashdjkashkjds")
        await self.close()
        await self.channel_layer.group_discard(
            self.personal_number,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data)
        await self.channel_layer.group_send(
            self.personal_number,
            {
                'type': 'forward_message',
                'message': message,
                'personal_number': self.personal_number
            }
        )

    async def forward_message(self, event):
        # if event['personal_number'] in self.allowed_mobile_users:
            message = event['message']
            await self.send(text_data=json.dumps({
                'message': message
            }))

    @database_sync_to_async
    def check_mobile_user_exists(self):
        try:
            self.mobile_user = Mobile_user.objects.get(personal_number=self.personal_number)
            print(self.mobile_user.personal_number)
            print("self.pc_user")
            print("self.pc_user")

        except:
            print("startstartstartstartstartstart")
            async_to_sync( self.disconnect())()
            print("endendendendendendendendendend")
            self.mobile_user = None
        

    @database_sync_to_async
    def check_pc_user_exists(self):
        try:
            self.pc_user = Pc_user.objects.get(pcIdentifier=self.personal_number)
        except Pc_user.DoesNotExist:
            self.pc_user = None
            self.disconnect()





class PcConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if "personal_number" not in self.scope["session"]:
            pc=self.scope["session"]["pcIdentifier"]
            user=await database_sync_to_async(Pc_user.objects.get)(pcIdentifier=pc)
            self.isPc=True
            print(user.pcIdentifier)
            self.pc_identifier = self.scope['url_route']['kwargs']['pc_identifier']
            await self.check_pc_user_exists()

            await self.channel_layer.group_add(
                self.pc_identifier,
                self.channel_name
            )

            await self.accept()
        else:
            mobile_user=await database_sync_to_async(Mobile_user.objects.get)(personal_number=self.scope["session"]["personal_number"])
            if mobile_user.personal_number in self.allowed_mobile_users:
                await self.channel_layer.group_add(
                    self.allowed_mobile_users[mobile_user.personal_number],
                    self.channel_name
                )   

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.pc_identifier,
            self.channel_name
        )

    async def get_session_type(self, session):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(self.scope["session"])
        reciever=text_data['reciever']


        
        await self.channel_layer.group_send(
            reciever,
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