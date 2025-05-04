from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json
from inventory.models import Vehicle
from .utils import cache_vehicle_location, get_all_cached_vehicles

@csrf_exempt
def vehicle_locations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f"[VEHICLE LOCATION] Received data: {data}")
        plate_number = data.get('plate_number')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        try:
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

            return JsonResponse({"message": "Vehicle location updated successfully"})
        except Vehicle.DoesNotExist:
            return JsonResponse({"error": "Vehicle not found"}, status=404)

    elif request.method == 'GET':
        vehicles = get_all_cached_vehicles()
        return JsonResponse({"vehicles": vehicles})

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

    
latest_rfid_tag = None  # global variable

@csrf_exempt
def rfid_scan_receiver(request):
    global latest_rfid_tag
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            rfid_tag = data.get("rfid_tag")

            if not rfid_tag:
                return JsonResponse({"error": "RFID tag missing"}, status=400)

            latest_rfid_tag = rfid_tag  # Store it
            print(f"[RFID SCAN] Received tag: {rfid_tag}")

            return JsonResponse({"status": "received"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def latest_rfid(request):
    global latest_rfid_tag
    return JsonResponse({"rfid_tag": latest_rfid_tag})
