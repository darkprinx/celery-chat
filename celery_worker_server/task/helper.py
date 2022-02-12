import os
import redis


def get_redis_connection():
    redis_conn = redis.Redis.from_url(os.environ.get("BROKER_URL"))
    return redis_conn
