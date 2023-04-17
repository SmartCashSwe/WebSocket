from django.urls import path
from .consumers import MobileConsumer, PcConsumer

PrnConsumer_urlpatterns = [
    path(r'ws/prn/(?P<room_name>\w+)/$', MobileConsumer.as_asgi()),
    path(r'ws/pc/(?P<room_name>\w+)/$', PcConsumer.as_asgi()),
]