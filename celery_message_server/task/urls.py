from django.urls import path

from .views import hand_shaking, servers

urlpatterns = [
    path('hand-shaking/', hand_shaking),
    path('servers/', servers)
]