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
            user=await self.check_valid_session()
            await self.channel_layer.group_add(
                    user,
                    self.channel_name
                )   
            await self.accept()
        except:
            pass

    
    async def disconnect(self, close_code):
        if "pcIdentifier" in self.scope["session"]:
            await self.channel_layer.group_discard(
                self.scope["session"]["pcIdentifier"],
                self.channel_name
            )
            await self.close()
            # await self.disconnect()
        elif "personal_number" in self.scope["session"]:
            prn=self.scope["session"]["personal_number"]
            mobile_user=await database_sync_to_async(Mobile_user.objects.get)(personal_number=prn)
            await self.channel_layer.group_discard(
                prn,
                self.channel_name
            )
            await self.close()
        else:
            await self.close()
            # await self.disconnect()

    
    



    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        if self.isPc:
            message = text_data_json["message"]
            receiver=self.scope["session"]["receiver"]
            print(self.scope["session"].session_key)
            await self.channel_layer.group_send(
                receiver,
                {
                    'message': message,
                    'type': 'forward_message',
                    'receiver':"123456789"
                }
            )
        else:
            # if text_data_json["receiver"] in self.scope["session"]["mobile_users"]:
            print(text_data_json["receivers"])
            receivers=text_data_json["receivers"]
            request=text_data_json["request"]
            sender=self.scope["session"]["personal_number"]
            message={"request":request, "sender":sender}
            for receiver in receivers:
                await self.channel_layer.group_send(
                    receiver,
                    {
                        'type': 'PcSend',
                        'message': message
                    }
                )

        


    async def PcSend(self, event):
        print("event")
        print(event)
        message = event['message']
        print("event")
        await self.send(text_data=json.dumps({
            'message': message
        }))

        
    async def forward_message(self, event):
        print("event forward message")
        message = event['message']
        print(event)
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def check_valid_session(self):
        try:
            if "pcIdentifier" in self.scope["session"]:
                pc=self.scope["session"]["pcIdentifier"]
                self.isPc=True
                user = Pc_user.objects.get(pcIdentifier=pc)
                return user.pcIdentifier
            elif "personal_number" in self.scope["session"]:
                mobile=self.scope["session"]["personal_number"]
                self.isPc=False
                user=Mobile_user.objects.get(personal_number=mobile)
                return user.personal_number
            else:
                return self.close()
        except :
            self.close()

        
    @database_sync_to_async
    def print_session(self, token):
        print("startstartstartstart")
        for s in Session.objects.filter(session_key=token):
            decoded = s.get_decoded()
            print("decoded")
            print(decoded)
        print("endendendendendendend")