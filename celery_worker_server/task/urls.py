from django.urls import path

from .views import initiate_message, connect_message_server

urlpatterns = [
    path('connect-message-server/', connect_message_server),
    path('initiate-message/', initiate_message),
]