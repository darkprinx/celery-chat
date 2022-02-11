from django.urls import path

from .views import assign_task, hand_shaking, check

urlpatterns = [
    path('assign-task/', assign_task),
    path('hand-shaking/', hand_shaking),
    path('check/', check),
]