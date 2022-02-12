from celery import Celery
# from .models import FinishedTask
from django.conf import settings
from worker_server.celery import app
import logging

logger = logging.getLogger(__name__)


@app.task(bind=True)
def process_message_task(self, message):
    logger.error("###### Message from {} to {} ######".format(message.get('from'), message.get('to')))

    if message.get("message_type") == "send":
        payload = {
            "message_type": "reply",
            "from": message.get("to"),
            "to": message.get("from")
        }
        celery_app = Celery(broker=settings.MESSAGE_SERVER_BROKER)
        celery_app.send_task('message_server', args=[payload], kwargs={}, queue="message_server")
