import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Pc_user, Mobile_user
from asgiref.sync import async_to_sync, sync_to_async


class MobileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.personal_number = self.scope['url_route']['kwargs']['personal_number']
        # self.pc_identifier = self.scope['url_route']['kwargs']['pc_identifier']
        await self.check_mobile_user_exists()
        # await self.check_pc_user_exists()

        await self.channel_layer.group_add(
            self.personal_number,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.close()
        await self.channel_layer.group_discard(
            self.personal_number,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
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

        except:
            async_to_sync( self.disconnect())()
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
            print("not personal_number")
            pc=self.scope["session"]["pcIdentifier"]
            user=await database_sync_to_async(Pc_user.objects.get)(pcIdentifier=pc)
            self.isPc=True
            self.pc_identifier = self.scope['url_route']['kwargs']['pc_identifier']
            await self.check_pc_user_exists()

            await self.channel_layer.group_add(
                self.pc_identifier,
                self.channel_name
            )

            await self.accept()
        else:
            print("is personal_number")
            prn=self.scope["session"]["personal_number"]
            print(prn)
            mobile_user=await database_sync_to_async(Mobile_user.objects.get)(personal_number=prn)
            print(mobile_user.personal_number)
            # if mobile_user.personal_number in self.allowed_mobile_users:
            await self.channel_layer.group_add(
                mobile_user.personal_number,
                self.channel_name
            )   
            await self.accept()
            print(mobile_user.personal_number)

    async def disconnect(self, close_code):
        if "personal_number" not in self.scope["session"]:
            await self.close()
            print(self.pc_identifier)
            await self.channel_layer.group_discard(
                self.pc_identifier,
                self.channel_name
            )
            # await self.disconnect()
        else:
            await self.close()
            prn=self.scope["session"]["personal_number"]
            mobile_user=await database_sync_to_async(Mobile_user.objects.get)(personal_number=prn)
            await self.channel_layer.group_discard(
                mobile_user.personal_number,

                self.channel_name
            )
            # await self.disconnect()

        pass

    async def get_session_type(self, session):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        if "personal_number" in self.scope["session"]:
            reciever=self.scope["session"]["reciever"]
            await self.channel_layer.group_send(
                reciever,
                {
                    'type': 'forward_message',
                    'message': message
                }
            )
        else:
            print('text_data_json["reciever"]')
            print(text_data_json["reciever"])
            print(self.scope["session"]["mobile_users"])
            print('self.scope.session["mobile_users"]')
            if text_data_json["reciever"] in self.scope["session"]["mobile_users"]:
                await self.channel_layer.group_send(
                    text_data_json["reciever"],
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