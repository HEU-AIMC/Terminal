from django.urls import path

from run_command.views import ChatConsumer,saveCode
websocket_urlpatterns = [
    path('ws/run_python/', ChatConsumer.as_asgi()),
]


