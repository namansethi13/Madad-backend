from django.urls import re_path
from .import consumers

websocket_urlpatterns = [
    re_path(r'ws/notify-socket/', consumers.NotifyConsumer.as_asgi())
]


