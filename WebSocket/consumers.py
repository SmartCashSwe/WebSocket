import json
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
from PersonalNumber.models import  Mobile_user
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.sessions.models import Session
from KasaRegister.views import requestHandler
from KasaRegister.models import KasaUser,Licence
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
        if "username" in self.scope["session"]:
            user=await self.check_valid_session()
            await self.channel_layer.group_discard(
                user,
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
        if self.isPc:
            # message = text_data_json["message"]
            receiver=text_data_json["receiver"]
            await self.channel_layer.group_send(
                receiver,
                {
                    'message': text_data_json,
                    'type': 'forward_message',
                    'receiver':receiver
                }
            )
        else:
            # if text_data_json["receiver"] in self.scope["session"]["prn"]:
            receivers=await self.get_receivers_list()
            request=text_data_json["request"]
            info=text_data_json["info"]
            sender=self.scope["session"]["personal_number"]
            message={"request":request, "sender":sender,"info":info}
            for receiver in receivers:
                await self.channel_layer.group_send(
                    receiver,
                    {
                        'type': 'PcSend',
                        'message': message
                    }
                )

        
    async def PcSend(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

        
    async def forward_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def check_valid_session(self):
        try:
            if "username" in self.scope["session"]:
                pc=self.scope["session"]["username"]
                username=requestHandler.encrypt(pc)
                _user = KasaUser.objects.get(username=pc)
                self.isPc=True
                try:
                    l=_user.licence
                    return l.licence
                except Exception as e:
                    self.close()

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
    def get_receivers_list(self):
        try:
            users=self.scope["session"]["receiver"]
            json_users=json.loads(users)
            license_list=[]
            for item in json_users:
                try:
                    user=KasaUser.objects.get(username=item)
                    li:Licence=user.licence
                    license_list.append(li.licence)
                except:
                    pass
            return license_list
        except Exception as e:
            self.close()

        
    @database_sync_to_async
    def print_session(self, token):
        for s in Session.objects.filter(session_key=token):
            decoded = s.get_decoded()