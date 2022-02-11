import os
import json
import redis
import random
from celery import shared_task, Celery
import logging

logger = logging.getLogger(__name__)


@shared_task(name="message_server")
def message_server(message):
    logger.error("Into message server {}".format(message))
    celery_app = Celery(broker=os.environ.get("BROKER_URL"))
    if message.get("message_type") == "send":
        redis_conn = redis.Redis.from_url(os.environ.get("BROKER_URL"))
        server_keys = redis_conn.keys("server*")
        rec_queue = message.get("from")
        for i in range(10):
            index = random.randint(0, len(server_keys)-1)
            server = json.loads(redis_conn.get(server_keys[index]))
            if message.get("from") != server.get("queue_name"):
                rec_queue = server.get("queue_name")
                break
        if rec_queue == message.get("from"):
            payload = {
                "message_type": "reply",
                "from": os.environ.get("QUEUE_NAME"),
                "to": rec_queue,
                "message": "No available server found, Please try again later"
            }
            celery_app.send_task('task.views.new_task', args=[payload], kwargs={}, queue=rec_queue)
            return
    else:
        rec_queue = message.get("to")
    payload = {
        "message_type": message.get("message_type"),
        "from": message.get("from"),
        "to": rec_queue
    }
    celery_app.send_task('task.task.new_task', args=[payload], kwargs={}, queue=rec_queue)
