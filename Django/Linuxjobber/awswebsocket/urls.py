from django.urls import path
from . import views

urlpatterns = [
    path('',views.AwsWebsocketGatewayView.as_view()),
    path('get_recent_messages/',views.get_recent_messages),
    path('get_messages/',views.get_messages),
]