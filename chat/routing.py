from django.urls import re_path

from chat.consumers import ChatConsumer
from PersonalNumber.consumers import PrnConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/prn/(?P<room_name>\w+)/$", PrnConsumer.as_asgi()),

]