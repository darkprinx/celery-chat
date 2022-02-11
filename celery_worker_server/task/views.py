import json
import os
import requests
from django.http import HttpResponse, JsonResponse
from celery import Celery
from .models import FinishedTask
from django.conf import settings


def hand_shaking(request):
    payload = {
        "broker_url": os.environ.get("BROKER_URL"),
        "queue_name": os.environ.get("QUEUE_NAME"),
        "server_name": os.environ.get("SERVER_NAME"),
        "worker_name": os.environ.get("WORKER_NAME")
    }
    response = requests.get("{}/task/hand-shaking/".format(os.environ.get("MESSAGE_SERVER_HOST")),
                            data=json.dumps(payload))
    data = json.loads(response.text)
    settings.MESSAGE_SERVER_BROKER = data.get("broker_url")
    return JsonResponse({"data": data, "ex": settings.MESSAGE_SERVER_BROKER})


def assign_task(request):
    queue = {
        "message_type": "send",
        "from": os.environ.get("QUEUE_NAME"),
        "message": "please do something"
    }
    if not settings.MESSAGE_SERVER_BROKER:
        return HttpResponse("<p>Message Server broker not found</p>")
    celery_app = Celery(broker=settings.MESSAGE_SERVER_BROKER)
    celery_app.send_task('message_server', args=[queue], kwargs={}, queue='message_server')
    return HttpResponse("<p>Successfully task assigned</p>")


def check(request):
    result = []
    queryset = FinishedTask.objects.all()
    for item in queryset:
        result.append({"message": item.message})
    return JsonResponse({"data": result})
