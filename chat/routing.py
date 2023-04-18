from django.urls import re_path

from chat.consumers import ChatConsumer
from PersonalNumber.consumers import MobileConsumer, PcConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/prn/(?P<room_name>\w+)/(?P<personal_number>\w+)/$", MobileConsumer.as_asgi()),
    re_path(r"ws/pc/(?P<room_name>\w+)/(?P<pc_identifier>\w+)/$", PcConsumer.as_asgi()),

]