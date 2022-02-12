import json
import os
from .helper import get_redis_connection
from django.http import HttpResponse, JsonResponse
from celery import Celery
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def connect_message_server(request):
    payload = {
        "broker_url": os.environ.get("BROKER_URL"),
        "queue_name": os.environ.get("QUEUE_NAME"),
        "server_name": os.environ.get("SERVER_NAME")
    }
    logger.error(payload)

    redis_conn = get_redis_connection()
    redis_conn.set(payload.get("server_name"), json.dumps(payload))
    return JsonResponse({"data": payload, "message": "Successfully connected with message server"})


def initiate_message(request):
    queue = {
        "message_type": "send",
        "from": os.environ.get("QUEUE_NAME"),
        "message": "please do something"
    }

    if not settings.MESSAGE_SERVER_BROKER:
        return HttpResponse("<p>Message Server broker not found</p>")

    server_name = os.environ.get("SERVER_NAME")
    redis_conn = get_redis_connection()
    if not redis_conn.get(server_name):
        return HttpResponse(f"<p>{server_name} is not connected to message server</p>")

    celery_app = Celery(broker=settings.MESSAGE_SERVER_BROKER)
    celery_app.send_task('message_server', args=[queue], kwargs={}, queue='message_server')
    return HttpResponse("<p>Successfully initiated message</p>")
