from django.urls import path
from .consumers import PrnConsumer

websocket_urlpatterns = [
    path('ws/prn/', PrnConsumer.as_asgi()),
]