import asyncio
import csv
import json
import os
import signal
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "vehicle/gps"

VEHICLES = [
    {
        "plate_number": "123014",
        "name": "Renault SYMBOL",
        "file": "compus_to_oran_road_dataset.csv"
    },
    {
        "plate_number": "567890",
        "name": "Renault Fourgon",
        "file": "sba_road_dataset.csv"
    },
    {
        "plate_number": "987654",
        "name": "Mercedes Benz",
        "file": "sba_to_temouchent.csv"
    }
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "test")

# Global stop event
stop_event = asyncio.Event()

# MQTT client
client = mqtt.Client()

def signal_handler(sig, frame):
    print("\n[INFO] Ctrl+C received! Shutting down...")
    stop_event.set()

signal.signal(signal.SIGINT, signal_handler)

async def simulate_vehicle(vehicle):
    file_path = os.path.join(DATA_DIR, vehicle["file"])
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if stop_event.is_set():
                    break
                latitude = float(row[0])
                longitude = float(row[1])
                payload = {
                    "plate_number": vehicle["plate_number"],
                    "vehicle_name": vehicle["name"],
                    "latitude": latitude,
                    "longitude": longitude
                }
                client.publish(MQTT_TOPIC, json.dumps(payload))
                print(f"[MQTT] {vehicle['name']} Published: {payload}")
                await asyncio.sleep(1)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")

async def main():
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    tasks = [simulate_vehicle(vehicle) for vehicle in VEHICLES]
    await asyncio.gather(*tasks)

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] KeyboardInterrupt received. Exiting...")
