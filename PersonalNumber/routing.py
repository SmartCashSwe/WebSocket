from django.urls import path
from .consumers import PrnConsumer

PrnConsumer_urlpatterns = [
    path('ws/prn/', PrnConsumer.as_asgi()),
]