#!/bin/bash

echo "Starting MQTT consumer..."
python -m tracking.mqtt_consumer &

echo "Starting Django..."
python manage.py runserver 0.0.0.0:8000
