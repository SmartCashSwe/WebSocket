import json
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Pc_user, Mobile_user
from asgiref.sync import async_to_sync, sync_to_async



class PcConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if "personal_number" not in self.scope["session"]:
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
            prn=self.scope["session"]["personal_number"]
            mobile_user=await database_sync_to_async(Mobile_user.objects.get)(personal_number=prn)
            # if mobile_user.personal_number in self.allowed_mobile_users:
            await self.channel_layer.group_add(
                mobile_user.personal_number,
                self.channel_name
            )   
            await self.accept()

    async def disconnect(self, close_code):
        if "personal_number" not in self.scope["session"]:
            await self.close()
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
        if "personal_number" in self.scope["session"]:
            message = text_data_json["type"]
            reciever=self.scope["session"]["reciever"]
            await self.channel_layer.group_send(
                reciever,
                {
                    'type': 'forward_message',
                    'type': message,
                    'reciever':self.scope["session"]["personal_number"]
                }
            )
        else:
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
        print(event)
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