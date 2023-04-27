from django.urls import re_path
from .consumers import  PcConsumer

PrnConsumer_urlpatterns = [
    # re_path(r'ws/prn/(?P<room_name>\w+)/$', MobileConsumer.as_asgi()),
    re_path(r'ws/pc/(?P<room_name>\w+)/$', PcConsumer.as_asgi()),
]