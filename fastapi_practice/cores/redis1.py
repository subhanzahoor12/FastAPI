import json

import redis

from fastapi_practice.cores.config import REDIS_PASSWORD

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    password=REDIS_PASSWORD,
    decode_responses=True,
)


def get_from_redis(key):
    cached = redis_client.get(key)
    if cached:
        print("returned from redis cache")
        return json.loads(cached)


def set_from_db_to_redis(key, data):
    redis_client.set(key, json.dumps(data), ex=30)
    print("fetched from db and cached in redis")
    return data
