# 🧭 Tracking and Inventory Management System (TIM Project)

A Django-based web application for managing real-time tracking and inventory, integrated with Redis for caching and MQTT for IoT messaging.

---

## 🚀 Features

- Django 5.1
- Redis caching
- MQTT broker (Mosquitto) for real-time communication
- Jazzmin-admin interface customization
- Dockerized environment for easy setup

---

## 🛠️ Project Structure

```
TIM_DjProject/
│
├── Dockerfile                  # Docker instructions for Django app
├── docker-compose.yml          # Multi-container orchestration
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
├── TIM_DjProject/              # Django settings
├── tracking/                   # Tracking app
├── inventory/                  # Inventory app
├── users/                      # User management
├── dashboard/                  # UI and analytics
├── test/                       # Test script and some GPS dataset to work with
├── custom_jazzmin_templates/   # Custom Jazzmin base.html to use in the project
└── mosquitto/
    └── config/
        └── mosquitto.conf      # MQTT broker config
```

---

## 🧪 Requirements

- Docker Desktop (Windows/macOS/Linux)
- Docker Compose v2+
- Python 3.12 (inside container)

---

## 🧱 Quick Start

### 1. clone the repository

```bash
git clone https://github.com/AnesIDAW/Tracking_and_Inventory_Management_DjProject.git
```

### 2. Build and Start All Services

```bash
docker-compose up --build
```

This starts:
- Django app on `http://localhost:8000`
- Redis on port `6379`
- Mosquitto MQTT on port `1883`
- Websocket on `9001`

### 3. Apply Migrations & Create Superuser

```bash
docker exec -it TIM_django_app python manage.py migrate
docker exec -it TIM_django_app python manage.py createsuperuser
```

### 4. Access the Admin Interface

Go to [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 📡 MQTT Test Hint

You can publish test messages using [MQTT Explorer](https://mqtt-explorer.com/) or `mosquitto_pub`:

```powershell
mosquitto_pub -h localhost -t test/topic -m "hello from host"
```

## GPS tracking Simulation in the Staff dashboard

You can use `test/GPS_send_test.py` to simulate vehicles tracking in the dashboard

```powershell
python .\test\GPS_send_test.py
```

### 🛡️ Rights & Declaration

This project is developed and maintained as part of a **startup initiative** focused on innovative solutions for real-time tracking and inventory management using IoT and containerization technologies.

All rights to the design, source code, and underlying intellectual property are reserved by the creator. Unauthorized reproduction, distribution, or commercial use of any part of this software is strictly prohibited without prior written permission.

> **© TIM Project By Naimi Anes and Brahmi Essadek, 2025. All Rights Reserved.**

This project is currently in active development and represents proprietary work intended for future commercial deployment and potential investor partnerships.

For licensing inquiries, collaboration proposals, or startup engagement, please contact: **anessnaimi29@gmail.com**
