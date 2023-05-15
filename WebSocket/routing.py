from django.urls import re_path

from WebSocket.consumers import  PcConsumer

websocket_urlpatterns = [
    re_path(r"ws/$", PcConsumer.as_asgi()),


]