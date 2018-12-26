from django.conf.urls import url
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    # url(r'', consumers.ChatConsumer)
    path('<int:group_id>', consumers.ChatConsumer)
]