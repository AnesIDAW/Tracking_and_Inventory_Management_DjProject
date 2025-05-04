"""
import os
import django
import json
import paho.mqtt.client as mqtt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TIM_DjProject.settings")  # UPDATE THIS
django.setup()

from inventory.models import Vehicle
from .utils import cache_vehicle_location

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")

def on_connect(client, userdata, flags, rc):
    print("[MQTT] Connected with result code " + str(rc))
    client.subscribe("vehicle/gps")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"[MQTT] Received: {data}")
        plate_number = data["plate_number"]
        latitude = data["latitude"]
        longitude = data["longitude"]

        vehicle = Vehicle.objects.get(plate_number=plate_number)
        vehicle.latitude = latitude
        vehicle.longitude = longitude
        vehicle.save()

        vehicle_data = {
            "vehicle_name": vehicle.name,
            "longitude": vehicle.longitude,
            "latitude": vehicle.latitude,
            "plate_number": vehicle.plate_number,
        }
        cache_vehicle_location(vehicle_data)

    except Exception as e:
        print("[MQTT ERROR]", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(MQTT_HOST, 1883, 60)
client.loop_forever()
"""

import os
import django
import json
import paho.mqtt.client as mqtt
from django.core.cache import cache

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TIM_DjProject.settings")
django.setup()

# Import models and utilities
from inventory.models import Vehicle
from tracking.utils import cache_vehicle_location  # Ensure this exists

# MQTT Configuration
MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")  # Use Docker service name or localhost
MQTT_PORT = 1883
GPS_TOPIC = "vehicle/gps"
RFID_TOPIC = "product/rfid"

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")
    client.subscribe(GPS_TOPIC)
    client.subscribe(RFID_TOPIC)

def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        payload = json.loads(msg.payload.decode())

        if topic == GPS_TOPIC:
            handle_gps(payload)
        elif topic == RFID_TOPIC:
            handle_rfid(payload)
        else:
            print(f"[MQTT] Unknown topic: {topic}")

    except json.JSONDecodeError:
        print(f"[MQTT ERROR] Invalid JSON: {msg.payload.decode()}")
    except Exception as e:
        print(f"[MQTT ERROR] {e}")

def handle_gps(payload):
    plate_number = payload.get("plate_number")
    latitude = payload.get("latitude")
    longitude = payload.get("longitude")

    if not all([plate_number, latitude, longitude]):
        print("[GPS] Missing data in payload")
        return

    try:
        vehicle = Vehicle.objects.get(plate_number=plate_number)
        vehicle.latitude = latitude
        vehicle.longitude = longitude
        vehicle.save()

        vehicle_data = {
            "vehicle_name": vehicle.name,
            "plate_number": vehicle.plate_number,
            "latitude": vehicle.latitude,
            "longitude": vehicle.longitude,
        }
        cache_vehicle_location(vehicle_data)
        print(f"[GPS] Updated {plate_number}: ({latitude}, {longitude})")

    except Vehicle.DoesNotExist:
        print(f"[GPS] Vehicle with plate {plate_number} not found")
    except Exception as e:
        print(f"[GPS ERROR] {e}")

def handle_rfid(payload):
    rfid_tag = payload.get("rfid_tag")
    if rfid_tag:
        cache.set("latest_rfid_tag", rfid_tag, timeout=None)
        print(f"[RFID] Received tag: {rfid_tag}")
    else:
        print("[RFID] Missing tag in payload")

# Set up and start MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()
