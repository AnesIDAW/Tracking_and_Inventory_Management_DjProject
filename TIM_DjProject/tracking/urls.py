from django.urls import path
from .views import *

app_name = "tracking"

urlpatterns = [
    path("api/vehicle-locations/", vehicle_locations, name="vehicle_locations"),
    path('api/rfid-scan/', rfid_scan_receiver, name='rfid_scan_receiver')
]
