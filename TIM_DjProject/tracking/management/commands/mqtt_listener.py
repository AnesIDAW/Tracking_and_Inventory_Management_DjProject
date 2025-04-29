import json
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Listen for GPS data via MQTT and store in Redis"

    def handle(self, *args, **kwargs):
        def on_connect(client, userdata, flags, rc):
            print("Connected to MQTT broker with code", rc)
            client.subscribe("gps/vehicle/update")

        def on_message(client, userdata, msg):
            try:
                payload = json.loads(msg.payload.decode())
                plate = payload.get("plate_number")
                lat = payload.get("latitude")
                lon = payload.get("longitude")

                if plate and lat and lon:
                    key = f"vehicle:{plate}"
                    settings.redis_client.hmset(key, {"lat": lat, "lon": lon})
                    settings.redis_client.expire(key, 300)  # optional TTL
                    print(f"[{plate}] Updated: lat={lat}, lon={lon}")
                else:
                    print("Invalid payload", payload)
            except Exception as e:
                print("Error processing message:", e)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("mosquitto", 1883, 60)  # internal Docker hostname
        client.loop_forever()
