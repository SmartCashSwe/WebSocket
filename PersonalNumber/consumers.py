import json
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Pc_user, Mobile_user
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.sessions.models import Session
mobile_format={
    "request":"",
    "sender":"",
}

class PcConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            if "personal_number" not in self.scope["session"]:
                print(1)
                session=await database_sync_to_async( Session.objects.get)(session_key=self.scope['url_route']['kwargs']['token'])
                print(2)
                self.scope["session"]=session.get_decoded()
                print(3)
                # await self.print_session(self.scope['url_route']['kwargs']['token'])
                # print('session.get_decoded().get("pcIdentifier")')
                # print(session.get_decoded())
                # print('session.get_decoded().get("pcIdentifier")')
                pc=session.get_decoded().get("pcIdentifier")
                print(4)
                user=await database_sync_to_async(Pc_user.objects.get)(pcIdentifier=pc)
                print(5)
                self.isPc=True
                print(6)
                self.pc_identifier = self.scope['url_route']['kwargs']['pc_identifier']
                print(self.pc_identifier)
                await self.check_pc_user_exists()
                print(8)
                await self.channel_layer.group_add(
                    self.pc_identifier,
                    self.channel_name
                )
                print(9)

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
        except:
            pass
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
        print(text_data_json)
        if "personal_number" in self.scope["session"]:
            message = text_data_json["message"]
            # receiver=self.scope["session"]["receiver"]
            await self.channel_layer.group_send(
                "123456789",
                {
                    'message': message,
                    'type': 'forward_message',
                    'receiver':"123456789"
                }
            )
        else:
            if text_data_json["receiver"] in self.scope["session"]["mobile_users"]:
                receiver=text_data_json["receiver"]
                request=text_data_json["request"]
                response=text_data_json["response"]
                await self.channel_layer.group_send(
                    receiver,
                    {
                        'type': 'forward_message',
                        'message': response
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
    @database_sync_to_async
    def print_session(self, token):
        print("startstartstartstart")
        for s in Session.objects.filter(session_key=token):
            decoded = s.get_decoded()
            print("decoded")
            print(decoded)
        print("endendendendendendend")