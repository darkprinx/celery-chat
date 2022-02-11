from celery import Celery
from .models import FinishedTask
from django.conf import settings
from worker_server.celery import app
import logging

logger = logging.getLogger(__name__)


@app.task(bind=True)
def new_task(self, message):
    if message.get("message_type") == "send":
        FinishedTask.objects.create(**{"message": "Got task from: {} to {}".format(message.get("from"),
                                                                                   message.get("to"))})
        logger.error("Got task from: {} to {}".format(message.get("from"), message.get("to")))
    else:
        FinishedTask.objects.create(**{"message": "Receive reply from: {} to {}".format(message.get("from"),
                                                                                        message.get("to"))})
        logger.error("Receive reply from: {} to {} and payload is: ".format(message.get("from"), message.get("to")),
                     message)

    if message.get("message_type") == "send":
        payload = {
            "message_type": "reply",
            "from": message.get("to"),
            "to": message.get("from")
        }
        celery_app = Celery(broker=settings.MESSAGE_SERVER_BROKER)
        celery_app.send_task('message_server', args=[payload], kwargs={}, queue="message_server")
