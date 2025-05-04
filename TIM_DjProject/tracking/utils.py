import redis
from django.conf import settings
import json

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

def cache_vehicle_location(vehicle_data):
    key = f"vehicle:{vehicle_data['plate_number']}"
    redis_client.set(key, json.dumps(vehicle_data))

def get_all_cached_vehicles():
    keys = redis_client.keys("vehicle:*")
    vehicles = []
    for key in keys:
        data = redis_client.get(key)
        if data:
            vehicles.append(json.loads(data))
    return vehicles