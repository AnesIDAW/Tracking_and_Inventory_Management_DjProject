from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json
from inventory.models import Vehicle

@csrf_exempt
def vehicle_locations(request):
    vehicles = Vehicle.objects.all()  # Fetch vehicles from iventory app

    # Debugging: Print fetched vehicles to Django console
    print("Fetched Vehicles:", list(vehicles))

    if not vehicles.exists():
        return JsonResponse({"error": "No vehicles found"})  # Debugging output
    
    data = [
        {
            "vehicle_name": v.name,
            "longitude": v.longitude,
            "latitude" : v.latitude,  
            "plate_number": v.plate_number,
        }
        for v in vehicles
    ]
    return JsonResponse({"vehicles": data})


@csrf_exempt  # ESP32 can't handle CSRF tokens
def rfid_scan_receiver(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            rfid_tag = data.get("rfid_tag")

            if not rfid_tag:
                return JsonResponse({"error": "RFID tag missing"}, status=400)

            # Optional: you can log it, or check if it already exists
            print(f"[RFID SCAN] Received tag: {rfid_tag}")

            # Instead of redirecting, you can respond with a redirect URL
            return JsonResponse({
                "redirect_url": f"/staff/product-form/?rfid={rfid_tag}"
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
