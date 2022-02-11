import json
import os
import redis
from django.http import JsonResponse


def hand_shaking(request):
    data = json.loads(request.body)
    redis_conn = redis.Redis.from_url(os.environ.get("BROKER_URL"))
    redis_conn.set(data.get("server_name"), json.dumps(data))
    payload = {
        "broker_url": os.environ.get("BROKER_URL"),
        "queue_name": os.environ.get("QUEUE_NAME")
    }
    return JsonResponse(payload, status=201)


def servers(request):
    redis_conn = redis.Redis.from_url(os.environ.get("BROKER_URL"))
    server_keys = redis_conn.keys("server*")
    servers_ = []
    for key in server_keys:
        servers_.append(json.loads(redis_conn.get(key)))
    
    return JsonResponse({"data": servers_}, status=201)
